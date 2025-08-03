from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    results: list
    summary: str | None