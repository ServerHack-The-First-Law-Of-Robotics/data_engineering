from pydantic import BaseModel, Field


class Task(BaseModel):
    task_key: str = ...


class Result(BaseModel):
    raw_response: str = ...
    is_error: bool = ...
    status_code: int = Field(200, nullable=False)
