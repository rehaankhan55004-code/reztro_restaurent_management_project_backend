from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
# Import your User model if needed, or query directly

def verify_token(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Local authentication dependency replacing Cognito JWT verification.
    Reads the user ID sent from the frontend headers.
    """
    user_id = request.headers.get("x-user-id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated. Missing user session.")

    # You can return a structured dictionary matching your previous token payload format
    return {
        "auth": {"sub": user_id, "token_use": "local"},
        "user": {"id": user_id}
    }


# For WebSocket token verification (Local fallback)
async def verify_token_from_query(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token verification failed: Missing token")
    return {"auth": {"sub": token}, "user": {}}