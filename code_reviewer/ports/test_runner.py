from abc import ABC, abstractmethod

class TestRunnerPort(ABC):
    @abstractmethod
    def execute_tests(self) -> str:
        """Run the project's test suite and return stdout/stderr output."""
        pass
