from fastapi import FastAPI, HTTPException, Depends, status
from models import RegisterRequest, LoginRequest, TaskCreate, Task
from auth import hash_password, verify_password, create_token, get_current_user

app = FastAPI(title="To-Do API")

# --- In-memory storage (no database yet) ---
users_db: dict = {}   # { email: { username, hashed_password } }
tasks_db: list = []   # [ { id, title, done, owner_email } ]
task_counter: list = [0]  # mutable counter for task IDs


# --- AUTH ROUTES ---

@app.post("/register", status_code=201)
def register(body: RegisterRequest):
    if body.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[body.email] = {
        "username": body.username,
        "hashed_password": hash_password(body.password),
    }
    return {"message": "User registered successfully"}


@app.post("/login")
def login(body: LoginRequest):
    user = users_db.get(body.email)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": body.email})
    return {"access_token": token, "token_type": "bearer"}


# --- TASK ROUTES (all protected) ---

@app.get("/tasks")
def get_tasks(current_user: dict = Depends(get_current_user)):
    my_tasks = [t for t in tasks_db if t["owner_email"] == current_user["email"]]
    return my_tasks


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate, current_user: dict = Depends(get_current_user)):
    task_counter[0] += 1
    new_task = {
        "id": task_counter[0],
        "title": body.title,
        "done": False,
        "owner_email": current_user["email"],
    }
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, current_user: dict = Depends(get_current_user)):
    for task in tasks_db:
        if task["id"] == task_id and task["owner_email"] == current_user["email"]:
            task["done"] = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    for i, task in enumerate(tasks_db):
        if task["id"] == task_id and task["owner_email"] == current_user["email"]:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/{task_id}")
def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    for task in tasks_db:
        if task["id"] == task_id and task["owner_email"] == current_user["email"]:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}/undone")
def undone_task(task_id: int, current_user: dict = Depends(get_current_user)):
    for task in tasks_db:
        if task["id"] == task_id and task["owner_email"] == current_user["email"]:
            task["done"] = False
            return task
    raise HTTPException(status_code=404, detail="Task not found")
