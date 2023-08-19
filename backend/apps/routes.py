from fastapi import APIRouter
from apps import events

events_api = APIRouter()
events_api.include_router(events.router, tags=["events"])