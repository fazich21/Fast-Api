from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

tasks=[]
class Task(BaseModel):
    title: str
    completed: bool = False

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)

    return {
        "message": "Task created",
        "task": task
    }


@app.get("/tasks/search")
def search_tasks(title: str):
    search_results = []

    for task_group in tasks:
        # Handle a nested list of tasks
        if isinstance(task_group, list):
            for task in task_group:
                if title.lower() in task.title.lower():
                    search_results.append(task)

        # Handle a task stored directly in the list
        else:
            if title.lower() in task_group.title.lower():
                search_results.append(task_group)

    return {
        "search_query": title,
        "total_results": len(search_results),
        "tasks": search_results
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):  
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 2. List se actual task return karein
    return {
        "task_id": task_id,
        "task": tasks[task_id]
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int,task:Task):

    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task

    return{
        "message": "Task Updated",
        "task_id": task_id,
        "task":task
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=404,
            detail="It is Not Found"
        )

    deleted_task = tasks.pop(task_id)

    return{
      "message": "Task Deleted Successfully",
      "task_id": task_id,
      "task": deleted_task
    }

