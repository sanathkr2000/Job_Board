# services/user_service.py

import json
import logging
import time
from typing import Optional
from cachetools import TTLCache
from sqlalchemy.orm import Session
from app.crud.user import get_users
from app.schemas.user import UserData

logger = logging.getLogger(__name__)
cache = TTLCache(maxsize=100, ttl=600)  # 10 minutes


def update_user_cache(db: Session):
    start_time = time.time()
    logger.info("Data fetch started from Database")

    try:
        users = get_users(db, skip=0, limit=1000000)
        user_dicts = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
        cache["user_json_test"] = json.dumps(user_dicts)
        duration = time.time() - start_time
        logger.info(f"Data fetch and saved to cache completed in {duration:.3f} seconds")
        return user_dicts
    except Exception as e:
        logger.error(f"Failed to warm user cache: {e}")
        raise


def process_filters(data, name: Optional[str]):
    try:
        return [
            user for user in data
            if not name or name.lower() in user.get("name", "").lower()
        ]
    except Exception as e:
        logger.error(f"[FILTER_ERROR] Failed to filter user data: {str(e)}", exc_info=True)
        return []


def paginate(data, page: int, page_size: int):
    try:
        if page < 1 or page_size < 1:
            raise ValueError("Page and page_size must be greater than 0")

        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end]

    except Exception as e:
        logger.error(f"[PAGINATION_ERROR] Failed to paginate data: {str(e)}", exc_info=True)
        return []


def fetch_filtered_paginated_users(db: Session, name: Optional[str], page: int, page_size: int):
    try:
        start = time.time()
        if "user_json_test" in cache:
            logger.info("[USER_CACHE_HIT] Returning users from cache")
            users = json.loads(cache["user_json_test"])
        else:
            logger.info("[USER_CACHE_MISS] No cache found. Fetching from DB")
            users = update_user_cache(db)

        filtered_users = process_filters(users, name)
        paginated_users = paginate(filtered_users, page, page_size)
        end = time.time() - start
        logger.info(f"[USER_FETCH_TIME] Data fetched in {end:.4f} seconds")

        return {
            "total": len(filtered_users),
            "page": page,
            "page_size": page_size,
            "users": [UserData(**user) for user in paginated_users]
        }

    except Exception as e:
        logger.error(f"[USER_FETCH_ERROR] Failed to fetch users: {str(e)}", exc_info=True)
        return {
            "total": 0,
            "page": page,
            "page_size": page_size,
            "users": [],
            "error": "An error occurred while fetching user data."
        }
