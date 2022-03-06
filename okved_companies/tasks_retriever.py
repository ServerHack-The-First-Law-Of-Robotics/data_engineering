from typing import List
from os.path import join

from .storage import OkvedCompaniesStorage
from .data_objects import OkvedCompaniesTask


class OkvedCompaniesTaskRetriever:
    def __init__(
            self,
            base_url: str,
            n_pages: int,
            storage: OkvedCompaniesStorage,
            okved: str
    ):
        self.tasks: List[OkvedCompaniesTask] = []

        for page_idx in range(1, n_pages + 1):
            task_key = str(page_idx)
            if storage.check_result_exists(task_key):
                continue

            if page_idx == 1:
                url = base_url
            else:
                url = join(base_url, str(page_idx))

            task = OkvedCompaniesTask(
                task_key=task_key,
                url=url,
                okved=okved
            )
            self.tasks.append(task)

    def have_task(self) -> bool:
        return len(self.tasks) > 0

    def next_task(self) -> OkvedCompaniesTask:
        return self.tasks.pop(0)
