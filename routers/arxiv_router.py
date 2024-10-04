from fastapi import APIRouter, HTTPException
from services.arxiv_service import search_arxiv

router = APIRouter()

@router.get("/search")
async def search(query: str = "", max_results: int = 10):
    try:
        results = search_arxiv(query, max_results)
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
