from typing import List

from base.task_retriever import TaskRetriever
from .data_objects import EgrulTask


class EgrulTaskRetriever(TaskRetriever):
    def __init__(
            self,
            *args,
            inns: List[str],
            **kwargs
    ):
        self.inns = inns
        super().__init__(*args, **kwargs)

    def create_tasks(self) -> List[EgrulTask]:
        return [EgrulTask(inn=inn, task_key=inn) for inn in self.inns]
