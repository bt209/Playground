from fastapi import FastAPI, HTTPException, Query, status

from app import storage
from app.models import Task, TaskCreate, TaskUpdate

app = FastAPI(
    title="Task API Learning Project",
    description="A small in-memory API for learning FastAPI basics.",
    version="1.0.0",
)


@app.get("/", tags=["Learning"])
def read_welcome() -> dict[str, str]:
    """Describe the API and where to find its documentation."""
    return {
        "message": "Welcome to the Task API!",
        "docs": "Visit /docs to try the API in your browser.",
    }


@app.get("/health", tags=["Learning"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task], tags=["Tasks"])
def list_tasks(completed: bool | None = Query(default=None)) -> list[Task]:
    return storage.list_all(completed)


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate) -> Task:
    return storage.create(task)


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int) -> Task:
    task = storage.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, task: TaskUpdate) -> Task:
    updated = storage.update(task_id, task)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int) -> None:
    if not storage.delete(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
