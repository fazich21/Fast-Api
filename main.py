
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Task(BaseModel):
    title: str
    completed: bool = False


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


# CREATE a task
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)

    return {
        "message": "Task created successfully",
        "task": task
    }


# SEARCH tasks by title
@app.get("/tasks/search")
def search_tasks(title: str):
    search_results = []

    for task in tasks:
        if title.lower() in task.title.lower():
            search_results.append(task)

    return {
        "search_query": title,
        "total_results": len(search_results),
        "tasks": search_results
    }


# READ all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# READ one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "task_id": task_id,
        "task": tasks[task_id]
    }


# UPDATE a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task

    return {
        "message": "Task updated successfully",
        "task_id": task_id,
        "task": task
    }


# DELETE a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "task_id": task_id,
        "task": deleted_task
    }


