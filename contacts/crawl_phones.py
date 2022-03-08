from logging import getLogger
from asyncio import get_event_loop
from pandas import read_csv

from utils import set_up_logging, read_proxies
from base.crawler import Crawler
from base.task_retriever import OGRNTaskRetriever
from contacts.worker import ContactsWorker
from contacts.data_objects import ContactsResult
from base.storage import JsonStorage

logger = getLogger(__name__)


if __name__ == "__main__":
    set_up_logging()

    save_pth = "data/phones/phones_all_companies.json"

    storage = JsonStorage(save_pth=save_pth, result_class=ContactsResult)
    proxies = read_proxies("resources/proxy.txt")
    print("proxies", proxies)

    # # TODO: убрать ограничение
    # proxies = proxies[:1]

    ogrns = list(read_csv("data/okved_companies/okved_companies_data.csv", usecols=["ogrn"])["ogrn"])
    ogrns += list(read_csv("data/okved_companies/okved_companies_data_sber.csv", usecols=["ogrn"])["ogrn"])

    task_retriever = OGRNTaskRetriever(
        storage,
        ogrns=ogrns
    )
    workers = []

    for resource in proxies:
        worker = ContactsWorker(
            storage,
            task_retriever,
            resource,
            cooldown=10,
            use_proxy=True,
            base_url="https://vbankcenter.ru/contragent/"
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
