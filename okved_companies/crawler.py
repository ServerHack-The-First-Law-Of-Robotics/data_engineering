from typing import List
from time import time
import json
from uuid import uuid4
from logging import getLogger
from asyncio import gather, get_event_loop

from base_objects import Proxy
from utils import set_up_logging, read_proxies
from okved_companies.tasks_retriever import OkvedCompaniesTaskRetriever
from okved_companies.worker import OkvedCompaniesWorker
from okved_companies.storage import OkvedCompaniesStorage
from okved_companies.data_saving import save_results_as_json, read_results_from_json

logger = getLogger(__name__)


class OkvedCompaniesCrawler:
    def __init__(
            self,
            resources: List[Proxy],
            storage: OkvedCompaniesStorage,
            base_url: str,
            n_pages: int,
            okved: str,
            cooldown: int = 5,
            only_main_okved: bool = True
    ):
        self.storage = storage
        self.base_url = base_url
        self.task_retriever = OkvedCompaniesTaskRetriever(self.base_url, n_pages, storage, okved)
        self.workers = [
            OkvedCompaniesWorker(
                self.storage, resource, str(uuid4()), cooldown=cooldown, only_main_okved=only_main_okved
            ) for resource in resources
        ]

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
    save_pth = "data/okved_companies/okved_259400_companies_not_only_main_okved.json"
    already_parsed = read_results_from_json(save_pth)

    set_up_logging()
    storage = OkvedCompaniesStorage(save_pth, already_parsed)
    proxies = read_proxies("resources/proxies.json")

    crawler = OkvedCompaniesCrawler(
        proxies,
        storage,
        "https://www.rusprofile.ru/codes/259400",
        394,
        "25.94",
        cooldown=20,
        only_main_okved=False
    )
    event_loop = get_event_loop()
    event_loop.run_until_complete(crawler.crawl())
    results = storage.get_results()
    logger.info(f"Сохраняем данные по {len(results)} страницам")
    save_results_as_json(results, save_pth)
