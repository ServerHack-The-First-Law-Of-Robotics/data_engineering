from typing import Dict, List

from .data_objects import OkvedCompaniesTask, OkvedCompaniesResult


class OkvedCompaniesStorage:
    def __init__(self, data_pth: str):
        self.data_pth = data_pth
        self.results: Dict[str, OkvedCompaniesResult] = {}

    def save_result(self, result: OkvedCompaniesResult, task: OkvedCompaniesTask):
        self.results[task.task_key] = result

    def get_results(self) -> List[OkvedCompaniesResult]:
        return list(self.results.values())

    def check_result_exists(self, task_key: str):
        return task_key in self.results
