from abc import ABC, abstractmethod
from typing import List

from .storage import Storage
from .data_objects import Task, INNTask, OGRNTask


class TaskRetriever(ABC):
    def __init__(
            self,
            storage: Storage
    ):
        tasks = self.create_tasks()
        not_ready_tasks = []
        for task in tasks:
            if not storage.check_result_exists(task.task_key):
                not_ready_tasks.append(task)
        self.tasks = not_ready_tasks

    @abstractmethod
    def create_tasks(self) -> List[Task]:
        ...

    def have_task(self) -> bool:
        return len(self.tasks) > 0

    def next_task(self) -> Task:
        return self.tasks.pop(0)


class INNTaskRetriever(TaskRetriever):
    def __init__(
            self,
            *args,
            inns: List[str],
            **kwargs
    ):
        self.inns = inns
        super().__init__(*args, **kwargs)

    def create_tasks(self) -> List[INNTask]:
        return [INNTask(inn=inn, task_key=inn) for inn in self.inns]


class OGRNTaskRetriever(TaskRetriever):
    def __init__(
            self,
            *args,
            ogrns: List[str],
            **kwargs
    ):
        self.ogrns = ogrns
        super().__init__(*args, **kwargs)

    def create_tasks(self) -> List[OGRNTask]:
        return [OGRNTask(ogrn=inn, task_key=inn) for inn in self.ogrns]
