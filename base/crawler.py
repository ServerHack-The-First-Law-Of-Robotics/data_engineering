from typing import List
from time import time
from asyncio import gather
from logging import getLogger

from .worker import Worker

logger = getLogger(__name__)


class Crawler:
    def __init__(
            self,
            workers: List[Worker]
    ):
        self.workers = workers

    async def crawl(self):
        logger.info(f"Начинаем собирать данные")
        start = time()
        await gather(*[self.run_worker(worker) for worker in self.workers])
        logger.info(f"Закончили собирать данные. Время - {time() - start}")

    async def run_worker(self, worker: Worker):
        logger.info(f"Запускаем {worker.id=}")
        await worker.run()
        logger.info(f"Закончили собирать данные с помощью {worker.id=}")
