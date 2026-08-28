from fastapi import APIRouter,Depends,HTTPException,status
from dependencies import get_connection
from schemas import UserCreate,Token
from auth import hash_password,verify_password,create_access_token

router=APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/register",status_code=201)
def register(user:UserCreate,connection=Depends(get_connection)):
    existing_user=connection.execute("SELECT id FROM users WHERE username=?",(user.username,)).fetchone()

    if existing_user:
        raise HTTPException(status_code=409,detail="Username already exists")
    hashed_password=hash_password(user.password)
    cursor=connection.execute("INSERT INTO users(username,password) VALUES(?,?)",(user.username,hashed_password))
    connection.commit()
    return {"id":cursor.lastrowid,"username":user.username}


@router.post("/login",response_model=Token)
def login(user:UserCreate,connection=Depends(get_connection)):
    db_user=connection.execute("SELECT id,username,password FROM users WHERE username=?",(user.username,)).fetchone()
    if db_user is None or not verify_password(user.password,db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    token=create_access_token(db_user["id"])

    return {"access_token":token,"token_type":"bearer"}