from abc import ABC, abstractmethod

class TextProcessor(ABC):
    @abstractmethod
    def load(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, search_phrase) -> list[tuple[int, int]]:
        raise NotImplementedError

    @abstractmethod
    def replace(self, search_string, replace_string) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_common_words(self, limit) -> list[tuple[str, int]]:
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
    def find_secret(self) -> None:
        raise NotImplementedError