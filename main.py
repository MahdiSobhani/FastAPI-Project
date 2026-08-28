from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from database import init_db
from exceptions import TaskNotFound
from routers.auth import router as auth_router
from routers.tasks import router as tasks_router

app=FastAPI(title="Task Manager API",version="1.0.0")

init_db()

@app.exception_handler(TaskNotFound)
async def task_not_found_handler(request:Request,exc:TaskNotFound):
    return JSONResponse(status_code=404,content={"detail":"Task not found"})


@app.get("/")
def home():
    return {"message":"Task Manager API"}


app.include_router(tasks_router)
app.include_router(auth_router)