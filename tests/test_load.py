from docuworksProject.my_text_processor import MyTextProcessor
from pathlib import Path

path = Path(r".\text.txt")

app = MyTextProcessor()
assert isinstance(app, MyTextProcessor)

def test_load() -> None:
    app.load(path)
    assert app.text.startswith("Otje")
    assert app.text.endswith("info@uitgeverijvolt.nl")

    assert "officiÃ«le" not in app.text