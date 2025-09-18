from datetime import timedelta

try:
    # livekit-api package
    from livekit.api.access_token import AccessToken, VideoGrants  # type: ignore
except Exception:  # pragma: no cover - allow environments without livekit installed
    AccessToken = None  # type: ignore
    VideoGrants = None  # type: ignore


def issue_token(api_key: str, api_secret: str, identity: str, room: str, ttl_minutes: int = 10) -> str:
    """Issue a LiveKit JWT for a user to join a room using livekit-api."""
    if not AccessToken or not VideoGrants:
        raise RuntimeError("livekit-api is not installed. Please install 'livekit-api'.")

    if not api_key or not api_secret:
        raise RuntimeError("LIVEKIT_API_KEY or LIVEKIT_API_SECRET not configured")

    if not identity or not room:
        raise RuntimeError("identity or room not specified")

    at = AccessToken(api_key=api_key, api_secret=api_secret)
    at = at.with_identity(identity)
    grants = VideoGrants(room_join=True, room=room, can_publish_data=True, can_subscribe=True)
    at = at.with_grants(grants)
    at = at.with_ttl(timedelta(minutes=ttl_minutes))
    return at.to_jwt()


