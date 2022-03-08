from typing import Optional, Dict, Tuple
from abc import ABC, abstractmethod
from logging import getLogger
from aiohttp import ClientSession, BasicAuth
from asyncio import sleep
from uuid import uuid4

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
            resource: Optional[Proxy] = None,
            proxy_login_and_password: Optional[Tuple[str, str]] = None,
            cooldown: int = 10,
            stop_on_error: bool = True,
            use_proxy: bool = True,
            cookies: Optional[Dict] = None,
            sleep_after_fail: Optional[int] = 120
    ):
        self.storage = storage
        self.task_retriever = task_retriever
        self.resource = resource
        self.proxy_login_and_password = proxy_login_and_password
        self.id = str(uuid4())
        self.cooldown = cooldown
        self.stop_on_error = stop_on_error
        self.sleep_after_fail = sleep_after_fail

        if cookies is None:
            cookies = {}
        self.cookies = cookies
        self.use_proxy = use_proxy

    async def run(self):
        async with ClientSession(cookies=self.cookies) as session:
            while self.task_retriever.have_task():

                task = self.task_retriever.next_task()
                logger.info(f"Обрабатываем {task=}")
                result = await self.complete_task(session, task)
                self.storage.save_result(result, task)

                if result.is_error:
                    if self.stop_on_error:
                        logger.info(f"Произошла ошбика в worker {self.id=}. {task=}, {result=}")
                        return
                    await sleep(self.sleep_after_fail)
                else:
                    await sleep(self.cooldown)
            else:
                logger.info(f"Для worker {self.id} не осталось задач")

    @abstractmethod
    async def complete_task(self, session: ClientSession, task: Task) -> Result:
        ...

    def get_response(self, session: ClientSession, url, method: str = "get", kwargs: Optional[Dict] = None):
        if kwargs is None:
            kwargs = {}
        if self.use_proxy:
            kwargs = kwargs.copy()
            kwargs["proxy"] = self.resource

        if self.proxy_login_and_password is not None:
            auth = BasicAuth(*self.proxy_login_and_password)
            kwargs["proxy_auth"] = auth

        kwargs["headers"] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36 "
        }

        if method == "get":
            return session.get(url, **kwargs)
        elif method == "post":
            return session.post(url, **kwargs)
        else:
            raise RuntimeError(f"Некорректный метод запроса: {method}")
