from pydantic import BaseModel


class PromptTemplate(BaseModel):
    name: str
    purpose: str
    template: str


DIAGNOSIS_PROMPTS: list[PromptTemplate] = []
