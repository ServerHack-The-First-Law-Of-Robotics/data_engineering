from typing import List
from pydantic import Field

from base.data_objects import Result


class ContactsResult(Result):
    emails: List[str] = Field([], nullable=False)
    phones: List[str] = Field([], nullable=False)
