from abc import ABC, abstractmethod
from typing import Dict
from logging import getLogger

from .data_objects import Task, Result

logger = getLogger(__name__)


class Storage(ABC):
    def __init__(
            self,
            already_existing_results: Dict[str, Result] = None,
            save_every: int = 2
    ):
        if already_existing_results is None:
            already_existing_results = {}
        self.results: Dict[str, Result] = already_existing_results
        self.save_every = save_every

    def save_result(self, result: Result, task: Task):
        logger.debug(f"Сохраняем запись в Storage. {task=}, {result.status_code=}")
        self.results[task.task_key] = result

        if len(self.results) % self.save_every == 0:
            self.dump_long_term(self.results)

    def get_results(self) -> Dict[str, Result]:
        return self.results

    @abstractmethod
    def dump_long_term(self, results: Dict[str, Result]):
        ...

    def check_result_exists(self, task_key: str):
        return task_key in self.results
