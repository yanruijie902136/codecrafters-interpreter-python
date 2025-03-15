import dataclasses


@dataclasses.dataclass(frozen=True)
class LoxClass:
    name: str

    def __str__(self) -> str:
        return self.name
