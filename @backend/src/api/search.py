from fastapi import APIRouter, HTTPException

from src.schemas.search import SearchRequest, SearchResponse
from src.services.search import SearchService

router = APIRouter()
search_service = SearchService()


@router.post("/search", response_model=SearchResponse)
async def search_web(request: SearchRequest):
    """웹 검색 및 요약 API"""
    try:
        results, summary = search_service.search_and_summarize(request.query)

        return SearchResponse(
            results=results,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))