from typing import Dict
from logging import getLogger

from .data_objects import OkvedCompaniesResult
from .data_saving import save_results_as_json
from base.storage import Storage

logger = getLogger(__name__)


class OkvedCompaniesStorage(Storage):
    def __init__(
            self,
            *args,
            save_pth: str,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.save_pth = save_pth

    def dump_long_term(self, results: Dict[str, OkvedCompaniesResult]):
        # использую функцию, тк считаю, что записывать данные можно и вне Storage. Например, если хотим смержить
        #  несколько файлов
        save_results_as_json(results, self.save_pth)
