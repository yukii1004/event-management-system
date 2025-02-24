import datetime
import re
from enum import IntEnum
from typing import List, Optional

import razorpay
from fastapi import APIRouter
from pydantic import BaseModel

from api.service import response

router = APIRouter()

# we'll populate these fields when the main app registers this router
router.database = None
router.razorpay_client = None

prefix = "/manage"

black_username_regex = re.compile(r"[a-zA-Z]+(?:\d{8}|\d{0})@snuchennai.edu.in")


class UserType(IntEnum):
    admin = 0
    club = 1
    user = 2


class User(BaseModel):
    username: str
    type: UserType
    interests: List[str]
    upi_id: str = None


class Event(BaseModel):
    club_id: int
    event_name: str
    event_location: str
    categories: List[str]
    start_time: int
    end_time: int
    limit: int
    price: float


class RatingUpdate(BaseModel):
    event_id: int
    rating: int


@router.post("/create-user")
async def create_user(user: User):
    try:
        current_users = router.database.get_usernames()
        if user.username in current_users:
            raise ValueError("Username already exists")
        if black_username_regex.findall(user.username):
            raise ValueError("Username contains invalid characters")

        if user.type == UserType.club and not user.upi_id:
            raise ValueError("UPI ID must be provided for club accounts")

        # todo: validate UPI ID using razorpay
        if user.type == UserType.club:
            try:
                account = router.razorpay_client.payment.validateVpa({"vpa": user.upi_id})
                if not account:
                    raise ValueError("Invalid UPI ID")
            except Exception as e:
                raise ValueError(f"Failed to validate UPI ID: {e}")
            userid = router.database.add_user(user.username, user.type.value, user.interests)
            router.database.add_club(user.id, user.username, upi_id=user.upi_id)
        else:
            userid = router.database.add_user(user.username, user.type.value, user.interests)

        # return the userid
        return response.format_response(200, userid)
    except Exception as e:
        return response.format_response(status_code=400, data={"error": str(type(e).__name__), "message": str(e)})


@router.get("/get-user/")
async def get_user(user_id: Optional[int] = None, username: Optional[str] = None):
    try:
        if not (user_id or username):
            raise KeyError("User ID or username required")

        user = router.database.get_user(user_id=user_id, username=username)
        if not user:
            raise ValueError(f"User not found: {f'id= {user_id}' if user_id else f'username={username}'}")

        return response.format_response(200, user)
    except Exception as e:
        status = 500
        if isinstance(e, ValueError):
            status = 404
        elif isinstance(e, KeyError):
            status = 400

        return response.format_response(status_code=status, data={"error": str(type(e).__name__), "message": str(e)})


@router.get("/all-user-ids")
async def all_users():
    try:
        users = router.database.get_user_ids()
        return response.format_response(status_code=200, data=users)
    except Exception as e:
        return response.format_response(status_code=500, data={"error": str(type(e).__name__), "message": str(e)})


@router.post("/add-event")
async def add_event(event: Event):
    try:
        events = router.database.search_event()
        event_names = [event["event_name"] for event in events]
        if event.event_name in event_names:
            raise ValueError("Event name already exists")
        if event.start_time <= datetime.datetime.now().timestamp():
            raise ValueError("Start time is invalid")

        if event.end_time - event.start_time > 12 * 60 * 60:
            raise ValueError("Event duration is too long")

        if event.limit <= 0:
            raise ValueError("Limit must be greater than 0")

        if len(event.categories) > 50:
            raise ValueError("Too many categories")

        for category in event.categories:
            if black_username_regex.findall(category):
                raise ValueError(f"Category `{category}` contains invalid characters")

        event_id = router.database.add_event(
            event_name=event.event_name,
            event_location=event.event_location,
            categories=event.categories,
            start_time=event.start_time,
            end_time=event.end_time,
            limit=event.limit,
            price=event.price,
            club_id=event.club_id
        )
        return response.format_response(200, event_id)
    except Exception as e:
        status = 500
        if isinstance(e, ValueError):
            status = 400
        return response.format_response(status_code=status, data={"error": str(type(e).__name__), "message": str(e)})


@router.put("/update-club-upi/{club_id}")
async def update_club_upi(club_id: int, upi_id: str):
    try:
        # Verify that the user is a club
        user = router.database.get_user(user_id=club_id)
        if not user:
            raise ValueError("Club not found")
        if user["user_type"] != UserType.club:
            raise ValueError("User is not a club")

        # todo: use razorpay to validate UPI ID
        try:
            account = router.razorplay_client.payment.validateVpa({"vpa": upi_id})
            if not account:
                raise ValueError("Invalid UPI ID")
        except Exception as e:
            raise ValueError(f"Failed to validate UPI ID: {e}")

        # Update the UPI ID
        router.database.update_club_upi(club_id=club_id, upi_id=upi_id)
        return response.format_response(200, {"message": "Club UPI updated successfully"})
    except Exception as e:
        return response.format_response(status_code=400, data={"error": str(type(e).__name__), "message": str(e)})


@router.put("/update-event-rating")
async def update_event_rating(rating_update: RatingUpdate):
    try:
        if not 1 <= rating_update.rating <= 5:  # Manual validation
            raise ValueError("Rating must be between 1 and 5")
        router.database.update_event_rating(rating_update.event_id, rating_update.rating)
        return response.format_response(200, {"message": "Event rating updated successfully"})
    except Exception as e:
        return response.format_response(status_code=400, data={"error": str(type(e).__name__), "message": str(e)})


def setup(app):
    app.include_router(router, prefix=prefix)
    router.database = app.database
