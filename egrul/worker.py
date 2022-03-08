from aiohttp import ClientSession
from asyncio import sleep
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
            async with self.get_response(
                    session,
                    'https://egrul.nalog.ru/',
                    kwargs={"data": {'query': inn}},
                    method="post"
            ) as resp:
                inn_info = await resp.json()
                if resp.status != 200:
                    raise ValueError(f"Некорректный ответ от egrul.nalog.ru. {resp.status=}, {inn_info=}")
                inn_access_key = inn_info["t"]

            async with self.get_response(
                    session,
                    f'https://egrul.nalog.ru/search-result/{inn_access_key}',
            ) as resp:
                search_result_resp = await resp.json()
                file_access_code = search_result_resp['rows'][0]['t']
            # гвоорит серверу "дядя, начни готовить для меня вот этот файл"
            async with self.get_response(
                session,
                f'https://egrul.nalog.ru/vyp-request/{file_access_code}'
            ) as resp:
                ...
            # проверяет, готов ли файл. Статус может быть "wait" и "ready"
            max_tries = 3
            time_to_sleep = 1
            await sleep(0.5)
            for _ in range(max_tries):
                async with self.get_response(
                    session,
                    f'https://egrul.nalog.ru/vyp-status/{file_access_code}',
                ) as resp:
                    data = await resp.json()
                    if data["status"] == "ready":
                        break
                    else:
                        logger.debug(f"Спим {time_to_sleep} секунд")
                        await sleep(time_to_sleep)
                        time_to_sleep = 60
            else:
                logger.error(f"После {max_tries} циклов ожидания, файл для ИНН {inn=} нам не доступен.")
                raise RuntimeError()

            async with self.get_response(
                    session,
                    f'https://egrul.nalog.ru/vyp-download/{file_access_code}',
            ) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Статус response для загрузки не 200: {resp.status=}")
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
                status_code=-1 if resp is None else resp.status
            )
