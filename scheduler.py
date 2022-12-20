from utils import FNF
from typing import Any, List
from threading import Thread


class Scheduler:
    def __init__(self, fnf: FNF, paralel=True) -> None:
        self.fnf = fnf
        self.paralel = paralel

    def run(self, *args, **kwargs):
        if self.paralel:
            for cls in self.fnf.classes:
                threads = [
                    Thread(target=task.run, name=str(task), args=args, kwargs=kwargs)
                    for task in cls
                ]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()
        else:
            for cls in self.fnf.classes:
                for task in cls:
                    task.run(*args, **kwargs)
