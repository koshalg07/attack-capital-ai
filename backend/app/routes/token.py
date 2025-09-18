from fastapi import APIRouter, HTTPException, Query

from app.services.livekit_token import issue_token
from app.utils.config import get_settings


router = APIRouter()


@router.get("/token")
def get_token(identity: str = Query("", min_length=1), room: str = Query("", min_length=1)):
    if not identity or not room:
        raise HTTPException(status_code=400, detail="identity and room are required")

    settings = get_settings()
    try:
        token = issue_token(
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
            identity=identity,
            room=room,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="failed_to_issue_token")

    ws_url = settings.livekit_ws_url
    return {"token": token, "wsUrl": ws_url}


