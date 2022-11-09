from docuworksProject.my_text_processor import MyTextProcessor
from pathlib import Path
from os import remove as rem

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