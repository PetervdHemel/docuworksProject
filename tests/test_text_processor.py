from docuworksProject.my_text_processor import MyTextProcessor
from docuworksProject.exceptions import NoPalindromesError, NoEmailAddressesError 
from pathlib import Path
from os import remove as rem
import pytest

path = Path(r".\text.txt")
test_file = Path(r".\save_my_text.txt")

app = MyTextProcessor()
assert isinstance(app, MyTextProcessor)

app.load(path)

def test_load() -> None:
    assert app.text.startswith("Otje")
    assert app.text.endswith("info@uitgeverijvolt.nl")

    assert "officiÃ«le" not in app.text

def test_display() -> None:
    assert app.text == app.display()

def test_save() -> None:
    app.save(test_file)
    assert test_file.exists()
    rem(test_file)

def test_search() -> None:
    results = app.search("Otje")
    assert isinstance(results, list)
    assert results == [(0, 4), (294, 298), 
                       (379, 383), (681, 685), 
                       (1060, 1064), (1157, 1161), 
                       (2111, 2115), (2431, 2435), 
                       (2809, 2813)]

def test_replace() -> None:
    app.replace(search_string="Otje", replace_string="Pluk")

    assert app.text.startswith("Pluk")

def test_get_common_words() -> None:
    top_ten = app.get_common_words(10)
    assert top_ten == [('een', 26), ('de', 26), 
                       ('en', 23), ('van', 19),
                       ('Tos', 18), ('zijn', 16),
                       ('het', 13), ('voor', 12),
                       ('met', 10), ('in', 10)]

def test_get_palindrome_words() -> None:
    palindromes = app.get_palindrome_words()

    assert palindromes == ['kok', 'radar', 'negen', 
                           'meetsysteem', 'kok', 'redder', 
                           'lepel', 'pap', 'tot', 'kok', 
                           'nemen']
    
    app.text = "No palindromes"
    with pytest.raises(Exception):
        palindromes = app.get_palindrome_words()

def test_get_emails() -> None:
    with pytest.raises(Exception):
        app.get_emails()

    app.load(path)
    assert app.get_emails() == ['manuscripten@querido.nl', 
                                'manuscripten@uitgeverijvolt.nl.', 
                                'publiciteit@querido.nl', 
                                'publiciteit@querido.nl', 
                                'publiciteit@uitgeverijvolt.nl', 
                                'publiciteit@uitgeverijvolt.nl', 
                                'info@lovebooks.com', 
                                'nina88@nijghenvanditmar.nl', 
                                'publiciteit@uitgeverijathenaeum.nl', 
                                'publiciteit@arbeiderspers.nl', 
                                'publiciteit@degeus.nl', 
                                'publiciteit@arbeiderspers.co.uk', 
                                'b.kleiweg@singeluitgeverijen.nl', 
                                'info@nijghenvanditmar.nl', 
                                'info@querido.nl', 
                                'info@arbeiderspers.nl', 
                                'info@uitgeverijathenaeum.nl', 
                                'info@degeus.nl', 
                                'info@uitgeverijvolt.nl']

def test_find_secret() -> None:
    assert app.find_secret() == ("OBAHFCHAG", "BONUSPUNT")