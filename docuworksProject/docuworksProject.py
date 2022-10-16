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

        if result != None:
            click.echo("Index of found searched phrase:")
            indices = [
                index.start() for index in result
            ]  # Creates a list of indices for each index in result
            click.echo(indices)
        else:
            click.echo("No results found.")

    def replace(self, searchStr, replaceStr):
        # Initalize new text object for replaced text
        newTxt = re.sub(searchStr, replaceStr, self.text)

        click.echo(f"New text: \n{newTxt}")

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
            click.echo(
                f"Most frequent word place {x + 1} is: {words_count[x][0]} with {words_count[x][1]} occurrences."
            )

        click.pause()

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
                            
        click.clear()
        if (
            palindromes == []
        ):  # Check if any palindromes were added to the list
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
        click.echo(f"Encrypted Message: {encryptedString}")

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

        click.echo(f"Secret Message: {decryptedString}")


def loadApp() -> MyTextProcessor:
    """Calls text processor class and loads the class. Returns class."""
    app = MyTextProcessor()
    app.load(Path(r"text.txt"))

    return app


@click.command()
def main():
    """"""
    click.clear()
    click.echo("DocuWorks Assessment Text Editor\n")

    click.echo("Please select a Menu Option | (1 - 8): ")
    click.echo("1. Display text")
    click.echo("2. Search phrase")
    click.echo("3. Search & replace")
    click.echo("4. List most common words")
    click.echo("5. List palindromes")
    click.echo("6. List email addresses")
    click.echo("7. Show secret message")
    click.echo("8. Quit program.")

    click.echo("")
    option = click.getchar()

    # Process input character
    if option == "1":
        display()
    elif option == "2":
        search()
    elif option == "3":
        replace()
    elif option == "4":
        commonWords()
    elif option == "5":
        palindromes()
    elif option == "6":
        emails()
    elif option == "7":
        secret()
    elif option == "8":
        sys.exit()
    else:
        click.clear()
        click.echo("Invalid option.")
        click.pause()
        main()


@click.command()
def display():
    app = loadApp()

    app.display()
    click.pause()


@click.command()
def search():
    """Searches through the text using a user input string and outputs index."""
    option = "y"
    while option == "y":
        click.clear()
        search = input("Please provide an input string for searching: ")

        app = loadApp()
        app.iterSearch(search)

        click.echo("\nWould you like to try again? y/n\n")
        option = click.getchar()


@click.command()
def replace():
    """Searches through the text using a user input string and replaces text"""
    option = "y"
    while option == "y":
        click.clear()

        search = input("Please provide an input string for searching: ")
        replace = input("Please provide an input string for replacing: ")

        app = loadApp()
        app.replace(search, replace)

        click.echo("\nDo you want to save the edited file as a new file? y/n: ")
        option = click.getchar()

        if option == "y":
            name = input("Please enter the file name: ")
            name = name + ".txt"

            app.save(Path(name))

        click.clear()
        click.echo("Would you like to try again? y/n\n")
        option = click.getchar()


@click.command()
def commonWords():
    """Finds the most commonly used words in the text."""
    option = "y"
    while option == "y":
        click.clear()
        app = loadApp()

        toplimit = input("How many of the most used words should be shown?: ")

        try:
            toplimit = int(toplimit)
        except:
            click.echo("Please enter a valid number.")
            click.pause()
        else:
            app.findCommon(toplimit)

        click.clear()
        click.echo("Would you like to try again? y/n\n")
        option = click.getchar()


@click.command()
def palindromes():
    click.clear()
    app = loadApp()

    palindromes = app.findPalindromes()
    click.echo(palindromes)
    click.pause()


@click.command()
def emails():
    click.clear()
    app = loadApp()

    app.findEmails()


@click.command()
def secret():
    click.clear()
    app = loadApp()

    app.findSecret()
    click.pause()


if __name__ == "__main__":
    main()
