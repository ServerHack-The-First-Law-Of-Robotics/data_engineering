from aiohttp import ClientSession
from logging import getLogger
from os.path import join

from base.worker import Worker
from base.data_objects import OGRNTask
from .data_objects import ContactsResult

logger = getLogger(__name__)


class ContactsWorker(Worker):
    def __init__(self, *args, base_url: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    async def complete_task(self, session: ClientSession, task: OGRNTask) -> ContactsResult:
        ogrn = task.ogrn

        resp = None
        try:
            async with self.get_response(
                    session,
                    join(self.base_url, ogrn)
            ) as resp:
                company_info = await resp.text()
                if resp.status != 200:
                    raise ValueError(f"Некорректный ответ от {self.base_url}. {resp.status=}, {company_info=}")
                # TODO: parse phones and emails
                if "Телефон:" in company_info:
                    phone_start_idx = company_info.index("Телефон:")
                    phones_info = company_info[phone_start_idx:]
                    phone_start = phones_info.index("+7")
                    phone_symbols_len = 18
                    phones = [phones_info[phone_start: phone_start + phone_symbols_len]]
                else:
                    phones = []
                print("phone", phones)

                if "E-mail:" in company_info:
                    email_start_idx = company_info.index("E-mail:")
                    email_info = company_info[email_start_idx:]
                    email_start = email_info.index('href="mailto:') + len('href="mailto:')
                    email_info = email_info[email_start:]
                    email_end = email_info.index('"')
                    emails = [email_info[:email_end]]
                else:
                    emails = []
                print("email", emails)

            return ContactsResult(
                phones=phones,
                emails=emails,
                is_error=False
            )

        except Exception:
            logger.error("Произошла ошибка при скачивании документа из ЕГРЮЛ", exc_info=True)
            return ContactsResult(
                pdf_path=None,
                is_error=True,
                status_code=-1 if resp is None else resp.status
            )
