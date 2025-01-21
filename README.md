# AI Pipelines

A modular pipeline architecture for processing AI tasks across different channels.

## Features

- Pipeline pattern for processing tasks
- Support for multiple channels (email, chat, etc.)
- Celery task queue integration
- LLM integration with structured outputs
- Error handling and monitoring

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your settings
6. Start the services:
   - Redis server
   - Celery worker: `celery -A app.tasks.celery_config worker --loglevel=info`
   - FastAPI server: `uvicorn app.main:app --reload`

## Project Structure

```
app/
  ├── api/           # FastAPI routes and models
  ├── config/        # Configuration settings
  ├── database/      # Database models and connections
  ├── pipelines/     # Pipeline implementations
  │   ├── email/     # Email processing pipeline
  │   └── base.py    # Base pipeline classes
  ├── services/      # External service integrations
  └── tasks/         # Celery tasks
```

## Usage

Example of processing an email:

```python
from app.tasks.tasks import process_task

input_data = {
    "channel": "email",
    "sender": "user@example.com",
    "subject": "Help request",
    "body": "I need assistance with..."
}

result = process_task.delay(input_data)
print(result.get())
```