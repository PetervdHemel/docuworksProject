import click
import sys
import re
from collections import Counter
from abc import ABC, abstractmethod
from pathlib import Path


class NoPalindromesError(Exception):
    def __str__(self):
        return f"The processed string contains no palindromes."


class NoEmailAddressesError(Exception):
    def __str__(self):
        return f"The processed string contains no email addresses."


class TextProcessor(ABC):
    @abstractmethod
    def load(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def iterSearch(self, searchPhrase) -> None:
        raise NotImplementedError

    @abstractmethod
    def replace(self, searchStr, replaceStr) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, path: Path) -> None:
        raise NotImplementedError

    @abstractmethod
    def findCommon(self, limit) -> None:
        raise NotImplementedError

    @abstractmethod
    def findPalindromes(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def findSecret(self) -> None:
        raise NotImplementedError


class MyTextProcessor(TextProcessor):
    def load(self, path):
        with click.open_file(path, "r") as file:
            self.text = file.read()

    def display(self):
        click.echo(self.text)

    def iterSearch(self, searchPhrase):
        result = re.finditer(
            searchPhrase, self.text
        )  # Iteratively searches phrase using regex


        indices =  [(index.start(), index.end() - 1) for index in result] # Creates a list of indices for each index in result
        if indices == []:
            click.echo("None found.")
        else:
            click.secho(f"Start, stop indices of {searchPhrase}:", fg="white", bg="black")
            click.echo(indices)
            

    def replace(self, searchStr, replaceStr):
        # Initalize new text object for replaced text
        self.newTxt = re.sub(searchStr, replaceStr, self.text)

        click.secho("New text:\n", fg="green", bg="black")
        click.echo(self.newTxt)

    def save(self, path):
        with click.open_file(path, "w") as newFile:
            newFile.seek(0)  # Start at beginning of the file.
            newFile.write(self.newTxt)
            newFile.truncate()

    def findCommon(self, limit):
        """Finds the most common words in text. 'limit' Is the amount of common words shown."""
        words = self.text.split(" ")
        words_count = Counter(words).most_common()
        for x in range(limit):
            click.secho(
                f"Most frequent word place {x + 1} is: ",
                fg="white",
                bg="black",
                nl=False,
            )
            click.secho(
                f"{words_count[x][0]}",
                fg="red",
                bg="black",
                nl=False,
            )
            click.secho(
                f" with {words_count[x][1]} counts.",
                fg="green",
                bg="black",
                )

    def findPalindromes(self) -> list:
        """Iterates through text to find if the substring is equal to the reverse of the substring."""
        # Makes text lower case, removes spaces and removes newline which could be counted as a palindrome character
        string = self.text.lower().replace(" ", "").replace("\n", "")
        stringLength = len(string)

        # Empty list for storing palindromes
        palindromes = []

        with click.progressbar(
            length=stringLength
        ) as bar:  # Use click to provide a progress bar since the operation might take a while
            for i in bar:
                for j in range(i + 1, stringLength + 1):
                    temp = string[
                        i:j
                    ]  # Use string slicing to slice each segment of text for comparison
                    if len(temp) > 2:
                        if (
                            temp == temp[::-1]
                        ):  # Compare the sliced text to its inverted counterpart
                            palindromes.append(
                                temp
                            )  # Add the palindromes to list, useful for any future additions.

        if palindromes == []:  # Check if any palindromes were added to the list
            raise NoPalindromesError  # Could also catch the error and print the exception instead of raising.
        else:
            return palindromes

    def findEmails(self):
        """
        Uses regular expressions (regex) to extract emails from text.
        Regex lookahead to make sure the sneakily placed fake emails are avoided:
        """
        emails = re.findall(
            r"[a-z0-9\-+_]+[\.(?!\.)]*[a-z0-9\-+_]+@[a-z0-9\-+_]+[\.(?=\.)]*[a-z]+[a-z\.]*",
            self.text,
        )
        if emails == []:
            raise NoEmailAddressesError
        else:
            click.echo(emails)

    def findSecret(self):
        """Finds secret message in text"""

        # Find all words in text that have a capitalized letter surrounded by lower case letters.
        capitalwords = re.findall(r"[a-z]+[A-Z]+[a-z]+", self.text)

        # Use list comprehension to extract capitalized characters from strings in capitalwords
        upper = []
        for word in capitalwords:  # loop through words in list
            string = ""
            string = [
                char for char in word if char.isupper()
            ].pop()  # nested loop through characters in word
            upper.append(string)

        # Define the shift for caesar decryption
        shift = 13  # His 'lucky number'
        encryptedString = ""
        encryptedString = encryptedString.join(upper)

        # Print encrypted string for before/after comparison
        click.secho(f"Encrypted Message: {encryptedString}", fg="red", bg="black")

        decryptedString = ""

        for char in encryptedString:
            uni = ord(char)  # Convert character to unicode
            index = uni - ord("A")  # Find index position 0-25

            # Perform shift
            new_index = (index - shift) % 26

            # Convert back
            new_uni = new_index + ord("A")

            new_char = chr(new_uni)

            # Add to string
            decryptedString += new_char

        click.secho(f"Secret Message: {decryptedString}", fg="green", bg="black")


def loadApp() -> MyTextProcessor:
    """Calls text processor class and loads the class. Returns class."""
    app = MyTextProcessor()
    app.load(Path(r".\text.txt"))

    return app


@click.group()
def main():
    """
    Reads the text file 'text.txt' and performs various functions.\n
    Example Usage:\n
    python docuworksProject.py replace --help\n
    To obtain the help page for the replace command.
    """


@main.command("display")
def display():
    """
    Displays text.
    """
    app = loadApp()

    app.display()


@main.command("search")
@click.argument("searchphrase")
def search(searchphrase):
    """
    Searches text using SEARCHPHRASE, outputs index.\n
    Example: python docuworksProject.py search Tos
    """

    app = loadApp()
    app.iterSearch(searchphrase)


@main.command("replace")
@click.argument("searchphrase")
@click.argument("replacephrase")
@click.option("--save", default=False, help="Save as new file True/False")
def replace(searchphrase, replacephrase, save):
    """
    Search phrase and replace it.

    SEARCHPHRASE is used to search the text.\n
    REPLACEPHRASE is used to replace the text.\n

    Example: python docuworksProject.py replace --save True Tos Peter
    """

    app = loadApp()
    app.replace(searchphrase, replacephrase)

    if save:
        fileName = click.prompt("Please enter a file name", type=str)
        fileName = fileName + ".txt"

        app.save(Path(fileName))
        click.secho(f"Saved {fileName} succesfully.", fg="green", bg="black")


@main.command("common")
@click.option("--limit", default=5, help="Number of most common words listed")
def commonWords(limit):
    """Finds most commonly used words in text."""

    app = loadApp()

    app.findCommon(limit)


@main.command("palindromes")
def palindromes():
    """Finds all palindromes in text."""

    app = loadApp()

    palindromes = app.findPalindromes()
    click.echo(palindromes)


@main.command("emails")
def emails():
    """Finds all emails in text."""

    app = loadApp()

    app.findEmails()


@main.command("secret")
def secret():
    """Finds secret message in text."""

    app = loadApp()

    app.findSecret()


if __name__ == "__main__":
    main()
