# Portfolio

Bunch of scripts helping you to reinvest into your stock portfolio.

## Installation

This project was setup with [Poetry](https://python-poetry.org/docs/), so you have to [install](https://python-poetry.org/docs/) it before proceeding.

Install the dependencies afterwards (preferred in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/)):

```bash
poetry install
```

## Requirements

Scripts were tested with Python 3.7 on Linux.
To run the Notebook, you need [Jupyter](https://jupyter.readthedocs.io/en/latest/install.html) installed which I added as optional dependency:

```bash
poetry install --extras "jupyter"
# to run it
jupyter notebook
```

The very first statement of the Notebook accesses a [Google Spread Sheet](https://docs.google.com/spreadsheets) which represents the portfolio, including stock symbols and desired networth distribution.
If you want to do the same, you have to [authorise the Notebook to access Google's API](https://developers.google.com/sheets/api/guides/authorizing). Store the credentials in `google-sheets-credentials.json`.
You can use also [Panda Datareader](https://pandas-datareader.readthedocs.io/en/latest/) to load your portfolio from a csv file or any other source you like.