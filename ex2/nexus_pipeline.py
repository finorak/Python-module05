from abc import ABC
from typing import Any


class ProcessingPipeline(ABC):
    def __init__(self) -> None:
        super().__init__()


class InputStage(ProcessingPipeline):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> Any:
        ...


class TransformStage(ProcessingPipeline):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> Any:
        ...


class OutputStage(ProcessingPipeline):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data: Any) -> Any:
        ...


class JSONAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__()
        ...


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__()
        ...


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__()
        pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()
