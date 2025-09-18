from fastapi import APIRouter, HTTPException, Query
import traceback

from app.services.livekit_token import issue_token
from app.utils.config import get_settings

router = APIRouter()

@router.get("/token")
def get_token(identity: str = Query(..., min_length=1), room: str = Query(..., min_length=1)):
    settings = get_settings()
    try:
        token = issue_token(
            api_key=settings.livekit_api_key,
            api_secret=settings.livekit_api_secret,
            identity=identity,
            room=room,
        )
    except Exception as e:
        print("Error in issue_token:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"failed_to_issue_token: {str(e)}")
    
    ws_url = settings.livekit_ws_url
    if not ws_url:
        # If your WS URL is blank, throw error
        raise HTTPException(status_code=500, detail="LIVEKIT_WS_URL not configured")

    return {"token": token, "wsUrl": ws_url}
