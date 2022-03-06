from typing import Any
from abc import ABC, abstractmethod
from logging import getLogger
from aiohttp import ClientSession
from asyncio import sleep

from .data_objects import Task, Result
from .storage import Storage
from .task_retriever import TaskRetriever
from base.base_objects import Proxy

logger = getLogger(__name__)


class Worker(ABC):
    def __init__(
            self,
            storage: Storage,
            task_retriever: TaskRetriever,
            resource: Proxy,
            worker_id: str,
            cooldown: int = 10,
            stop_on_error: bool = True
    ):
        self.storage = storage
        self.task_retriever = task_retriever
        self.resource = resource
        self.id = worker_id
        self.cooldown = cooldown
        self.stop_on_error = stop_on_error
        self.cookies = {}

    async def run(self):
        async with ClientSession(cookies=self.cookies) as session:
            while self.task_retriever.have_task():

                task = self.task_retriever.next_task()
                logger.info(f"Обрабатываем {task=}")
                result = await self.complete_task(session, task)
                self.storage.save_result(result, task)

                if result.is_error and self.stop_on_error:
                    logger.info(f"Произошла ошбика в worker {self.id=}. {task=}, {result=}")
                    return
                await sleep(self.cooldown)

    @abstractmethod
    async def complete_task(self, session: ClientSession, task: Task) -> Result:
        ...

    def add_cookie(self, key: str, val: Any):
        self.cookies[key] = val
