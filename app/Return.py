import typing


class Return(Exception):
    def __init__(self, value: typing.Any):
        super().__init__()
        self.value = value
