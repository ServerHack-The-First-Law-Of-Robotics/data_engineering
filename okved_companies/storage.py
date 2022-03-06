from typing import Dict
from logging import getLogger

from .data_objects import OkvedCompaniesTask, OkvedCompaniesResult
from .data_saving import save_results_as_json

logger = getLogger(__name__)


class OkvedCompaniesStorage:
    def __init__(
            self,
            save_pth: str,
            already_existing_results: Dict[str, OkvedCompaniesResult] = None,
            save_every: int = 2
    ):
        if already_existing_results is None:
            already_existing_results = {}
        self.results: Dict[str, OkvedCompaniesResult] = already_existing_results
        self.save_every = save_every
        self.save_pth = save_pth

    def save_result(self, result: OkvedCompaniesResult, task: OkvedCompaniesTask):
        logger.debug(f"Сохраняем запись в Storage. {task=}, {result.status_code=}, {result.companies_list=}")
        self.results[task.task_key] = result

        if len(self.results) % self.save_every == 0:
            save_results_as_json(self.results, self.save_pth)

    def get_results(self) -> Dict[str, OkvedCompaniesResult]:
        return self.results

    def check_result_exists(self, task_key: str):
        return task_key in self.results
