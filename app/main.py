from fastapi import FastAPI, HTTPException
from app.api.models import InputDataModel, TaskResult
from app.tasks.tasks import process_task

app = FastAPI(
    title="AI Pipelines",
    description="A modular pipeline architecture for processing AI tasks",
    version="0.1.0",
)

@app.post("/tasks/", response_model=TaskResult)
async def create_task(data: InputDataModel):
    """Create a new processing task."""
    try:
        result = process_task.delay(data.model_dump())
        return result.get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint returning API info."""
    return {
        "name": "AI Pipelines API",
        "version": "0.1.0",
        "status": "running",
    }