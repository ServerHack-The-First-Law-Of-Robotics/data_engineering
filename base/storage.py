from abc import ABC, abstractmethod
from typing import Dict, Type
from logging import getLogger

from utils.data_saving import save_results_as_json, read_results_from_json


from .data_objects import Task, Result

logger = getLogger(__name__)


class Storage(ABC):
    def __init__(
            self,
            save_every: int = 2
    ):
        self.results: Dict[str, Result] = self.load_already_existing()
        self.save_every = save_every

    def save_result(self, result: Result, task: Task):
        logger.debug(f"Сохраняем запись в Storage. {task=}, {result.status_code=}")
        self.results[task.task_key] = result

        if len(self.results) % self.save_every == 0:
            self.dump_long_term()

    def get_results(self) -> Dict[str, Result]:
        return self.results

    def check_result_exists(self, task_key: str):
        return task_key in self.results

    @abstractmethod
    def load_already_existing(self) -> Dict[str, Result]:
        ...

    @abstractmethod
    def dump_long_term(self):
        ...


class JsonStorage(Storage):
    def __init__(
            self,
            *args,
            result_class: Type[Result],
            save_pth: str,
            **kwargs
    ):
        self.save_pth = save_pth
        self.result_class = result_class
        super().__init__(*args, **kwargs)

    def dump_long_term(self):
        # использую функцию, тк считаю, что записывать данные можно и вне Storage. Например, если хотим смержить
        #  несколько файлов
        save_results_as_json(self.results, self.save_pth)

    def load_already_existing(self) -> Dict[str, Result]:
        return read_results_from_json(self.save_pth, self.result_class)
