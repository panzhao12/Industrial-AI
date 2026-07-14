from __future__ import annotations

import re
from typing import Iterable

from app.rag.schemas import ChunkingResult, DocumentChunk, LoadedDocument


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")


class MarkdownChunker:
    def __init__(self, min_chunk_chars: int = 80, max_chunk_chars: int = 1600) -> None:
        self.min_chunk_chars = min_chunk_chars
        self.max_chunk_chars = max_chunk_chars

    def chunk(self, document: LoadedDocument) -> ChunkingResult:
        sections = self._split_by_headings(document.content)

        chunks: list[DocumentChunk] = []
        chunk_index = 0

        for section_title, section_content in sections:
            normalized_content = self._normalize_text(section_content)

            if len(normalized_content) < self.min_chunk_chars:
                continue

            for piece in self._split_large_section(normalized_content):
                chunk = DocumentChunk(
                    id=f"{document.id}_chunk_{chunk_index}",
                    document_id=document.id,
                    chunk_index=chunk_index,
                    section_title=section_title,
                    content=piece,
                    metadata={
                        **document.metadata,
                        "document_title": document.title,
                        "source_path": document.source_path,
                        "source_type": document.source_type,
                    },
                )
                chunks.append(chunk)
                chunk_index += 1

        return ChunkingResult(document_id=document.id, chunks=chunks)

    def _split_by_headings(self, content: str) -> list[tuple[str | None, str]]:
        lines = content.splitlines()

        sections: list[tuple[str | None, list[str]]] = []
        current_title: str | None = None
        current_lines: list[str] = []

        for line in lines:
            heading_match = HEADING_PATTERN.match(line.strip())

            if heading_match:
                if current_lines:
                    sections.append((current_title, current_lines))

                current_title = heading_match.group(2).strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            sections.append((current_title, current_lines))

        return [(title, "\n".join(section_lines)) for title, section_lines in sections]

    def _split_large_section(self, text: str) -> Iterable[str]:
        if len(text) <= self.max_chunk_chars:
            yield text
            return

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        current = ""

        for paragraph in paragraphs:
            if len(current) + len(paragraph) + 2 <= self.max_chunk_chars:
                current = f"{current}\n\n{paragraph}".strip()
            else:
                if current:
                    yield current
                current = paragraph

        if current:
            yield current

    def _normalize_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text