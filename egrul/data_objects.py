from typing import Optional
from pydantic import Field

from base.data_objects import Task, Result


class EgrulTask(Task):
    inn: str = ...


class EgrulResult(Result):
    pdf_path: Optional[str] = Field(None)
