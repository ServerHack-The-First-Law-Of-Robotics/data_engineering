from aiohttp import ClientSession
from logging import getLogger
from os.path import join

from base.worker import Worker
from .data_objects import EgrulTask, EgrulResult

logger = getLogger(__name__)


class EgrulWorker(Worker):
    def __init__(
            self,
            *args,
            base_pdf_path: str,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.base_pdf_path = base_pdf_path

    async def complete_task(self, session: ClientSession, task: EgrulTask) -> EgrulResult:
        inn = task.inn
        resp = None

        pdf_path = join(self.base_pdf_path, f"egrul_{inn}.pdf")
        try:
            # TODO: починить прокси
            async with session.post(
                'https://egrul.nalog.ru/',
                data={'query': inn},
                # proxy=self.resource
            ) as resp:
                inn_info = await resp.json()
                inn_access_key = inn_info["t"]

            async with session.get(
                f'https://egrul.nalog.ru/search-result/{inn_access_key}',
                # proxy=self.resource
            ) as resp:
                search_result_resp = await resp.json()
                file_access_code = search_result_resp['rows'][0]['t']
            # тут выполняются 2 запроса, хз, зачем они нужны, но без них не работает. Спрашивайте у ГК
            async with session.get(
                f'https://egrul.nalog.ru/vyp-request/{file_access_code}',
                # proxy=self.resource
            ) as resp:
                ...

            async with session.get(
                f'https://egrul.nalog.ru/vyp-status/{file_access_code}',
                # proxy=self.resource
            ) as resp:
                ...

            async with session.get(
                f'https://egrul.nalog.ru/vyp-download/{file_access_code}',
                # proxy=self.resource
            ) as resp:
                with open(pdf_path, 'wb') as pdf_file:
                    async for data in resp.content.iter_chunked(1024):
                        pdf_file.write(data)

            return EgrulResult(
                pdf_path=pdf_path,
                is_error=resp.status != 200,
                status_code=resp.status
            )

        except Exception:
            logger.error("Произошла ошибка при скачивании документа из ЕГРЮЛ", exc_info=True)
            return EgrulResult(
                pdf_path=None,
                is_error=True,
                status_code=None if resp is None else resp.status
            )
