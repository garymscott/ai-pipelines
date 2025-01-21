from typing import Tuple
from app.pipelines.base import PipelineStep
from app.api.models import InputDataModel, ProcessingContext, OutputDataModel
from app.services.llm_factory import LLMFactory

class GenerateResponse(PipelineStep):
    def _process(
        self,
        input_data: InputDataModel,
        context: ProcessingContext,
        output_data: OutputDataModel,
    ) -> Tuple[InputDataModel, ProcessingContext, OutputDataModel]:
        response = self.generate_response(input_data, context)
        output_data.result["response"] = response
        return input_data, context, output_data

    def generate_response(self, data: InputDataModel, context: ProcessingContext) -> str:
        llm = LLMFactory.get_connector("openai")
        category = context.intermediates.get("category", "general")
        
        completion = llm.create_completion(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant. Generate a response for a {category} inquiry."
                },
                {
                    "role": "user",
                    "content": f"Generate a response for this email:\n{data.model_dump()}",
                },
            ]
        )
        
        return completion