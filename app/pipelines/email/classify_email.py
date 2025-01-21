from enum import Enum
from pydantic import BaseModel, Field
from typing import Tuple
from app.pipelines.base import PipelineStep
from app.api.models import InputDataModel, ProcessingContext, OutputDataModel
from app.services.llm_factory import LLMFactory

class CategoryModel(str, Enum):
    GENERAL = "general"
    BILLING = "billing"
    COLLABORATION = "collaboration"

class CategoryResponseModel(BaseModel):
    category: CategoryModel
    confidence: float = Field(ge=0, le=1)
    reasoning: str = Field(description="Explain your reasoning for the category.")

class ClassifyEmail(PipelineStep):
    def _process(
        self,
        input_data: InputDataModel,
        context: ProcessingContext,
        output_data: OutputDataModel,
    ) -> Tuple[InputDataModel, ProcessingContext, OutputDataModel]:
        completion = self.classify_email(input_data)
        context.intermediates["category"] = completion.category
        return input_data, context, output_data

    def classify_email(self, data: InputDataModel) -> CategoryResponseModel:
        llm = LLMFactory.get_connector("openai")
        
        completion = llm.create_completion(
            response_model=CategoryResponseModel,
            messages=[
                {
                    "role": "system",
                    "content": "Analyze incoming tickets and classify them into categories while giving a confidence score."
                },
                {
                    "role": "user",
                    "content": f"Here's a new email for you to classify:\n{data.model_dump()}",
                },
            ]
        )
        
        return completion