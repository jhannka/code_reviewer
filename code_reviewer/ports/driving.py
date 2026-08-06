from abc import ABC, abstractmethod

class CodeReviewUseCasePort(ABC):
    @abstractmethod
    def execute_review(self, source_or_git: str) -> str:
        """Run the core review logic on a file path or git changes."""
        pass
