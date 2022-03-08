from logging import getLogger
from asyncio import get_event_loop
from pandas import read_csv
from os import makedirs

from utils import set_up_logging, read_proxies
from base.crawler import Crawler
from egrul.task_retriever import EgrulTaskRetriever
from egrul.worker import EgrulWorker
from egrul.storage import EgrulStorage

logger = getLogger(__name__)


if __name__ == "__main__":
    # рабочая директория должна быть data_engineering - это можно настроить в edit configuration в pycharm
    set_up_logging()
    proxies = read_proxies("resources/proxy6_net.txt")

    makedirs("data/egrul", exist_ok=True)
    makedirs("data/egrul_pdf", exist_ok=True)

    storage = EgrulStorage(parsed_inns_list_path="data/egrul/inns.json")

    parsed_inns = read_csv("data/okved_companies/okved_companies_data.csv", usecols=["inn"])
    parsed_inns = list(parsed_inns["inn"])

    task_retriever = EgrulTaskRetriever(
        storage,
        inns=parsed_inns
    )

    workers = []

    for proxy in proxies:
        worker = EgrulWorker(
            storage,
            task_retriever,
            cooldown=60,
            resource=proxy,
            proxy_login_and_password=("Yzhnwe", "ff7E2B"),
            base_pdf_path="data/egrul_pdf/",
            use_proxy=True,
            stop_on_error=False,
            sleep_after_fail=120
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
