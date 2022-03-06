from typing import List
from time import time
import json
from uuid import uuid4
from logging import getLogger
from asyncio import gather, get_event_loop

from base_objects import Proxy
from utils.set_up_logging import set_up_logging
from okved_companies.tasks_retriever import OkvedCompaniesTaskRetriever
from okved_companies.worker import OkvedCompaniesWorker
from okved_companies.storage import OkvedCompaniesStorage

logger = getLogger(__name__)


class OkvedCompaniesCrawler:
    def __init__(
            self,
            resources: List[Proxy],
            storage: OkvedCompaniesStorage,
            base_url: str,
            n_pages: int
    ):
        self.storage = storage
        self.base_url = base_url
        self.task_retriever = OkvedCompaniesTaskRetriever(self.base_url, n_pages, storage)
        self.workers = [OkvedCompaniesWorker(self.storage, resource, str(uuid4())) for resource in resources]

    async def crawl(self):
        logger.info(f"Начинаем собирать данные из {self.base_url}")
        start = time()
        await gather(*[self.run_worker(worker) for worker in self.workers])
        logger.info(f"Закончили собирать данные из {self.base_url}. Время - {time() - start}")

    async def run_worker(self, worker: OkvedCompaniesWorker):
        logger.info(f"Запускаем {worker.id=}")
        await worker.run(self.task_retriever)
        logger.info(f"Закончили собирать данные с помощью {worker.id=}")


if __name__ == "__main__":
    # TODO: убедиться, что отжимаем галку "Только основной код ОКВЭД"
    set_up_logging()
    storage = OkvedCompaniesStorage("../data/okved_22197_companies.csv")
    with open("../resources/proxies.json") as f:
        proxies = json.load(f)

    # TODO: убрать ограничение на количество
    proxies = proxies[:1]

    crawler = OkvedCompaniesCrawler(
        proxies,
        storage,
        "https://www.rusprofile.ru/codes/221970",
        47
    )
    event_loop = get_event_loop()
    event_loop.run_until_complete(crawler.crawl())
    results = storage.get_results()
    print("results", len(results), results)
