from __future__ import annotations

from pathlib import Path
from typing import Protocol

from app.rag.schemas import DocumentLoadRequest, LoadedDocument


class DocumentLoader(Protocol):
    async def load(self, request: DocumentLoadRequest) -> LoadedDocument:
        """Load one source document for ingestion."""


class MarkdownFileDocumentLoader:
    async def load(self, request: DocumentLoadRequest) -> LoadedDocument:
        if request.source_type != "markdown":
            raise ValueError(f"Unsupported source type: {request.source_type}")

        path = Path(request.source_uri)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if not path.is_file():
            raise ValueError(f"Document path is not a file: {path}")

        if path.suffix.lower() != ".md":
            raise ValueError(f"Only markdown files are supported for now: {path}")

        content = path.read_text(encoding="utf-8")

        return LoadedDocument(
            id=path.stem,
            title=_title_from_markdown(content, fallback=path.stem),
            source_path=str(path),
            source_type="markdown",
            content=content,
            metadata={
                **request.metadata,
                "file_name": path.name,
            },
        )


async def load_markdown_folder(folder_path: str) -> list[LoadedDocument]:
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise ValueError(f"Path is not a folder: {folder}")

    loader = MarkdownFileDocumentLoader()
    documents: list[LoadedDocument] = []

    for path in sorted(folder.glob("*.md")):
        document = await loader.load(
            DocumentLoadRequest(
                source_uri=str(path),
                source_type="markdown",
                metadata={"folder": str(folder)},
            )
        )
        documents.append(document)

    return documents


def _title_from_markdown(content: str, fallback: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("# "):
            return stripped.replace("# ", "", 1).strip()

    return fallback.replace("-", " ").replace("_", " ").title()
