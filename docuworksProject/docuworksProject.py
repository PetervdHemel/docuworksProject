import click
import sys

@click.command()
def main():
    click.clear()
    click.echo("DocuWorks Assessment Text Editor\n")

    click.echo("Please select a Menu Option | (1 - 8): ")
    option = click.getchar()
    click.echo("1. Display text")
    click.echo("2. Search phrase")
    click.echo("3. Search & replace")
    click.echo("4. List most common words")
    click.echo("5. List palindromes")
    click.echo("6. List email addresses")
    click.echo("7. Show secret message")
    click.echo("8. Quit program.")
    if option == '1':
        display()
    elif option == '2':
        search()
    elif option == '8':
        sys.exit()
    else:
        click.echo('Invalid.')
        main()

@click.command()
def display():
    txtFile = click.open_file("text.txt", "r")

    # Display txt
    text = txtFile.read()
    click.echo(text)

    # Save txt
    txtFile.close()

@click.command()
def search():
    '''Searches through the text using a user input string and outputs index.'''
    input("Please provide an input string for searching: ")
    click.echo("")


if __name__ == "__main__":
    main()