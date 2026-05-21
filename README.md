# To-Do API

A simple REST API for managing tasks, built with FastAPI and JWT authentication.

## Features

- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Full CRUD for tasks (create, read, update, delete)
- Users can only see their own tasks
- Auto-generated interactive API docs

## Tech Stack

- **FastAPI** — modern Python web framework
- **bcrypt** — secure password hashing
- **python-jose** — JWT token creation and verification
- **uvicorn** — ASGI server

## Setup

```bash
cd todo-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` in your browser.

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Create a new user |
| POST | `/login` | No | Login and get a JWT token |
| GET | `/tasks` | Yes | Get all your tasks |
| POST | `/tasks` | Yes | Create a new task |
| GET | `/tasks/{id}` | Yes | Get a specific task |
| PUT | `/tasks/{id}` | Yes | Mark a task as done |
| PUT | `/tasks/{id}/undone` | Yes | Mark a task as not done |
| DELETE | `/tasks/{id}` | Yes | Delete a task |
