from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.cruds import user as crud_user
from app.db.session import SessionLocal
from app.services.auth import create_access_token, verify_password, decode_access_token

router = APIRouter()

# Зависимость для работы с сессией БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sign-up/", response_model=UserResponse)
def sign_up(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=new_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user_created = crud_user.create_user(db, new_user)
    token = create_access_token({"sub": user_created.email})
    return UserResponse(id=user_created.id, email=user_created.email, token=token)

@router.post("/login/", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": db_user.email})
    return UserResponse(id=db_user.id, email=db_user.email, token=token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    return UserResponse(id=current_user.id, email=current_user.email)