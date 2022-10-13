import click

@click.command()
def main():
    click.echo("DocuWorks Assessment Text Editor\n")

    # Load txt
    txtFile = click.open_file("text.txt", "r")

    # Display txt
    text = txtFile.read()
    click.echo(text)

    # Save txt
    txtFile.close()



if __name__ == "__main__":
    main()