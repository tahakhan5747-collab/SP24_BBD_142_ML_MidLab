"""Optional: recreate the bundled CSV files from the original UCI downloads."""

from pathlib import Path
from urllib.request import urlopen
import zipfile
import io
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)


def archive(url):
    with urlopen(url, timeout=60) as r:
        return zipfile.ZipFile(io.BytesIO(r.read()))


if __name__ == "__main__":
    mpg = archive("https://archive.ics.uci.edu/static/public/9/auto+mpg.zip")
    cols = [
        "mpg",
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model_year",
        "origin",
        "car_name",
    ]
    pd.read_csv(
        io.BytesIO(mpg.read("auto-mpg.data")), sep=r"\s+", names=cols, na_values="?"
    ).to_csv(DATA / "auto_mpg.csv", index=False)
    outer = archive("https://archive.ics.uci.edu/static/public/222/bank+marketing.zip")
    bank = zipfile.ZipFile(io.BytesIO(outer.read("bank.zip")))
    (DATA / "bank.csv").write_bytes(bank.read("bank.csv"))
    (DATA / "bank_original_names.txt").write_bytes(bank.read("bank-names.txt"))
    text = archive(
        "https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip"
    )
    lines = (
        text.read("sentiment labelled sentences/yelp_labelled.txt")
        .decode()
        .splitlines()
    )
    pd.DataFrame(
        [s.rsplit("\t", 1) for s in lines if s.strip()], columns=["text", "sentiment"]
    ).to_csv(DATA / "reviews.csv", index=False)
    print("Saved real datasets in", DATA)
