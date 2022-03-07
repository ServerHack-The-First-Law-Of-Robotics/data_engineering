from typing import List, Optional
from pydantic import BaseModel, Field

from base.data_objects import Task, Result


class OkvedCompaniesTask(Task):
    url: str = ...
    okved: str = ...


class RusprofileCompanyData(BaseModel):
    inn: str = ...
    ogrn: Optional[str] = Field(None, nullable=True)


class OkvedCompaniesResult(Result):
    okved: str = ...
    companies_list: List[RusprofileCompanyData] = Field([], nullable=True)
