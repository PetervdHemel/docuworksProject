# DocuWorks Text Editor Assessment
> Reads a text file (text.txt) and performs various functions on it as required by the Product Owner.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Text editor that performs various functions as follows:
* Display text.
* Search text for a user-input phrase.
* Search for a user-input phrase and replace it.
    * Following this, allow the user to save text as a new file.
* List the most common words seen in the text.
* Find and list all palindromes.
* List all email addresses found in the text.
* Show the secret message in the text.
    * Secret message is encoded as mid-word upper case characters.
    * Secret message uses Caesar Cipher with shift 13.

![](img/overview.png)

## Installation
Create and activate a virtual environment (venv):
```sh
python -m venv venv
```

**OS X and Linux**
```sh
./venv/bin/activate
```
```sh
pip3 install -r requirements.txt
```

**Windows**
```sh
.\venv\Scripts\activate.bat
```
```sh
python -m pip install -r requirements.txt
```

## Documentation
**Table of Contents**

1. Structure
2. Menu
3. MyTextProcessor Examples

**Structure:**

The program is divided into three sections:


### Custom Exceptions:
```
class NoPalindromesError(Exception):
```
```
class NoEmailAddressesError(Exception):
```
These exceptions are raised in the ```MyTextProcessor``` class under ```findPalindromes``` and ```findEmails``` respectively, when the text is processed and contains no palindromes or email addresses.

As an example, both palindromes and emails are checked as an empty list:
```
if (
            palindromes == []
        ):
    raise NoPalindromesError
```
This raises the ```__str__``` component of ```NoPalindromesError(Exception)``` class: 
```
def __str__(self):
    return f"The processed string contains no palindromes."
```

### MyTextProcessor Class:
```
class MyTextProcessor(TextProcessor):
```
Calls ```TextProcessor(ABC)``` abstract class.

```TextProcessor``` contains all the primary features of the program, seen as functions. It is made up of the following functions:

---
```
load(self, path):
```
Opens the text file under Path ```text.txt``` under read ```"r"``` as a file, and stores it in ```self.text```. This variable is used in the rest of the ```MyTextProcessor``` functions as a string file to perform actions on.

---
```
display(self):
```
Simply prints the ```self.text``` string:
```
click.echo(self.text)
```
---
```
iterSearch(self, searchPhrase):
```
Uses ```import re``` function ```finditer``` to iteratively search through the ```self.text``` string using ```searchPhrase``` and stores it in ```result```:
```        
result = re.finditer(
    searchPhrase, self.text
    )  # Iteratively searches phrase    using regex
```
```re.finditer``` outputs an iterator datastream, from which the index numbers have to be printed. 

Indices are acquired by 
```
indices = [
    index.start() for index in result
```
after which the indices are printed.

---
```
replace(self, searchStr, replaceStr):
```
Makes use of ```import re``` function ```sub``` to substitute (replace) ```self.text``` substrings ```searchStr``` with ```replaceStr``` and then prints the new text:

```
newTxt = re.sub(searchStr, replaceStr, self.text)
```
---
```
save(self, path):
```
Can be called to open a file as 'write' ```"w"``` following ```path``` input:
```
with click.open_file(path, "w") as newFile:
    newFile.seek(0)  # Start at beginning of the file.
    newFile.write(self.newTxt)
```
It makes sure to write at the beginning of the file, regardless of if it is a new file or not with ```.seek(0)```

---
```
findCommon(self, limit):
```
Is used to find the most common words in the text, ranked by ```limit``` set by the user input.
```
words = self.text.split(" ")
```
Splits the entire text string into a list, where each word is a list item. This makes it easier to count the number of common words.
```
words_count = Counter(words).most_common()
```
```Counter``` is used from the ```collections``` [module](https://docs.python.org/3/library/collections.html#collections.Counter) to create a dictionary ```words_count``` with their key as popularity, value as number of occurrences. These are then printed:
```
for x in range(limit):
    click.echo(
        f"Most frequent word place {x + 1} is: {words_count[x][0]} with {words_count[x][1]} occurrences."
    )
```

---
```
findPalindromes(self) -> list:
```

---
```
findEmails(self):
```

---
```
findSecret(self):
```
---