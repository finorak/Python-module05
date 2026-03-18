from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, Dict


class DataStream(ABC):
    def __init__(self, stream_id: Optional[str | None] = None,
                 stream_type: Optional[str | None] = None) -> None:
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = stream_type
        self.data_batch: Any = None
        self.is_valid = True
        print(f"Sream ID: {self.stream_id}", end=", ")
        print(f"Type: {self.stream_type}")

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        ...

    @abstractmethod
    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        filtered_data = []
        try:
            for el in data_batch:
                item = f"{el}"
                if critera:
                    item += f'{critera}'
                else:
                    item += ":"
                item += f"{data_batch[el]}"
                filtered_data += [item]
        except Exception:
            raise Exception()
        return filtered_data

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
        self.is_valid = True
        self.stats: dict | None = None

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data_batch = data_batch
        print(f"Processing sensor batch: {self.data_batch}")
        if not self.data_is_valid(data_batch):
            self.is_valid = False
            return "Failure"
        return "success"

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        filtered_data = []
        try:
            for el in data_batch:
                item = f"{el}"
                if critera:
                    item += f'{critera}'
                else:
                    item += ":"
                item += f"{data_batch[el]}"
                filtered_data += [item]
        except Exception:
            return ["error"]
        return filtered_data

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        try:
            stats = dict()
            if not self.is_valid:
                print("No stats available, run with the correct data...")
                return stats
            for el in self.data_batch:
                separate = self.separate(el)
                if separate is None:
                    continue
                item, value = separate
                if not value or not item:
                    continue
                stats.update({item: value})
            self.stats = stats
            print("Sensor analysys", end=": ")
            print(f"{self.ft_len(self.data_batch)}", end=" ")
            print(f"readings processed, avg temp: {self.stats['temp']}°")
            return stats
        except Exception:
            raise Exception()

    def data_is_valid(self, data_batch: List[str]) -> bool:
        valid = False
        try:
            for el in data_batch:
                separate = self.separate(el)
                if separate is None:
                    return False
                item, value = separate
                if not value or not item:
                    return False
                if ":" in value:
                    return False
                if item == "temp":
                    valid = True
        except Exception:
            return False
        if not valid:
            return False
        return True


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        print("Initializing Transaction Stream...")
        self.stream_type = "Financial Data"
        super().__init__(stream_id, self.stream_type)
        self.stream_id = stream_id
        self.filtered_data = None

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data_batch = data_batch
        print(f"Processing transaction batch: {self.data_batch}")
        if not self.data_is_valid(data_batch):
            self.is_valid = False
            return "Failure"
        return "Success"

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        filtered_data = []
        try:
            for el in data_batch:
                item = f"{el}"
                if critera:
                    item += f'{critera}'
                else:
                    item += ":"
                item += f"{data_batch[el]}"
                filtered_data += [item]
        except Exception:
            return ["error"]
        return filtered_data

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        try:
            stats = {}
            if not self.is_valid:
                print("Couldn't process data so there is no", end=" ")
                print("stats.... Run with correct data")
                return stats
            for el in self.data_batch:
                separate = self.separate(el)
                if not separate:
                    continue
                item, value = separate
                if value is None:
                    raise ValueError()
                value = self.ft_int(value)
                if item in stats:
                    stats[item] += value
                else:
                    stats[item] = value
            net_flow = stats['buy'] - stats['sell']
            profit = "+" if net_flow > 0 else ""
            print("Transaction analysis", end=": ")
            print(f"{self.ft_len(self.data_batch)} operations", end=", ")
            print(f"net flow: {profit}{net_flow}")
            return stats
        except Exception:
            raise Exception()

    def data_is_valid(self, data_batch: List[Any]) -> bool:
        bought = False
        sold = False
        try:
            for el in data_batch:
                separate = self.separate(el)
                if separate is None:
                    return False
                item, value = separate
                if not value or not item:
                    return False
                if ":" in value or self.ft_int(value) < 0:
                    return False
                if item == "buy":
                    bought = True
                elif item == "sell":
                    sold = True
        except Exception:
            return False
        return bought and sold

    def ft_int(self, num: str | None) -> int:
        if num is None:
            raise ValueError()
        value = 0
        digits = {
                "0": 0,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                }
        for el in num:
            if el not in digits:
                raise ValueError()
            value = (value * 10) + (digits[el])
        return value


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        print("Initializing Event Stream...")
        self.stream_type = "System Events"
        super().__init__(stream_id, self.stream_type)
        self.stream_id = stream_id
        self.levels = {"success", "error", "logout",
                       "login"}
        self.is_valid = True

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data_batch = data_batch
        print(f"Processing event batch: {self.data_batch}")
        if not self.data_is_valid(data_batch):
            self.is_valid = False
            return "Failure"
        return "Success"

    def filter_data(self, data_batch: List[Any],
                    critera: Optional[str] = None) -> List[Any]:
        logs = {}
        filtered_data = []
        try:
            for el in data_batch:
                if el in logs:
                    continue
                logs[el] = self.ft_count(data_batch, el)
            for key, value in logs:
                filtered_data += [f"{key}:{value}"]
            return filtered_data
        except Exception:
            raise Exception()

    def ft_count(self, data_batch: List[str], log: str) -> int:
        counter = 0
        for el in data_batch:
            if el == log:
                counter += 1
        return counter

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        try:
            stats = dict()
            error_count = 0
            if not self.is_valid:
                print("Not stats available due to corruped data")
                return stats
            for el in self.data_batch:
                if el == "error":
                    error_count += 1
                stats[el] = error_count
            print("Event analysis", end=": ")
            print(f"{self.ft_len(self.data_batch)} events", end=", ")
            print(f"{error_count} error detected")
            return stats
        except Exception:
            raise Exception()

    def data_is_valid(self, data_batch: List[Any]) -> bool:
        try:
            for el in data_batch:
                if el not in self.levels:
                    return False
            return True
        except Exception:
            return False


class StreamProcessor:
    def __init__(self) -> None:
        self.streams: list[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams += [stream]

    def process_all(self, data: List[Any]):
        for stream in self.streams:
            print("-", stream.stream_id, "data", end=" ")
            stream.process_batch(data)
            stream.get_stats()
            print()


def polymorphic_demonstration() -> None:
    try:
        data = ["temp:3", "humidity:65", "pressure:1013"]
        stream = StreamProcessor()
        sensor = SensorStream("SENSOR_001")
        transaction = TransactionStream("TRANS_001")
        event = EventStream("EVENT_001")
        stream.add_stream(sensor)
        stream.add_stream(transaction)
        stream.add_stream(event)
        stream.process_all(data)
    except Exception as e:
        print(e)


def main() -> None:
    try:
        print()
        stream_id = "SENSOR_001"
        data = ["temp:22.5", "humidity:65", "pressure:1013"]
        sensor = SensorStream(stream_id)
        sensor.process_batch(data)
        sensor.get_stats()
        print()
        stream_id = "TRANS_001"
        data = ["buy:100", "sell:150", "buy:75"]
        transaction = TransactionStream(stream_id)
        transaction.process_batch(data)
        transaction.get_stats()
        print()
        stream_id = "EVENT_001"
        data = ["login", "error", "logout"]
        event = EventStream(stream_id)
        event.process_batch(data)
        event.get_stats()
        print()
        polymorphic_demonstration()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    main()
