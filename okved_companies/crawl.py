from logging import getLogger
from asyncio import get_event_loop

from utils import set_up_logging, read_proxies
from base.crawler import Crawler
from okved_companies.tasks_retriever import OkvedCompaniesTaskRetriever
from okved_companies.worker import OkvedCompaniesWorker
from okved_companies.storage import JsonStorage

logger = getLogger(__name__)


if __name__ == "__main__":
    set_up_logging()

    save_pth = "data/okved_companies/okved_221900_companies_not_only_main_okved.json"

    storage = JsonStorage(save_pth=save_pth)
    proxies = read_proxies("resources/proxy.txt")
    print("proxies", proxies)

    task_retriever = OkvedCompaniesTaskRetriever(
        storage,
        base_url="https://www.rusprofile.ru/codes/221900",
        n_pages=288,
        okved="22.19"
    )
    workers = []

    for resource in proxies:
        worker = OkvedCompaniesWorker(
            storage,
            task_retriever,
            resource,
            cooldown=20,
            only_main_okved=False,
            use_proxy=True
        )
        workers.append(worker)

    crawler = Crawler(
        workers
    )

    event_loop = get_event_loop()
    event_loop.run_until_complete(crawler.crawl())
    results = storage.get_results()
    logger.info(f"Сохраняем данные по {len(results)} страницам")
    storage.dump_long_term()
