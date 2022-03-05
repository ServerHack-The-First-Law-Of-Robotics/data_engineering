from typing import Dict, Callable

from base_objects import Proxy


class OkvedCompaniesWorker:
    def __init__(
            self,
            resource: Proxy,
            callbacks: Dict[str, Callable]
    ):
        ...
