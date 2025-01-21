from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Type
from pydantic import BaseModel
from app.api.models import InputDataModel, ProcessingContext, OutputDataModel
import time

class PipelineConfig(BaseModel):
    max_retries: int = 3
    timeout: int = 30
    critical_steps: List[str] = []
    fallback_handlers: Dict[str, Any] = {}

class PipelineStep(ABC):
    def __init__(self, critical: bool = False):
        self.critical = critical
        self.name = self.__class__.__name__
    
    def process(self, data: InputDataModel, context: ProcessingContext, 
                output_data: OutputDataModel) -> Tuple[InputDataModel, ProcessingContext, OutputDataModel]:
        start_time = time.time()
        try:
            result = self._process(data, context, output_data)
            self._record_metrics(time.time() - start_time)
            return result
        except Exception as e:
            self._record_error(e, context)
            raise

    @abstractmethod
    def _process(self, data: InputDataModel, context: ProcessingContext,
               output_data: OutputDataModel) -> Tuple[InputDataModel, ProcessingContext, OutputDataModel]:
        pass

    def _record_metrics(self, duration: float):
        # TODO: Implement metrics recording
        pass

    def _record_error(self, error: Exception, context: ProcessingContext):
        context.errors.append(f"{self.name}: {str(error)}")

class BasePipeline(ABC):
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        self.steps: List[PipelineStep] = []

    def add_step(self, step: PipelineStep):
        self.steps.append(step)

    def run(self, input_data: InputDataModel) -> Tuple[ProcessingContext, OutputDataModel]:
        context = ProcessingContext()
        output_data = OutputDataModel()

        for step in self.steps:
            try:
                input_data, context, output_data = step.process(
                    input_data, context, output_data
                )
            except Exception as e:
                context.errors.append(f"{step.name}: {str(e)}")
                if step.critical:
                    raise
                # Continue if non-critical

        return context, output_data