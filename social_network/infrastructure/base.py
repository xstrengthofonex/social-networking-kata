from abc import ABC, abstractmethod


class Response(object):
    pass


class Request(object):
    pass


class OutputBoundary(ABC):
    @abstractmethod
    def on_success(self, response: Response) -> None:
        pass

    @abstractmethod
    def on_failure(self, error: str) -> None:
        pass


class InputBoundary(ABC):
    @abstractmethod
    def execute(self, request: Request) -> None:
        pass
