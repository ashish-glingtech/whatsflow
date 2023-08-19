import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from apps.routes import events_api
load_dotenv()

app = FastAPI()
app.include_router(events_api, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/healthcheck')
async def healthcheck():
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get("HOST_NAME"), port=os.environ.get("PORT"), reload=os.environ.get("RELOAD"))