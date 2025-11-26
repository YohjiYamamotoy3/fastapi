from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from app import schemas, crud
from typing import List

app = FastAPI(title="FastAPI Demo Backend")

SECRET_KEY = "demo-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire_time = expires_delta if expires_delta else timedelta(minutes=15)
    expire = datetime.utcnow() + expire_time
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = crud.get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
async def root():
    return {"message": "FastAPI demo backend is running"}

@app.post("/auth/register", response_model=schemas.Token)
async def register(user_data: schemas.UserRegister):
    user = crud.create_user(user_data.username, user_data.email, user_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=expires)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login", response_model=schemas.Token)
async def login(user_data: schemas.UserLogin):
    user = crud.authenticate_user(user_data.username, user_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    
    token_data = {"sub": user["username"]}
    access_token = create_access_token(token_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
async def create_task(task_data: schemas.TaskCreate, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    task = crud.create_task(task_data.title, task_data.description, username)
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }

@app.get("/tasks", response_model=List[schemas.TaskResponse])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    user_id = current_user["username"]
    tasks = crud.get_user_tasks(user_id)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["username"]
    task = crud.get_task(task_id, user_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task_data: schemas.TaskUpdate, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    updated = crud.update_task(task_id, username, task_data.title, task_data.description, task_data.completed)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    if not crud.delete_task(task_id, current_user["username"]):
        raise HTTPException(status_code=404, detail="Task not found")

