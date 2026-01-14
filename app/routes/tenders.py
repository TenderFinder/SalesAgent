"""
Tender routes for managing tender data.
"""

from fastapi import APIRouter, HTTPException

from app.services.matching_service import MatchingService

router = APIRouter(prefix="/api/v1/tenders", tags=["tenders"])

# Initialize service
matching_service = MatchingService()


@router.get("/count")
async def get_tender_count():
    """Get total number of tenders in database."""
    try:
        count = matching_service.tender_repo.count()
        return {"total_tenders": count}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to count tenders: {str(e)}"
        )


@router.post("/fetch")
async def fetch_tenders():
    """Fetch fresh tenders from GeM API and store in database."""
    try:
        tender_collection = matching_service.tender_repo.fetch_from_api()
        tenders = tender_collection.services
        
        if tenders:
            matching_service.tender_repo.save_many(tenders)
        
        return {
            "success": True,
            "message": f"Fetched and stored {len(tenders)} tenders",
            "total_tenders": len(tenders)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch tenders: {str(e)}"
        )
