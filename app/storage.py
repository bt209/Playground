"""A tiny in-memory task store for learning API basics."""

from app.models import Task, TaskCreate, TaskUpdate

_tasks: dict[int, Task] = {}
_next_id = 1


def reset() -> None:
    global _next_id
    _tasks.clear()
    _next_id = 1


def create(task: TaskCreate) -> Task:
    global _next_id
    created = Task(id=_next_id, title=task.title, completed=task.completed)
    _tasks[_next_id] = created
    _next_id += 1
    return created


def get(task_id: int) -> Task | None:
    return _tasks.get(task_id)


def list_all(completed: bool | None = None) -> list[Task]:
    tasks = list(_tasks.values())
    if completed is not None:
        tasks = [task for task in tasks if task.completed == completed]
    return tasks


def update(task_id: int, task: TaskUpdate) -> Task | None:
    if task_id not in _tasks:
        return None

    updated = Task(id=task_id, title=task.title, completed=task.completed)
    _tasks[task_id] = updated
    return updated


def delete(task_id: int) -> bool:
    if task_id not in _tasks:
        return False

    del _tasks[task_id]
    return True
