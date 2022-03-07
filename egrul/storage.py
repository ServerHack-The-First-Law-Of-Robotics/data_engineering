from typing import Dict
from json import dump, load
from os.path import isfile

from base.storage import Storage
from .data_objects import EgrulResult


class EgrulStorage(Storage):
    def __init__(
            self,
            *args,
            parsed_inns_list_path: str,
            **kwargs
    ):
        self.parsed_inns_list_path = parsed_inns_list_path
        super().__init__(*args, **kwargs)

    def dump_long_term(self):
        encoded = {}
        for key, val in self.results.items():
            encoded[key] = val.json()

        with open(self.parsed_inns_list_path, "w") as f:
            dump(encoded, f)

    def load_already_existing(self) -> Dict[str, EgrulResult]:
        if not isfile(self.parsed_inns_list_path):
            return {}

        with open(self.parsed_inns_list_path) as f:
            raw = load(f)

            decoded = {}
            for key, val in raw.items():
                decoded[key] = EgrulResult(**val)
        return decoded
