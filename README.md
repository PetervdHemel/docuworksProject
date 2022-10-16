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

1. Custom Exceptions:
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
2. MyTextProcessor Class:
```
class MyTextProcessor(TextProcessor):
```
Calls ```TextProcessor(ABC)``` abstract class.

```TextProcessor``` contains all the primary features of the program, seen as functions. It is made up of the following functions:
```
load(self, path):
```
>which opens the text file under Path ```text.txt``` under read ```"r"``` as a file, and stores it in ```self.text```. This variable is used in the rest of the ```MyTextProcessor``` functions as a string file to perform actions on.
```
display(self):
```
> Simply prints the ```self.text``` string.
```
iterSearch(self, searchPhrase):
```
> Uses ```import re``` function ```finditer``` to iteratively search through the ```self.text``` string using ```searchPhrase``` and stores it in ```result```. ```re.finditer``` outputs an iterator datastream, from which the index numbers have to be printed. Indices are acquired by ```indices = [
                index.start() for index in result```
after which the indices are printed.
```
replace(self, searchStr, replaceStr):
```
> Makes use of ```import re``` function ```sub``` to substitute (replace) ```self.text``` substrings ```searchStr``` with ```replaceStr``` and then prints the new text.
```
save(self, path):
```
```
findCommon(self, limit):
```
```
findPalindromes(self) -> list:
```
```
findEmails(self):
```
```
findSecret(self):
```
