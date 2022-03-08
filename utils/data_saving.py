from typing import Dict, Type
from json import dump, load
from logging import getLogger
from os.path import isfile

from base.data_objects import Result

logger = getLogger(__name__)


def read_results_from_json(
        pth: str,
        result_class: Type[Result]
) -> Dict[str, Result]:
    if not isfile(pth):
        return {}

    with open(pth) as f:
        results = load(f)

    encoded_data = {}
    for key, page in results.items():
        page_data_obj = result_class(**page)
        encoded_data[key] = page_data_obj
    return encoded_data


def save_results_as_json(
        results: Dict[str, Result],
        pth: str
):
    json_converted = {}
    for key, page in results.items():
        page_converted = page.dict()
        json_converted[key] = page_converted

    with open(pth, "w") as f:
        dump(json_converted, f)
