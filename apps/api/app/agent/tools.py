from typing import Any, Protocol

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    requested_by: str | None = None


class ToolCallResult(BaseModel):
    tool_name: str
    ok: bool
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ToolRegistry(Protocol):
    async def list_tools(self) -> list[ToolDefinition]:
        """List tools available to a future diagnosis agent."""

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResult:
        """Call a future validated tool adapter."""


class PlaceholderToolRegistry:
    async def list_tools(self) -> list[ToolDefinition]:
        return []

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResult:
        return ToolCallResult(
            tool_name=request.tool_name,
            ok=False,
            error="Manual tool calling is not implemented yet.",
        )
