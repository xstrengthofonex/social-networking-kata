from abc import ABC, abstractmethod

class BaseUseCase(ABC):
  @abstractmethod
  def execute(self, request: object) -> None:
    pass