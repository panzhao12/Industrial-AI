from __future__ import annotations

import asyncio
from pathlib import Path

from app.rag.chunker import MarkdownChunker
from app.rag.document_loader import load_markdown_folder


async def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    manuals_path = project_root / "data" / "synthetic" / "manuals"

    documents = await load_markdown_folder(str(manuals_path))
    chunker = MarkdownChunker()

    for document in documents:
        result = chunker.chunk(document)

        print(f"\nDocument: {document.title}")
        print(f"Chunks: {len(result.chunks)}")

        for chunk in result.chunks:
            print("-" * 60)
            print(f"Chunk ID: {chunk.id}")
            print(f"Section: {chunk.section_title}")
            print(chunk.content[:300])


if __name__ == "__main__":
    asyncio.run(main())