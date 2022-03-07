from typing import Dict
from logging import getLogger

from .data_objects import OkvedCompaniesResult
from .data_saving import save_results_as_json, read_results_from_json
from base.storage import Storage

logger = getLogger(__name__)


class OkvedCompaniesStorage(Storage):
    def __init__(
            self,
            *args,
            save_pth: str,
            **kwargs
    ):
        self.save_pth = save_pth
        super().__init__(*args, **kwargs)

    def dump_long_term(self):
        # использую функцию, тк считаю, что записывать данные можно и вне Storage. Например, если хотим смержить
        #  несколько файлов
        save_results_as_json(self.results, self.save_pth)

    def load_already_existing(self) -> Dict[str, OkvedCompaniesResult]:
        return read_results_from_json(self.save_pth)
