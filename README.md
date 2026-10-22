# FastAPI Learning Project

A small Task API for learning FastAPI, Pydantic, HTTP requests, and automated tests.

The data is stored only in memory. Restarting the server clears every task, which keeps this first project easy to understand.

## Setup on Windows

From PowerShell in the project directory:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks the activation command, enable scripts for your current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- API welcome page: http://127.0.0.1:8000/
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- Alternative ReDoc documentation: http://127.0.0.1:8000/redoc

## Run the tests

```powershell
python -m pytest -q
```

## Endpoints

| Method | URL | Purpose |
| --- | --- | --- |
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Check that the API is running |
| `GET` | `/tasks` | List tasks |
| `GET` | `/tasks?completed=true` | List completed tasks |
| `GET` | `/tasks?completed=false` | List incomplete tasks |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks/{task_id}` | Get one task |
| `PUT` | `/tasks/{task_id}` | Replace a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

Create a task with PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks `
  -ContentType "application/json" `
  -Body '{"title":"Learn FastAPI","completed":false}'
```

## Project structure

- `app/main.py` defines routes and HTTP behavior.
- `app/models.py` defines the JSON schemas with Pydantic.
- `app/storage.py` implements the in-memory CRUD operations.
- `tests/test_api.py` checks that the API behaves correctly.

## Learning exercises

1. Add a `priority` field to `TaskCreate`, `TaskUpdate`, and `Task`. Run tests and use Swagger to verify it.
2. Add a minimum value to the new priority field so users cannot submit negative priorities.
3. Add a `GET /tasks/count` route that returns the number of tasks.
4. Add a `PATCH /tasks/{task_id}` route that allows updating only selected fields.
5. Add validation that task titles cannot contain only spaces.
6. Replace the dictionary storage with a SQLite database after you understand the current code.

## Important concepts

- `@app.get(...)` registers a route for an HTTP method.
- Function parameters connected to URL paths are path parameters.
- Function parameters accepted from `?completed=true` are query parameters.
- Pydantic models validate request JSON before route code runs.
- `response_model` controls what fields FastAPI serializes for a response.
- `HTTPException` returns an API error such as `404 Not Found`.
- Tests use a `TestClient`, so requests run against the app without starting a server.
