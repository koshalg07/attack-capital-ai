from datetime import timedelta

try:
    # livekit-server-sdk >= 0.5 uses AccessToken, VideoGrants
    from livekit import AccessToken, VideoGrants  # type: ignore
except Exception:  # pragma: no cover - allow environments without livekit installed
    AccessToken = None  # type: ignore
    VideoGrants = None  # type: ignore


def issue_token(api_key: str, api_secret: str, identity: str, room: str, ttl_minutes: int = 10) -> str:
    """Issue a LiveKit JWT for a user to join a room.

    If livekit sdk is not installed, raise a clear error.
    """
    if not AccessToken or not VideoGrants:
        raise RuntimeError("livekit-server-sdk is not installed. Please install 'livekit'.")

    if not api_key or not api_secret:
        raise RuntimeError("LIVEKIT_API_KEY/SECRET not configured")

    grants = VideoGrants(room_join=True, can_publish_data=True, can_subscribe=True, room=room)
    at = AccessToken(api_key, api_secret, identity=identity)
    at.ttl = timedelta(minutes=ttl_minutes)
    at.add_grants(grants)
    return at.to_jwt()


