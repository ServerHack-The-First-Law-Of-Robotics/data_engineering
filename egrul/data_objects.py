from typing import Optional
from pydantic import Field

from base.data_objects import Result


class EgrulResult(Result):
    pdf_path: Optional[str] = Field(None)
