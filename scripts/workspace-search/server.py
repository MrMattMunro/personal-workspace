"""MCP semantic search server for workspace docs.

Indexes markdown under plans/, outputs/, reference/, and context/ and serves
natural-language search over them. Enable it via `/setup` (it needs a one-time
`pip install -r requirements.txt`). The index lives in a local .chromadb/ folder
and is built on the first reindex_workspace call.
"""

from mcp.server.fastmcp import FastMCP

from indexer import (
    build_index,
    reindex_file,
    get_collection,
    CHROMA_PATH,
)

mcp_server = FastMCP("workspace-search")

MAX_EXCERPT_CHARS = 1500


@mcp_server.tool()
def search_workspace(
    query: str,
    n_results: int = 5,
    doc_type: str = "",
    area: str = "",
    status: str = "",
) -> str:
    """Search workspace docs with a natural language query.

    Returns ranked excerpts with file paths and line numbers from plans/,
    outputs/, reference/, and context/.

    Args:
        query: Natural language search query (e.g. "budget assumptions", "job search next steps")
        n_results: Number of results to return (1-20, default 5)
        doc_type: Filter by type: "plan", "output", "reference", "context"
        area: Filter by area (the subfolder name under context/, e.g. "career", "health")
        status: Filter plans by status: "implemented", "draft", "active"
    """
    n_results = max(1, min(20, n_results))

    collection = get_collection(CHROMA_PATH)

    if collection.count() == 0:
        return "Index is empty. Run reindex_workspace(force=True) to build it."

    where_clauses = []
    if doc_type:
        where_clauses.append({"doc_type": doc_type})
    if area:
        where_clauses.append({"area": area})
    if status:
        where_clauses.append({"status": status})

    where = None
    if len(where_clauses) == 1:
        where = where_clauses[0]
    elif len(where_clauses) > 1:
        where = {"$and": where_clauses}

    kwargs = {"query_texts": [query], "n_results": n_results}
    if where:
        kwargs["where"] = where

    results = collection.query(**kwargs)

    if not results["ids"] or not results["ids"][0]:
        return "No results found."

    output_parts = []
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (chunk_id, doc, meta, dist) in enumerate(
        zip(ids, documents, metadatas, distances), start=1
    ):
        score = 1 - dist  # cosine distance -> similarity
        file_path = meta["file_path"]
        start = meta["start_line"]
        end = meta["end_line"]
        header = meta.get("header_chain", "")

        meta_bits = []
        if meta.get("area"):
            meta_bits.append(f"area={meta['area']}")
        if meta.get("status"):
            meta_bits.append(f"status={meta['status']}")
        meta_line = f" [{', '.join(meta_bits)}]" if meta_bits else ""

        text = doc
        if len(text) > MAX_EXCERPT_CHARS:
            text = text[:MAX_EXCERPT_CHARS] + "..."

        header_line = f"\nSection: {header}" if header else ""
        output_parts.append(
            f"[{i}] {file_path} (lines {start}-{end}) [score: {score:.2f}]{meta_line}"
            f"{header_line}\n---\n{text}"
        )

    return "\n\n".join(output_parts)


@mcp_server.tool()
def reindex_workspace(
    file_path: str = "",
    force: bool = False,
) -> str:
    """Rebuild the search index over workspace docs.

    Incremental by default - only re-indexes files that changed since last index.

    Args:
        file_path: Relative path to a single file to re-index (e.g. "plans/2026-05-20-foo.md"). If empty, re-indexes all changed files.
        force: If true (with no file_path), full rebuild ignoring modification times.
    """
    if file_path:
        stats = reindex_file(file_path)
        if "error" in stats:
            return stats["error"]
        lines = [f"Re-indexed: {k} ({v} chunks)" for k, v in stats.items() if k != "_total"]
        lines.append(f"Total chunks in index: {stats['_total']}")
        return "\n".join(lines)
    else:
        stats = build_index(force=force)
        changed = {k: v for k, v in stats.items() if k != "_total"}
        if not changed:
            return f"Index is up to date. Total chunks: {stats['_total']}"
        lines = []
        for path, count in sorted(changed.items()):
            lines.append(f"  {path}: {count} chunks")
        lines.append(f"\nTotal chunks in index: {stats['_total']}")
        action = "Rebuilt" if force else "Updated"
        return f"{action} index:\n" + "\n".join(lines)


if __name__ == "__main__":
    mcp_server.run()
