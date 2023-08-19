from fastapi import APIRouter, Depends, Response, Body, Request, Header, status
from apps.utility import MongoDBConnect

router = APIRouter()

@router.post("/events")
async def data_ingestion(request: Request, body=Body(...)):
    async with MongoDBConnect() as db:
        x = await db.events.insert_one(body)
    return {"status": True, "inserted_id": str(x.inserted_id)}


"""
curl --location 'https://studious-engine-v66657v4grg3p99-8000.app.github.dev/api/events' \
--header 'Content-Type: application/json' \
--data '{
    "data":1
}'
"""