from uuid import uuid4
from logging import getLogger
from asyncio import get_event_loop

from utils import set_up_logging, read_proxies
from base.crawler import Crawler
from okved_companies.tasks_retriever import OkvedCompaniesTaskRetriever
from okved_companies.worker import OkvedCompaniesWorker
from okved_companies.storage import OkvedCompaniesStorage
from okved_companies.data_saving import save_results_as_json, read_results_from_json

logger = getLogger(__name__)


if __name__ == "__main__":
    set_up_logging()

    save_pth = "data/okved_companies/okved_259400_companies_not_only_main_okved.json"
    already_parsed = read_results_from_json(save_pth)

    storage = OkvedCompaniesStorage(already_parsed, save_pth=save_pth)
    proxies = read_proxies("resources/proxies.json")

    task_retriever = OkvedCompaniesTaskRetriever(
        storage,
        base_url="https://www.rusprofile.ru/codes/259400",
        n_pages=394,
        okved="25.94"
    )
    workers = []

    for resource in proxies:
        worker = OkvedCompaniesWorker(
            storage,
            task_retriever,
            resource,
            str(uuid4()),
            cooldown=20,
            only_main_okved=True
        )
        workers.append(worker)

    crawler = Crawler(
        workers
    )

    event_loop = get_event_loop()
    event_loop.run_until_complete(crawler.crawl())
    results = storage.get_results()
    logger.info(f"Сохраняем данные по {len(results)} страницам")
    save_results_as_json(results, save_pth)