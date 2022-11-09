import click
from my_text_processor import MyTextProcessor
from pathlib import Path


def load_app() -> MyTextProcessor:
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
    app = load_app()

    click.echo(app.display())


@main.command("search")
@click.argument("searchphrase")
def search(searchphrase):
    """
    Searches text using SEARCHPHRASE, outputs index.\n
    Example: python docuworksProject.py search Tos
    """

    app = load_app()
    search_result = app.search(searchphrase)

    if not search_result:
        click.echo("None found.")
    else:
        click.secho(
            f"Start, stop indices of {searchphrase}:", fg="white", bg="black"
        )
        click.echo(search_result)


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

    app = load_app()
    app.replace(searchphrase, replacephrase)
    click.secho("New text:\n", fg="green", bg="black")

    click.echo(app.display())

    if save:
        file_name = click.prompt("Please enter a file name", type=str)
        file_name = file_name + ".txt"

        app.save(Path(file_name))
        click.secho(f"Saved {file_name} succesfully.", fg="green", bg="black")


@main.command("common")
@click.option("--limit", default=5, help="Number of most common words listed")
def common_words(limit):
    """Finds most commonly used words in text."""

    app = load_app()

    words_list = app.get_common_words(limit)

    for x in range(limit):
        click.secho(
            f"Most frequent word place {x + 1} is: ",
            fg="white",
            bg="black",
            nl=False,
        )
        click.secho(
            f"{words_list[x][0]}",
            fg="red",
            bg="black",
            nl=False,
        )
        click.secho(
            f" with {words_list[x][1]} counts.",
            fg="green",
            bg="black",
        )


"""
Deprecated functionality

@main.command("palindromes")
def palindromes():
    Finds all palindrome phrases in text.

    app = loadApp()

    palindromes = app.findPalindromes()
    click.echo(palindromes)
"""

@main.command("emails")
def emails():
    """Finds all emails in text."""

    app = load_app()

    emails = app.get_emails()

    for i in range(len(emails)):
        click.echo(f"Email {i + 1}: {emails[i]}")


@main.command("secret")
def secret():
    """Finds secret message in text."""

    app = load_app()

    encrypted, decrypted = app.find_secret()

    # Print encrypted string for before/after comparison
    click.secho(f"Encrypted Message: {encrypted}", fg="red", bg="black")
    click.secho(f"Secret Message: {decrypted}", fg="green", bg="black")


@main.command("palindromes")
def palindromes():
    """
    Finds all full palindrome words in text.\n
    Differs from 'palindromes' as it only compares full words, regardless of punctuation, not every phrase.
    """

    app = load_app()

    palindromes = app.get_palindrome_words()
    click.echo(palindromes)


if __name__ == "__main__":
    main()
