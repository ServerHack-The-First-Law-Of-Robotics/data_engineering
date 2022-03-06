from typing import List
from logging import getLogger
from aiohttp import ClientSession
from asyncio import sleep
from bs4 import BeautifulSoup

from .data_objects import OkvedCompaniesTask, OkvedCompaniesResult, RusprofileCompanyData
from .tasks_retriever import OkvedCompaniesTaskRetriever
from .storage import OkvedCompaniesStorage
from base_objects import Proxy

logger = getLogger(__name__)


class OkvedCompaniesWorker:
    def __init__(
            self,
            storage: OkvedCompaniesStorage,
            resource: Proxy,
            worker_id: str,
            cooldown: int = 10,
            stop_on_error: bool = True,
            only_main_okved: bool = False
    ):
        self.storage = storage
        self.resource = resource
        self.id = worker_id
        self.cooldown = cooldown
        self.stop_on_error = stop_on_error
        self.cookies = {
            # используется, чтобы получать даже те компании, у которых нужный ОКВЭД - не основной. Мы делаем это, чтобы
            #  получить все компании, которые могут заниматься нужным нам производством
        }
        if not only_main_okved:
            self.cookies["okved_all"] = "yes"

    async def run(self, task_retriever: OkvedCompaniesTaskRetriever):
        async with ClientSession(cookies=self.cookies) as session:
            while task_retriever.have_task():

                task = task_retriever.next_task()
                logger.info(f"Обрабатываем {task=}")
                result = await self.complete_task(session, task)
                self.storage.save_result(result, task)

                if result.is_error and self.stop_on_error:
                    logger.info(f"Произошла ошбика в worker {self.id=}. {task=}, {result=}")
                    return
                await sleep(self.cooldown)

    async def complete_task(self, session: ClientSession, task: OkvedCompaniesTask) -> OkvedCompaniesResult:
        async with session.get(
                task.url, proxy=self.resource
        ) as resp:
            text = await resp.text()
            if resp.status != 200:
                result = OkvedCompaniesResult(
                    is_error=True,
                    raw_response=text,
                    okved=task.okved,
                    status_code=resp.status
                )
                return result

            try:
                html = BeautifulSoup(text, "html.parser")
                companies = html.findAll('div', class_='company-item')
                companies_data: List[RusprofileCompanyData] = []
                for comp in companies:
                    status = comp.find('div', class_='company-item-status')
                    if status is not None:
                        continue

                    info = comp.findAll('div', class_='company-item-info')[1].findAll('dl')
                    inn = info[0].find('dd').contents[0].strip()
                    if len(info) > 1:
                        ogrn = info[1].find('dd').contents[0].strip()
                    else:
                        ogrn = None

                    company_data = RusprofileCompanyData(
                        inn=inn,
                        ogrn=ogrn
                    )
                    companies_data.append(company_data)

                result = OkvedCompaniesResult(
                    is_error=False,
                    raw_response=text,
                    companies_list=companies_data,
                    okved=task.okved
                )
                return result

            except Exception:
                logger.error("Произошла ошибка при парсинге документа OkvedCompanies."
                             f"Полный текст документа: {text}", exc_info=True)
                return OkvedCompaniesResult(
                    is_error=True,
                    raw_response=text,
                    okved=task.okved
                )
