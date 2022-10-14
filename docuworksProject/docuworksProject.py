from json import load
from tkinter import Toplevel
import click
import sys
import re
from collections import Counter
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

class MyTextProcessor(TextProcessor):
    def load(self, path):
        with click.open_file(path, "r") as file:
            self.text = file.read()

    def display(self):
        click.echo(self.text)

    def iterSearch(self, searchPhrase):
        result = re.finditer(searchPhrase, self.text) # Iteratively searches phrase using regex

        if result != None:
            click.echo("Index of found searched phrase:")
            indices = [index.start() for index in result] # Creates a list of indices for each index in result
            click.echo(indices)
        else:
            click.echo("No results found.")
    
    def replace(self, searchStr, replaceStr):
        # Initalize new text object for replaced text
        self.newTxt = re.sub(searchStr, replaceStr, self.text)

        click.echo(f"New text: \n{self.newTxt}")

    def save(self, path):
        with click.open_file(path, 'w') as newFile:
                newFile.seek(0) # Start at beginning of the file.
                newFile.write(self.newTxt)
                newFile.truncate()

    def findCommon(self, limit):
            '''Finds the most common words in text. 'limit' Is the amount of common words shown.'''
            words = self.text.split(" ")
            words_count = Counter(words).most_common()
            for x in range(limit):
                click.echo(f"Most frequent word place {x + 1} is: {words_count[x][0]} with {words_count[x][1]} occurrences.")

            click.pause()

def loadApp():
    '''Calls text processor class and loads the class. Returns class.'''
    app = MyTextProcessor()
    app.load(Path(r"text.txt"))

    return app

@click.command()
def main():
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
        display()
    elif option == '2':
        search()
    elif option == '3':
        replace()
    elif option == '4':
        commonWords()
    elif option == '8':
        sys.exit()
    else:
        click.echo('Invalid.')
        main()
    
@click.command()
def display():
    app = loadApp()

    app.display()
    click.pause()
    
@click.command()
def search():
    '''Searches through the text using a user input string and outputs index.'''
    option = 'y'
    while option == 'y':
        click.clear()
        search = input("Please provide an input string for searching: ")

        app = loadApp()
        app.iterSearch(search)

       
        click.echo("\nWould you like to try again? y/n\n")
        option = click.getchar()

@click.command()
def replace():
    '''Searches through the text using a user input string and replaces text'''
    option = 'y'
    while option == 'y':
        click.clear()

        search = input("Please provide an input string for searching: ")
        replace = input("Please provide an input string for replacing: ")

        app = loadApp()
        app.replace(search, replace)

        click.echo("\nDo you want to save the edited file as a new file? y/n: ")
        option = click.getchar()

        if option == 'y':
            name = input("Please enter the file name: ")
            name = name + ".txt"
            
            app.save(Path(name))
        
        click.clear()
        click.echo("Would you like to try again? y/n\n")
        option = click.getchar()

@click.command()
def commonWords():
    '''Finds the most commonly used words in the text.'''
    option = 'y'
    while option == 'y':
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


if __name__ == "__main__":
    main()