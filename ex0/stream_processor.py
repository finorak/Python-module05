from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.data = None

    @abstractmethod
    def process(self, data: Any) -> str:
        ...

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def format_output(self, result: str) -> str:
        ...

    def ft_len(self, data: Any) -> int:
        counter = 0
        for _ in data:
            counter += 1
        return counter


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f"Processig data: {data}")
        if self.validate(data):
            self.data = data
            print("Validation: Numeric data verified")
            return "False"
        print("Validation: None Numeric Data")
        return "True"

    def validate(self, data: Any) -> bool:
        try:
            self.data_len = self.ft_len(data)
            for index in range(self.data_len):
                _ = data[index] + 1
            return True
        except (TypeError, IndexError):
            pass
        try:
            _ = data + 1
            return True
        except Exception as e:
            print("Error:", e)
        return False

    def format_ouput(self, result: str) -> str:
        ...


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f"Processig data: {data}")
        if not self.validate(data):
            print("Error")
            return "error"
        self.data = data
        print("Success")
        return "Success"

    def validate(self, data: Any) -> bool:
        try:
            self.data_len = self.ft_len(data)
            for index in range(self.data_len):
                _ = data[index] + ""
            return True
        except (TypeError, IndexError):
            pass
        try:
            _ = data + ""
            return True
        except Exception as e:
            print("error:", e)
        return False

    def format_output(self, result: str) -> str:
        res = ""
        str_len = self.ft_len(self.data)
        word_count = self.word_count(self.data, str_len)
        res = f"Processed text: {str_len} characters"
        res += f"{word_count} words"
        print("Output:", res)
        return res

    def word_count(self, string: str, str_len: int) -> int:
        counter = 0
        index = 0
        sep = ("\t", "\r", "\f", " ", "\v", "\n")
        while index < str_len:
            char = string[index]
            count = False
            while char in sep and index < str_len:
                char = string[index]
                index += 1
            while char not in sep and index < str_len:
                char = string[index]
                index += 1
                count = True
            if count:
                counter += 1
        return counter


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        ...

    def validate(self, data: Any) -> bool:
        ...

    def format_ouput(self, result: str) -> str:
        ...


def main() -> None:
    text = TextProcessor()
    text.process("Hello world 42")


if __name__ == "__main__":
    main()
