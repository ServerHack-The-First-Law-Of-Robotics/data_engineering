from typing import List
from logging import getLogger

from base_objects import Proxy
from utils.set_up_logging import set_up_logging
from okved_companies.tasks import OkvedCompaniesTasks
from okved_companies.worker import OkvedCompaniesWorker

logger = getLogger(__name__)


class OkvedCompaniesCrawler:
    def __init__(
            self,
            resources: List[Proxy],
            storage,
            base_url: str,
            n_pages: int
    ):
        self.callbacks = {
            "stopping_resource_exhausted": self._worker_callback_resource_exhausted,
            "stopping_no_tasks": self._worker_callback_no_tasks
        }

        self.storage = storage
        self.base_url = base_url
        self.tasks = OkvedCompaniesTasks(self.base_url, n_pages)
        self.workers = [OkvedCompaniesWorker(resource, self.callbacks) for resource in resources]

    def crawl(self):
        # TODO
        logger.info(f"Начинаем собирать данные из {self.base_url}")
        ...

    def _worker_callback_resource_exhausted(self):
        """Коллбэк, если worker больше не может работать, тк ресурс выработан (например, прокси заблочили)"""
        ...

    def _worker_callback_no_tasks(self):
        """Коллбэк, если worker остановился, тк не осталось задач"""
        ...


if __name__ == "__main__":
    set_up_logging()
    crawler = OkvedCompaniesCrawler(
        [],
        None,
        "https://www.rusprofile.ru/codes/220000",
        353
    )
    crawler.crawl()
