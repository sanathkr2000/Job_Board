
# @router.get("/", response_model=list[UserOut])
# def get_all_users(
#     offset: int = Query(0),
#     page_size: int = Query(100),
#     db: Session = Depends(get_db)
# ):
#     try:
#         logger.info(f"Initiating user fetch: offset={offset}, count={page_size}")
#         return get_users(db=db, offset=offset, page_size=page_size)
#     except Exception as e:
#         logger.error(f"Error fetching user list: {e}")
#         raise HTTPException(status_code=500, detail="Unable to fetch users")


# ---------------------------------------------
# """
#     Created_by: Sanathkumar
#     created date: 06/05/2025
#     Modified date: 07/05/2025
# """
# Route: GET /users/
# Description: Fetch a list of users with cachetools(Aiocache)


# --------------------------     cache in memory code     -----------------------------------------------------------

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.db.session import get_db
from app.schemas.user import UsersListResponse
from app.services.user_service import fetch_filtered_paginated_users
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/fetch-all", response_model=UsersListResponse)
async def fetch_all_users(
    name: Optional[str] = Query(None),  # Uncommented the name parameter
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        start_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"[USER_FETCH_START] User data fetch started at {start_time}")

        # Pass the name parameter along with page and page_size
        response = fetch_filtered_paginated_users(db, name, page, page_size)

        end_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"[USER_FETCH_SUCCESS] Successfully fetched user data at {end_time}")

        return response

    except Exception as e:
        logger.error(f"[USER_FETCH_ERROR] Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch users")








