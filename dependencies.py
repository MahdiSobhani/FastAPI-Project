from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from config import settings
from database import get_db


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_connection(connection=Depends(get_db)):
    return connection

def get_current_user(token:str=Depends(oauth2_scheme),connection=Depends(get_connection)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError,ValueError):
        raise credentials_exception
    user=connection.execute("SELECT id,username FROM users WHERE id=?",(user_id,)).fetchone()
    if user is None:
        raise credentials_exception

    return dict(user)