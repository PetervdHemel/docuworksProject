from collections import Counter
from text_processor import TextProcessor
from exceptions import NoPalindromesError, NoEmailAddressesError
import re

class MyTextProcessor(TextProcessor):
    def load(self, path) -> None:
        with open(path, "r", encoding="UTF-8") as file:
            self.text = file.read()

    def display(self) -> str:
        return self.text

    def search(self, search_phrase: str) -> list[tuple[int, int]]:
        return [
                (match.span())
                # Iteratively searches phrase using regex
                for match in re.finditer(search_phrase, self.text)
            ]


    def replace(self, search_string, replace_string) -> None:
        # Initalize new text object for replaced text
        self.text = re.sub(search_string, replace_string, self.text)
        

    def save(self, path) -> None:
        with open(path, "w") as new_file:
            new_file.seek(0)  # Start at beginning of the file.
            new_file.write(self.text)
            new_file.truncate()

    def format_text(self, set_lower: bool) -> filter:
        """Fomats input text to remove punctuation, and returns a filter object with filtered words"""

        format_text = self.text.replace("\n", " ")
        format_text = re.sub(r"[^\w\s]", "", format_text) # Remove punctuation

        if set_lower:
            format_text = format_text.lower()

        words = format_text.split(" ")
        # Filter out leftover empty strings:
        words = filter(None, words)

        return words

    def get_common_words(self, limit: int) -> list[tuple[str, int]]:
        """Finds the most common words in text. 'limit' Is the amount of common words shown."""
        words = self.format_text(False)

        words_count = Counter(words).most_common(limit)
        return words_count

    """
    Deprecated functionality:

    def findPalindromes(self) -> list[str]:
        Iterates through text to find if the substring is equal to the reverse of the substring.
        # Makes text lower case, removes spaces and removes newline which could be counted as a palindrome character
        string = self.text.lower().replace(" ", "").replace("\n", "")

        # Get rid of punctuation
        string = re.sub(r"[^\w\s]", "", string)

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
    """

    def get_palindrome_words(self) -> list[str]:
        """Iterates through each word in the text, to see if it is equal to its reverse equivalent."""

        words = self.format_text(True)

        valid_words = []
        for word in words:
            # Get rid of punctuation
            word = re.sub(r"[^\w\s]", "", word)
            valid_words.append(word)

        # Use list comprehension to store each word into valid_strings if it is at least 3 long
        valid_strings = [string for string in valid_words if len(string) > 2]

        palindromes = []

        for i, string in enumerate(valid_strings):
            temp_word = string
            if temp_word == temp_word[::-1]:
                palindromes.append(temp_word)

        if palindromes == []:
            raise NoPalindromesError
        else:
            return palindromes

    def get_emails(self) -> list[str]:
        """
        Uses regular expressions (regex) to extract emails from text.
        Regex lookahead to make sure the sneakily placed fake emails are avoided:
        """
        emails = re.findall(
            r"[a-z0-9\-+_]+[\.(?!\.)]*[a-z0-9\-+_]+@[a-z0-9\-+_]+[\.(?=\.)]*[a-z]+[a-z\.]*",
            self.text,
        )
        if not emails:
            raise NoEmailAddressesError
        else:
            return emails

    def find_secret(self) -> str:
        """Finds secret message in text"""

        # Find all words in text that have a capitalized letter surrounded by lower case letters.
        capital_words = re.findall(r"[a-z]+[A-Z]+[a-z]+", self.text)

        # Use list comprehension to extract capitalized characters from strings in capital_words
        upper = []
        for word in capital_words:  # loop through words in list
            string = ""
            string = [
                char for char in word if char.isupper()
            ].pop()  # nested loop through characters in word
            upper.append(string)

        # Define the shift for caesar decryption
        shift = 13  # His 'lucky number'
        encrypted_string = "".join(upper)

        decrypted_string = ""

        for char in encrypted_string:
            uni = ord(char)  # Convert character to unicode
            index = uni - ord("A")  # Find index position 0-25

            # Perform shift
            new_index = (index - shift) % 26

            # Convert back
            new_uni = new_index + ord("A")

            new_char = chr(new_uni)

            # Add to string
            decrypted_string += new_char

        return encrypted_string, decrypted_string