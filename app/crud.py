import hashlib
from app.db import users_db, tasks_db, get_next_task_id
from app.models import User, Task
from typing import Optional

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_user(username: str, email: str, password: str) -> Optional[User]:
    if username in users_db:
        return None
    
    for u in users_db.values():
        if u.get("email") == email:
            return None
    
    password_hash = hash_password(password)
    user = User(username, email, password_hash)
    users_db[username] = {
        "username": user.username,
        "email": user.email,
        "password_hash": user.password_hash,
        "created_at": user.created_at
    }
    return user

def get_user(username: str) -> Optional[dict]:
    return users_db.get(username)

def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_user(username)
    if user is None:
        return None
    if verify_password(password, user["password_hash"]):
        return user
    return None

def create_task(title: str, description: str, user_id: str) -> Task:
    task_id = get_next_task_id()
    task = Task(task_id, title, description, user_id)
    tasks_db[task_id] = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "user_id": task.user_id,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }
    return task

def get_task(task_id: int, user_id: str) -> Optional[dict]:
    task = tasks_db.get(task_id)
    if task and task["user_id"] == user_id:
        return task
    return None

def get_user_tasks(user_id: str) -> list:
    result = []
    for task in tasks_db.values():
        if task["user_id"] == user_id:
            result.append(task)
    return result

def update_task(task_id: int, user_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[dict]:
    if task_id not in tasks_db:
        return None
    
    task = tasks_db[task_id]
    if task["user_id"] != user_id:
        return None
    
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    
    from datetime import datetime
    task["updated_at"] = datetime.now().isoformat()
    return task

def delete_task(task_id: int, user_id: str) -> bool:
    task = tasks_db.get(task_id)
    if not task or task["user_id"] != user_id:
        return False
    del tasks_db[task_id]
    return True

