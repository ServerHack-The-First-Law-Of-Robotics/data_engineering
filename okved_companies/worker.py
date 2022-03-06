from logging import getLogger
from aiohttp import ClientSession
from asyncio import sleep

from .data_objects import OkvedCompaniesTask, OkvedCompaniesResult
from .tasks_retriever import OkvedCompaniesTaskRetriever
from .storage import OkvedCompaniesStorage
from base_objects import Proxy

logger = getLogger(__name__)


class OkvedCompaniesWorker:
    def __init__(
            self,
            storage: OkvedCompaniesStorage,
            resource: Proxy,
            worker_id: str
    ):
        self.storage = storage
        self.resource = resource
        self.id = worker_id

    async def run(self, task_retriever: OkvedCompaniesTaskRetriever):
        async with ClientSession() as session:
            while task_retriever.have_task():
                task = task_retriever.next_task()
                logger.info(f"Обрабатываем {task=}")
                # TODO: обработка ошибок
                result = await self.complete_task(session, task)
                self.storage.save_result(result, task)

    async def complete_task(self, session: ClientSession, task: OkvedCompaniesTask) -> OkvedCompaniesResult:
        # TODO: заменить на реальный запрос к rusprofile
        await sleep(1)
        result = OkvedCompaniesResult(
            is_error=False,
            raw_response="aboba"
        )
        return result
        # async with session.get(task.url) as resp:
        #     content = resp.read()
        #     print("content", content)
        #     raise NotImplementedError
