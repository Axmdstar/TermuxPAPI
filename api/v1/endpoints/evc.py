from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.schemas.user import Token, UserCreate, UserResponse
# from app.services.user_service import UserService
# from app.core.security import create_access_token, verify_password, get_password_hash

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "Ok"}


@router.get("/sendevc")
def sendevc(amount: str, to: str):
    return {"status": "EVC Sent", "amount": amount, "to": to}


# @router.post("/login", response_model=Token)
# def login(
#     db: Session = Depends(get_db),
#     form_data: OAuth2PasswordRequestForm = Depends()
# ):
#     user = UserService.get_user_by_email(db, form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/register", response_model=UserResponse)
# def register(user_in: UserCreate, db: Session = Depends(get_db)):
#     user = UserService.get_user_by_email(db, user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists",
#         )
#
#     user = UserService.create_user(db, user_in)
#     return user
