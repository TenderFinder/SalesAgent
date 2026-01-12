"""
Matching routes for tender-product matching operations.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel

from app.models import Match
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/api/v1", tags=["matching"])

# Initialize service
matching_service = MatchingService()


# Request/Response models
class MatchRequest(BaseModel):
    """Request model for matching."""
    use_ai: bool = False
    min_score: float = 1.0
    save_results: bool = True


class MatchResponse(BaseModel):
    """Response model for matching."""
    success: bool
    message: str
    total_matches: int
    matches: List[Match]


@router.post("/match", response_model=MatchResponse)
async def run_matching(request: MatchRequest):
    """
    Run tender-product matching.
    
    - **use_ai**: Use AI-powered matching (requires Ollama)
    - **min_score**: Minimum match score threshold
    - **save_results**: Save results to database
    
    Returns list of matches found.
    """
    try:
        matches = matching_service.execute_matching(
            use_ai=request.use_ai,
            min_score=request.min_score,
            save_results=request.save_results,
            export_json=True
        )
        
        return MatchResponse(
            success=True,
            message=f"Matching complete. Found {len(matches)} matches.",
            total_matches=len(matches),
            matches=matches
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Matching failed: {str(e)}"
        )


@router.post("/match/async")
async def run_matching_async(request: MatchRequest, background_tasks: BackgroundTasks):
    """
    Run matching in background.
    
    Returns immediately and processes matching asynchronously.
    """
    def run_matching_task():
        matching_service.execute_matching(
            use_ai=request.use_ai,
            min_score=request.min_score,
            save_results=request.save_results,
            export_json=True
        )
    
    background_tasks.add_task(run_matching_task)
    
    return {
        "success": True,
        "message": "Matching started in background",
        "status": "processing"
    }


@router.get("/matches", response_model=List[Match])
async def get_matches(
    min_score: Optional[float] = None,
    product: Optional[str] = None,
    limit: Optional[int] = 100
):
    """
    Get stored matches from database.
    
    - **min_score**: Filter by minimum score
    - **product**: Filter by product name
    - **limit**: Maximum number of results
    """
    try:
        if min_score is not None:
            matches = matching_service.match_repo.find_by_score_range(min_score)
        elif product:
            matches = matching_service.match_repo.find_by_product(product)
        else:
            matches = matching_service.match_repo.find_all()
        
        # Apply limit
        matches = matches[:limit]
        
        return matches
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve matches: {str(e)}"
        )


@router.get("/stats")
async def get_statistics():
    """Get matching statistics."""
    try:
        stats = matching_service.get_match_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get statistics: {str(e)}"
        )
