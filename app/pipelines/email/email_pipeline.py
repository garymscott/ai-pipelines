from app.pipelines.base import BasePipeline
from app.pipelines.registry import PipelineRegistry
from app.pipelines.email.classify_email import ClassifyEmail
from app.pipelines.email.generate_response import GenerateResponse

@PipelineRegistry.register("email")
class EmailPipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self.add_step(ClassifyEmail(critical=True))
        self.add_step(GenerateResponse())