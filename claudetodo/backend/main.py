from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, hash_password, verify_password
from database import Base, get_db, get_engine
from models import Todo, TodoCreate, TodoResponse, TodoUpdate, User


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=get_engine())
    yield


app = FastAPI(title="ClaudeTodo API", lifespan=lifespan)


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/auth/register", status_code=200)
def register(body: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    existing = db.execute(select(User).where(User.email == body.email)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(email=body.email, hashed_password=hash_password(body.password))
    db.add(user)
    db.commit()
    return {"message": "registered"}


@app.post("/auth/login", status_code=200)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = db.execute(select(User).where(User.email == body.email)).scalar_one_or_none()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token: str = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/todos", response_model=list[TodoResponse])
def get_todos(
    status: Literal["pending", "completed", "all"] = "all",
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> list[TodoResponse]:
    stmt = select(Todo)
    if status == "pending":
        stmt = stmt.where(Todo.completed == False)  # noqa: E712
    elif status == "completed":
        stmt = stmt.where(Todo.completed == True)  # noqa: E712
    rows = db.execute(stmt).scalars().all()
    return [TodoResponse.model_validate(row) for row in rows]


@app.post("/todos", status_code=201, response_model=TodoResponse)
def create_todo(
    body: TodoCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> TodoResponse:
    todo = Todo(title=body.title, description=body.description, category=body.category)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    body: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> TodoResponse:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if body.title is not None:
        todo.title = body.title
    if body.description is not None:
        todo.description = body.description
    if body.completed is not None:
        todo.completed = body.completed
    if body.category is not None:
        todo.category = body.category
    db.commit()
    db.refresh(todo)
    return TodoResponse.model_validate(todo)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> None:
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
