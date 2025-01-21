from typing import Type
from app.pipelines.base import BasePipeline
from app.api.models import InputDataModel

class PipelineRegistry:
    pipeline_classes: dict[str, Type[BasePipeline]] = {}

    @classmethod
    def register(cls, channel: str):
        def decorator(pipeline_class: Type[BasePipeline]):
            cls.pipeline_classes[channel] = pipeline_class
            return pipeline_class
        return decorator

    @classmethod
    def get_pipeline(cls, input_data: InputDataModel) -> BasePipeline:
        pipeline_class = cls.pipeline_classes.get(input_data.channel)
        if pipeline_class:
            return pipeline_class()
        else:
            raise ValueError(f"Unknown pipeline type: {input_data.channel}")