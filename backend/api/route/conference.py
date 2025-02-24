from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

from api.service.response import format_response

# we'll populate these fields when the main app registers this router
router.database = None
router.razorpay_client = None

prefix = "/events"


class EventRegistration(BaseModel):
    name: str
    user_id: int


@router.post("/register-event")
async def register_event(registration: EventRegistration):
    try:
        # collect registered events and their timings
        registered = router.database.get_registered_events(registration.user_id)
        event_details_ids = [event["event_id"] for event in registered]
        event_details = [router.database.search_event(event_id=x)[0] for x in event_details_ids]
        timings = [(event["start_time"], event["end_time"]) for event in event_details]

        to_register = router.database.search_event(event_name=registration.name)
        if not to_register:
            raise ValueError("Event not found")
        to_register = to_register[0]

        if to_register["event_id"] in event_details_ids:
            raise ValueError("Already registered for this event")

        # check each event for time conflict
        for start, end in timings:
            if to_register["start_time"] < end and to_register["end_time"] > start:
                raise ValueError("Time slot collides with another event")

        order_id = None
        if to_register["price"] > 0:
            order_id = await process_payment(registration.user_id, to_register["price"])
            if not order_id:
                raise ValueError("Payment failed")

        registration_id = router.database.register_event(registration.name, registration.user_id)
        return format_response(status_code=200, data={"registration_id": registration_id, "order_id": order_id})

    except Exception as e:
        return {"response": {"error": type(e).__name__, "message": str(e)}}


@router.get("/get-events")
async def get_events():
    try:
        events = router.database.get_event_ids()
        return format_response(status_code=200, data=events)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/get-event/{event_id}")
async def get_event(event_id: int):
    try:
        event = router.database.search_event(event_id=event_id)
        if not event:
            return format_response(status_code=404, data={"error": "Event not found"})

        return format_response(status_code=200, data=event[0])
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/get-all-registrations")
async def get_registrations():
    try:
        registrations = router.database.get_registrations()
        return format_response(status_code=200, data=registrations)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/approve-registration/{registration_id}")
async def approve_registration(registration_id: int):
    try:
        registration = router.database.approve_registration(registration_id)
        return format_response(status_code=200, data=registration)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/registered-events")
async def get_registered_events(user_id: int):
    try:
        events = router.database.get_registered_events(user_id)
        return format_response(status_code=200, data=events)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/cancel-registration/{registration_id}")
async def cancel_registration(registration_id: int):
    try:
        registration = router.database.cancel_registration(registration_id)
        return format_response(status_code=200, data=registration)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/registration-status/{registration_id}")
async def registration_status(registration_id):
    try:
        status = router.database.registration_status(registration_id)
        return format_response(status_code=200, data=status)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


@router.get("/search-event")
async def search_event(
    event_id: Optional[int] = None,
    event_name: Optional[str] = None,
    event_location: Optional[str] = None,
    categories: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: Optional[int] = None,
):
    if categories:
        categories: list[str] = categories.split(",")
    results = router.database.search_event(
        event_id=event_id,
        event_name=event_name,
        event_location=event_location,
        categories=categories,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )
    return format_response(status_code=200, data=results)


@router.get("/leaderboard")
async def get_leaderboard(limit: Optional[int] = 10):
    try:
        leaderboard = router.database.get_leaderboard(limit=limit)
        return format_response(status_code=200, data=leaderboard)
    except Exception as e:
        return format_response(status_code=500, data={"error": type(e).__name__, "message": str(e)})


async def process_payment(user_id: int, amount: float) -> Optional[str]:
    try:
        order = router.razorpay_client.order.create(
            {
                "amount": int(amount * 100),  # Amount in paise
                "currency": "INR",
                "receipt": f"event_{user_id}_{datetime.now().timestamp()}",
                "payment": {"capture": "automatic"},
            }
        )
        order_id = order["id"]
        print(f"Razorpay order created with ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"Payment processing failed: {e}")
        return None


def setup(app):
    app.include_router(router, prefix=prefix)
    router.database = app.database
