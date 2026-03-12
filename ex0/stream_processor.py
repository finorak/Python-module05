from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, data: Any) -> None:
        super().__init__()
        self.data = data

    @abstractmethod
    def process(self, data: Any) -> str:
        ...

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def format_output(self) -> str:
        ...


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        ...

    def validate(self, data: Any) -> bool:
        ...

    def format_ouput(self, result: str) -> str:
        ...


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        ...

    def validate(self, data: Any) -> bool:
        ...

    def format_ouput(self, result: str) -> str:
        ...


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        ...

    def validate(self, data: Any) -> bool:
        ...

    def format_ouput(self, result: str) -> str:
        ...


def main() -> None:
    numeric = NumericProcessor


if __name__ == "__main__":
    main()
