from abc import ABC, abstractmethod
from typing import Any, Self


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()

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
    def __init__(self) -> None:
        super().__init__()
        self.data: Any = None
        self.is_valid: bool = True
        self.is_digit: bool = False

    def process(self, data: Any) -> str:
        print(f"Processig data: {data}")
        self.data = data
        if not self.validate(data):
            print("Validation: Data is not numeric")
            self.is_valid = False
            return "False"
        print("Validation: Data is numeric")
        return "True"

    def validate(self, data: Any) -> bool:
        data_el = 0
        first_el = None
        try:
            for el in data:
                if first_el is None:
                    first_el = el
                data_el += el
            self.is_digit = False
            return True
        except Exception:
            pass
        try:
            _ = data + 1
            self.is_digit = True
            return True
        except Exception:
            pass
        return False

    def format_output(self: Self, result: str) -> str:
        if not self.is_valid:
            print("Data provided is not a numeric")
            return ""
        res = ""
        data_len = 1
        data_sum = self.data
        average = self.data
        if not self.is_digit:
            data_len = self.ft_len(self.data)
            data_sum = self.ft_sum(self.data)
            average = self.get_average(self.data)
        res = f"Processed {data_len} numeric values, "
        res += f"sum = {data_sum}, avg = {average}"
        print("Output:", res)
        return result

    def ft_sum(self, lst: list[int] | None) -> int:
        count = 0
        if lst is None:
            return 0
        for el in lst:
            count += el
        return count

    def get_average(self, lst: Any) -> float:
        if self.is_digit:
            return lst
        lst_sum = self.ft_sum(lst)
        return lst_sum / self.ft_len(lst)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.is_valid = True

    def process(self, data: Any) -> str:
        print(f"Processig data: \"{data}\"")
        self.data = data
        if not self.validate(data):
            print("Validiation: Data not a text")
            self.is_valid = False
            return "Error"
        self.data = data
        print("Validiation: Text data verified")
        return "Success"

    def validate(self, data: Any) -> bool:
        data_el = ""
        try:
            self.data_len = self.ft_len(data)
            for index in range(self.data_len):
                data_el += data[index]
            return data_el == data
        except Exception:
            pass
        try:
            _ = data + ""
            return True
        except Exception:
            pass
        return False

    def format_output(self, result: str) -> str:
        if not self.is_valid:
            print("Data provided is not a string")
            return ""
        res = ""
        str_len = self.ft_len(self.data)
        word_count = self.word_count(self.data, str_len)
        res = f"Processed text: {str_len} characters "
        res += f"{word_count} words"
        print("Output:", res)
        return result

    def word_count(self, string: str | None, str_len: int) -> int:
        counter: int = 0
        index: int = 0
        sep: tuple = ("\t", "\r", "\f", " ", "\v", "\n")
        if string is None:
            return -1
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
    def __init__(self) -> None:
        super().__init__()
        self.data: Any = None
        self.is_valid: bool = True
        self.level: str | None = None
        self.status: str | None = None

    def process(self, data: Any) -> str:
        print(f"Processing data: \"{data}\"")
        self.data = data
        if not self.validate(data):
            self.is_valid = False
            print("Validation: Data is not a Log")
            return "error"
        print("Validation: Log entry verified")
        return "success"

    def validate(self, data: Any) -> bool:
        text_processor = TextProcessor()
        if not text_processor.validate(data):
            return False
        separete = self.separate(data)
        if separete is None:
            return False
        self.level, self.status = separete
        if self.level == "" or self.status == "":
            return False
        return True

    def format_output(self, result: str) -> str:
        if not self.is_valid:
            print("No level detected")
            return result
        print(f"Output: [ALERT] {self.level} level", end=" ")
        print(f"detected: {self.status}")
        return result

    def separate(self, data: Any) -> list[str | None] | None:
        if not self.is_valid:
            return
        error_level = ""
        status = ""
        data_len = self.ft_len(data)
        index = 0
        while index < data_len:
            if data[index] == ":":
                status = self.get_status(data, index + 1)
                break
            error_level += data[index]
            index += 1
        return [error_level, status]

    def get_status(self, data: Any, index: int) -> str | None:
        if not self.is_valid:
            return
        status = ""
        data_len = self.ft_len(data)
        char = data[index]
        while char == " " and index < data_len:
            char = data[index]
            index += 1
        if data[index] != " " and data[index - 1] != ":":
            index -= 1
        while index < data_len:
            status += data[index]
            index += 1
        return status


def main() -> None:
    data = "ERROR:System timeout"
    log = LogProcessor()
    log.process(data)
    log.format_output("None")


if __name__ == "__main__":
    main()
