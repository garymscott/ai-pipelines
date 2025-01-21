from pydantic import BaseModel, EmailStr, Field
from typing import Any, Dict, Optional

class InputDataModel(BaseModel):
    channel: str
    sender: Optional[EmailStr] = None
    username: Optional[str] = None
    subject: Optional[str] = None
    body: str

class ProcessingContext(BaseModel):
    parameters: Dict[str, Any] = Field(default_factory=dict)
    intermediates: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)  # Persistent memory store
    errors: list[str] = Field(default_factory=list)  # Error tracking

class OutputDataModel(BaseModel):
    result: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TaskResult(BaseModel):
    task_id: Optional[str] = None
    status: str
    input_data: InputDataModel
    processing_context: ProcessingContext
    output_data: Optional[OutputDataModel] = None

class EventModel(BaseModel):
    event_type: str
    data: InputDataModel