from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, Dict


class DataStream(ABC):
    def __init__(self, stream_id: Optional[str | None] = None,
                 stream_type: Optional[str | None] = None) -> None:
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = stream_type
        self.data_batch = None
        print(f"Sream ID: {self.stream_id}", end=", ")
        print(f"Type: {self.stream_type}")

    @abstractmethod
    def process_data(self, data_batch: List[Any]) -> str:
        ...

    @abstractmethod
    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        ...

    @abstractmethod
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...

    def ft_len(self, data: Any) -> int:
        counter = 0
        for _ in data:
            counter += 1
        return counter

    def separate(self, data: Any) -> list[str | None] | None:
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


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        print("Initializing Sensor Stream...")
        self.stream_type = "Environmental Data"
        super().__init__(stream_id, self.stream_type)
        self.stream_id = stream_id

    def process_data(self, data_batch: List[Any]) -> str:
        filtered_data = self.filter_data(data_batch, ":")
        print(f"Processing sensor batch: {filtered_data}")
        return "success"

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        filtered_data = ''
        for data in data_batch:
            ...
        return [filtered_data]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...

    def is_valid(self, data_batch: List[Any]) -> bool:
        return True


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        print("Initializing Transaction Stream...")
        self.stream_type = "Financial Data"
        super().__init__(stream_id, self.stream_type)
        self.stream_id = stream_id

    def process_data(self, data_batch: List[Any]) -> str:
        ...

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        ...

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        print("Initializing Event Stream...")
        self.stream_type = "System Events"
        super().__init__(stream_id, self.stream_type)
        self.stream_id = stream_id

    def process_data(self, data_batch: List[Any]) -> str:
        ...

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        ...

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        ...


class StreamProcessor:
    def __init__(self) -> None:
        pass


def main() -> None:
    stream_id = "SENSOR_001"
    data = [{"temp": 22.5, "humidity": 65, "pressure": 1013}]
    sensor = SensorStream(stream_id)
    sensor.process_data(data)
    stats = sensor.get_stats()
    print(stats)


if __name__ == "__main__":
    main()
