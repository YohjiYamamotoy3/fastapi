from typing import Optional
from datetime import datetime

class User:
    def __init__(self, username: str, email: str, password_hash: str):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()

class Task:
    def __init__(self, id: int, title: str, description: str, user_id: str, completed: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.completed = completed
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

