
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserSession
from app.schemas import UserRegister, UserResponse, UserLogin
from app.security import hash_password, verify_password, create_session_token, hash_session_token, get_session_expiry

from datetime import datetime, timezone
from fastapi import Request

from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    # Read the session token from the HttpOnly cookie.
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )

    # Look up the hash, never the raw token.
    token_hash = hash_session_token(token)

    session = db.scalar(
        select(UserSession).where(
            UserSession.token_hash == token_hash
        )
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session.",
        )

    # Check whether the server-side session has expired.
    expires_at = session.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
        )

    user = db.get(User, session.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    return user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    # Normalize the email before checking or storing it.
    email = str(user_data.email).strip().lower()

    # Check whether this email is already registered.
    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Create a database user with a hashed password.
    user = User(
        email=email,
        password_hash=hash_password(user_data.password),
        display_name=(
            user_data.display_name.strip()
            if user_data.display_name
            else None
        ),
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        # Also handles a duplicate email submitted concurrently.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    return user




@router.post("/login")
def login_user(
    user_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):
    email = str(user_data.email).strip().lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if (
        user is None
        or user.password_hash is None
        or not verify_password(
            user_data.password,
            user.password_hash,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    # Generate a secret token for the browser.
    token = create_session_token()

    # Store only its hash in PostgreSQL.
    session = UserSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=get_session_expiry(),
    )

    db.add(session)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create a login session.",
        )

    # Local development: Secure=False because localhost uses HTTP.
    # Set Secure=True when deployed over HTTPS.
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/",
    )

    return {
        "message": "Login successful.",
        "user": UserResponse.model_validate(user),
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("/logout")
def logout_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    token = request.cookies.get("session_token")

    if token:
        token_hash = hash_session_token(token)

        session = db.scalar(
            select(UserSession).where(
                UserSession.token_hash == token_hash
            )
        )

        if session is not None:
            db.delete(session)
            db.commit()

    # Clear the browser cookie even if the session is already gone.
    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/",
    )

    return {"message": "Logout successful."}
