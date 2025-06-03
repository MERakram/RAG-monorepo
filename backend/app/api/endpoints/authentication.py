from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from app.core.dependencies import create_user_dep, authenticate_user, require_active_user
from app.schema.user import User, Token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


# Get current logged-in user details
@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(require_active_user)],
):
    return current_user

@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_description="User created successfully",
    name="auth:sign-up",
    response_model_exclude_none=True,
    response_model=User,
)
def sign_up(user_created: User = Depends(create_user_dep)):
    """
    Create a new user.
    """
    return user_created


@router.post(
    "/sign-in",
    response_description="User signed in successfully",
    name="auth:sign-in",
)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Sign in to get an access token.
    """
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        active=user.active,
        role=user.role,
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_description="User logged out successfully",
    name="auth:logout",
)
async def logout(response: Response):
    """
    Logout user (client-side token removal is typical for JWT).
    This endpoint can be used to clear cookies if set, or for other server-side session cleanup if applicable.
    """
    return {"message": "Logout successful"}