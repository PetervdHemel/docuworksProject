from tkinter import Toplevel
import click
import sys
import re
from collections import Counter

@click.command()
def main():
    txtFile = click.open_file("text.txt", "r")
    text = txtFile.read()
    txtFile.close()
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
    if option == '1':
        display(text)
    elif option == '2':
        search(text)
    elif option == '3':
        replace(text)
    elif option == '4':
        commonWords(text)
    elif option == '8':
        sys.exit()
    else:
        click.echo('Invalid.')
        main()
    main()
    

def display(txt):
    click.echo(txt)
    

def search(txt):
    '''Searches through the text using a user input string and outputs index.'''
    option = 'y'
    while option == 'y':
        search = input("Please provide an input string for searching: ")
        result = re.finditer(search, txt)

        if result != None:
            click.echo("Index of found searched phrase:")
            indices = [index.start() for index in result]
            click.echo(indices)
        else:
            click.echo("No results found.")
        
        click.echo("\nWould you like to try again? y/n\n")
        option = click.getchar()

def replace(txt):
    '''Searches through the text using a user input string and replaces text'''
    option = 'y'
    while option == 'y':
        # Initalize new text object for replaced text
        newtxt = 'replaced'
        click.clear()

        search = input("Please provide an input string for searching: ")
        replace = input("Please provide an input string for replacing: ")

        txt = re.sub(search, replace, txt)
        click.echo(f"New text: \n{txt}")

        click.echo("\nDo you want to save the edited file as a new file? y/n: ")
        option = click.getchar()

        if option == 'y':
            name = input("Please enter the file name: ")
            name = name + ".txt"
            with click.open_file(name, 'w') as newFile:
                newFile.seek(0)
                newFile.write(txt)
                newFile.truncate()
        
        click.clear()
        click.echo("Would you like to try again? y/n\n")
        option = click.getchar()

def commonWords(txt):
    '''Finds the most commonly used words in the text.'''
    option = 'y'
    while option == 'y':
        toplimit = input("How many of the most used words should be shown?: ")
        try:
            int(toplimit)
        except:
            click.echo("Please enter a valid number.")
        else:
            words = txt.split(" ")
            words_count = Counter(words).most_common()
            click.echo(f"Most frequent word used is: {words_count[0][0]} with {words_count[0][1]} occurrences.")
            click.pause()

            click.clear()
            click.echo("Would you like to try again? y/n\n")
            option = click.getchar()


if __name__ == "__main__":
    main()