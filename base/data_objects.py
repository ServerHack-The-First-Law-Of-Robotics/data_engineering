from typing import Optional
from pydantic import BaseModel, Field, validator
from uuid import uuid4


class Task(BaseModel):
    # task_key используется для опознавания задачи. Например, если нам нужно парсить по ИНН - кладите сюда ИНН. task_key
    #  используется такими компонентами, как Storage, чтобы отсекать уже выполненные задачи (например, уже спаршенные
    #  ИНН)
    task_key: str = ...


class Result(BaseModel):
    raw_response: Optional[str] = None
    is_error: bool = ...
    status_code: int = Field(200, nullable=True)
