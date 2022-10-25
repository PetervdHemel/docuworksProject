from abc import ABC, abstractmethod
from pathlib import Path

class TextProcessor(ABC):
    @abstractmethod
    def load(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, search_phrase: str) -> list[tuple[int, int]]:
        raise NotImplementedError

    @abstractmethod
    def replace(self, search_string: str, replace_string: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_common_words(self, limit: bool) -> list[tuple[str, int]]:
        raise NotImplementedError

    """
    @abstractmethod
    def findPalindromes(self) -> list[str]:
        raise NotImplementedError
    """

    @abstractmethod
    def get_palindrome_words(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_emails(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def find_secret(self) -> str:
        raise NotImplementedError