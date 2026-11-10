"""Chunking and ChromaDB indexing for workspace docs.

Indexes markdown under plans/, outputs/, reference/, and context/. Each doc is
split by markdown headers into chunks, tagged with a doc_type (from the top
folder) and an area (the subfolder under context/, if any), plus a status for
plans. Generic — no project-specific classification; the area tag is just
whatever folder a doc lives in.
"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import chromadb

# Paths relative to project root (this file is scripts/workspace-search/indexer.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_ROOTS = [
    PROJECT_ROOT / "plans",
    PROJECT_ROOT / "outputs",
    PROJECT_ROOT / "reference",
    PROJECT_ROOT / "context",
]
CHROMA_PATH = str(Path(__file__).resolve().parent / ".chromadb")
MTIME_FILE = os.path.join(CHROMA_PATH, "file_mtimes.json")


@dataclass
class Chunk:
    chunk_id: str       # "{rel_path}::{start_line}-{end_line}"
    file_path: str      # relative to project root, forward slashes
    start_line: int     # 1-indexed
    end_line: int       # 1-indexed, inclusive
    header_chain: str   # "Doc Title > Section > Subsection"
    doc_type: str       # "plan", "output", "reference", "context"
    area: str           # subfolder name under the top folder, or ""
    status: str         # "implemented", "draft", "active", "" (plans only)
    text: str


def classify_file(rel_path: str) -> tuple[str, str]:
    """Return (doc_type, area) from the relative path.

    doc_type comes from the top-level folder. area is the next subfolder, if the
    file sits in one (e.g. context/career/foo.md -> ("context", "career")).
    """
    posix = rel_path.replace("\\", "/")
    parts = posix.split("/")
    top = parts[0]

    doc_type = {
        "plans": "plan",
        "outputs": "output",
        "reference": "reference",
        "context": "context",
    }.get(top, "")

    area = parts[1] if len(parts) >= 3 else ""  # only if nested in a subfolder
    return doc_type, area


def parse_status(lines: list[str]) -> str:
    """Parse `**Status:** <value>` from the first 20 lines of a plan file."""
    pattern = re.compile(r"\*\*Status:\*\*\s*([^\n]+)")
    for line in lines[:20]:
        m = pattern.search(line)
        if not m:
            continue
        value = m.group(1).strip().lower()
        if value == "draft":
            return "draft"
        if value.startswith("implemented"):
            return "implemented"
        if value in ("in progress", "active", "ready", "ready for /implement"):
            return "active"
        return ""
    return ""


def chunk_header_split(
    lines: list[str],
    rel_path: str,
    doc_type: str,
    area: str,
    status: str,
) -> list[Chunk]:
    """Split by markdown headers. Each section becomes one chunk."""
    chunks = []
    header_stack: dict[int, str] = {}
    block_start = 1
    block_lines: list[str] = []

    def emit_chunk(end_line: int):
        text = "\n".join(block_lines).strip()
        if not text:
            return
        chain_parts = [header_stack[d] for d in sorted(header_stack) if d in header_stack]
        chunks.append(Chunk(
            chunk_id=f"{rel_path}::{block_start}-{end_line}",
            file_path=rel_path,
            start_line=block_start,
            end_line=end_line,
            header_chain=" > ".join(chain_parts) if chain_parts else "",
            doc_type=doc_type,
            area=area,
            status=status,
            text=text,
        ))

    for i, line in enumerate(lines, start=1):
        header_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if header_match:
            if block_lines:
                emit_chunk(i - 1)
            depth = len(header_match.group(1))
            title = header_match.group(2).strip()
            header_stack[depth] = title
            for d in list(header_stack.keys()):
                if d > depth:
                    del header_stack[d]
            block_start = i
            block_lines = [line]
        else:
            block_lines.append(line)

    if block_lines:
        emit_chunk(len(lines))

    return chunks


def chunk_file(abs_path: Path, rel_path: str) -> list[Chunk]:
    """Read a file and return its chunks."""
    doc_type, area = classify_file(rel_path)

    with open(abs_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    status = parse_status(lines) if doc_type == "plan" else ""
    return chunk_header_split(lines, rel_path, doc_type, area, status)


def get_collection(chroma_path: str = CHROMA_PATH):
    """Get or create the ChromaDB collection."""
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(
        name="workspace_docs",
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def discover_files() -> list[tuple[Path, str]]:
    """Walk all corpus roots and return (abs_path, rel_path_posix) for .md files."""
    results = []
    for root in CORPUS_ROOTS:
        if not root.exists():
            continue
        for abs_path in sorted(root.rglob("*.md")):
            rel = abs_path.relative_to(PROJECT_ROOT)
            results.append((abs_path, rel.as_posix()))
    return results


def load_mtimes(mtime_file: str) -> dict:
    if os.path.exists(mtime_file):
        with open(mtime_file, "r") as f:
            return json.load(f)
    return {}


def save_mtimes(mtime_file: str, mtimes: dict):
    os.makedirs(os.path.dirname(mtime_file), exist_ok=True)
    with open(mtime_file, "w") as f:
        json.dump(mtimes, f, indent=2)


def delete_file_chunks(collection, rel_path: str) -> int:
    results = collection.get(where={"file_path": rel_path})
    if results["ids"]:
        collection.delete(ids=results["ids"])
        return len(results["ids"])
    return 0


def index_file(abs_path: Path, rel_path: str, collection) -> int:
    delete_file_chunks(collection, rel_path)

    chunks = chunk_file(abs_path, rel_path)
    if not chunks:
        return 0

    collection.add(
        ids=[c.chunk_id for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{
            "file_path": c.file_path,
            "start_line": c.start_line,
            "end_line": c.end_line,
            "header_chain": c.header_chain,
            "doc_type": c.doc_type,
            "area": c.area,
            "status": c.status,
        } for c in chunks],
    )
    return len(chunks)


def build_index(chroma_path: str = CHROMA_PATH, force: bool = False) -> dict:
    """Index all docs. If not force, only re-index changed files.

    Returns dict with stats: {file_path: chunk_count, ...} and "_total" key.
    """
    collection = get_collection(chroma_path)
    stored_mtimes = {} if force else load_mtimes(MTIME_FILE)
    current_mtimes = {}
    stats: dict = {}

    files = discover_files()
    current_paths = set()

    for abs_path, rel_path in files:
        current_paths.add(rel_path)
        mtime = os.path.getmtime(abs_path)
        current_mtimes[rel_path] = mtime

        if not force and rel_path in stored_mtimes:
            if stored_mtimes[rel_path] == mtime:
                continue

        count = index_file(abs_path, rel_path, collection)
        stats[rel_path] = count

    # Remove chunks for deleted files
    for old_path in set(stored_mtimes.keys()) - current_paths:
        deleted = delete_file_chunks(collection, old_path)
        if deleted:
            stats[old_path] = f"deleted ({deleted} chunks)"

    save_mtimes(MTIME_FILE, current_mtimes)

    total = collection.count()
    stats["_total"] = total
    return stats


def reindex_file(file_path: str, chroma_path: str = CHROMA_PATH) -> dict:
    """Re-index a single file. file_path is relative to project root."""
    abs_path = PROJECT_ROOT / file_path.replace("/", os.sep)
    if not abs_path.exists():
        return {"error": f"File not found: {file_path}"}

    rel_path = Path(file_path).as_posix()
    collection = get_collection(chroma_path)
    count = index_file(abs_path, rel_path, collection)

    stored_mtimes = load_mtimes(MTIME_FILE)
    stored_mtimes[rel_path] = os.path.getmtime(abs_path)
    save_mtimes(MTIME_FILE, stored_mtimes)

    total = collection.count()
    return {rel_path: count, "_total": total}


if __name__ == "__main__":
    print("Corpus roots:")
    for root in CORPUS_ROOTS:
        print(f"  {root}")
    print(f"ChromaDB path: {CHROMA_PATH}")
    print("Building full index (force=True)...")
    stats = build_index(force=True)
    print()
    for path, count in sorted(stats.items()):
        if path == "_total":
            continue
        print(f"  {path}: {count} chunks")
    print(f"\nTotal chunks in index: {stats['_total']}")
