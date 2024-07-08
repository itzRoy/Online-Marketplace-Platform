from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.core import AgnosticDatabase

from backend import controllers, deps, schemas, security
from backend.custom_router import router


@router.post("/login", response_model=schemas.Token)
async def login_with_oauth2(
    db: AgnosticDatabase = Depends(deps.get_db),
    data: OAuth2PasswordRequestForm = Depends(),
):
    """
    First step with OAuth2 compatible token login,
    get an access token for future requests.
    """
    user = await controllers.user.authenticate(
        db, email=data.username, password=data.password
    )
    if not data.password or not user or not controllers.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login failed; incorrect email or password",
        )

    return schemas.Token(
        access_token=security.create_access_token(subject=user.id)
    )
