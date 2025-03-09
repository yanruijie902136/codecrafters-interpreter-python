from typing import Any


class ReturnException(Exception):
    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value
