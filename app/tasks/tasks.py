from app.tasks.celery_config import celery_app
from app.api.models import InputDataModel, TaskResult
from app.pipelines.registry import PipelineRegistry

@celery_app.task(name="task.process_task")
def process_task(data: dict) -> dict:
    input_data = InputDataModel(**data)
    pipeline = PipelineRegistry.get_pipeline(input_data)
    processing_context, output_data = pipeline.run(input_data)
    
    task_result = TaskResult(
        task_id=process_task.request.id,
        status="completed",
        input_data=input_data,
        processing_context=processing_context,
        output_data=output_data,
    )
    
    return task_result.model_dump()