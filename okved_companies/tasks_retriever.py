from os.path import join

from base.task_retriever import TaskRetriever
from .data_objects import OkvedCompaniesTask


class OkvedCompaniesTaskRetriever(TaskRetriever):
    def __init__(
            self,
            *args,
            base_url: str,
            n_pages: int,
            okved: str,
            **kwargs
    ):
        self.n_pages = n_pages
        self.okved = okved
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def create_tasks(self):
        tasks = []
        for page_idx in range(1, self.n_pages + 1):
            task_key = str(page_idx)

            if page_idx == 1:
                url = self.base_url
            else:
                url = join(self.base_url, str(page_idx))

            task = OkvedCompaniesTask(
                task_key=task_key,
                url=url,
                okved=self.okved
            )
            tasks.append(task)
        return tasks
