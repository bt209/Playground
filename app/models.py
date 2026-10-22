from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Data accepted when a new task is created."""

    title: str = Field(min_length=1, max_length=100)
    completed: bool = False


class TaskUpdate(BaseModel):
    """Data accepted when an existing task is replaced."""

    title: str = Field(min_length=1, max_length=100)
    completed: bool = False


class Task(BaseModel):
    """Complete task returned by the API."""

    id: int
    title: str
    completed: bool
