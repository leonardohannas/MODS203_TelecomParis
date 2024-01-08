import csv
import json
import os
import re

import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))


def rename_columns(filename):
    """
    Rename columns of a csv file

    Parameters:
    ----------
        filename (str): name of the csv file
    """

    df = pd.read_csv(os.path.dirname(PATH) + "\data\\csv_files\\" + filename)

    columns = {
        "price/unity": "price/unity [€/u]",
        "price": "price [€]",
        "Valeur énergétique en kJ": "Valeur énergétique [kJ]",
        "Valeur énergétique en kCal": "Valeur énergétique [kCal]",
        "Matières grasses": "Matières grasses [g]",
        "Dont acides gras saturés": "Dont acides gras saturés [g]",
        "Dont acides gras mono-insaturés": "Dont acides gras mono-insaturés [g]",
        "Glucides": "Glucides [g]",
        "Dont sucres": "Dont sucres [g]",
        "Protéines": "Protéines [g]",
        "Fibres alimentaires": "Fibres alimentaires [g]",
        "Sel": "Sel [g]",
        "Sodium": "Sodium [mg]",
    }

    df = df.rename(columns=columns)

    df.to_csv(os.path.dirname(PATH) + "/data/csv_files/" + filename, index=False)


def clean_value(text):
    """
    Clean a string to get a float value

    Parameters:
    ----------
        text (str): string to clean

    Returns:
    ----------
        float_value (float): float value of the string
    """

    text_match = re.search(r"(\d+([.,]{1}\d{1,2}){1}?)", text)
    if text_match:
        float_value = float(text_match.group(1).replace(",", "."))
    else:
        float_value = None

    return float_value


def get_cookies_headers(filename="config.json"):
    """
    Get cookies and headers from a json file

    Parameters:
    ----------
        filename (str): name of the json file
    """

    try:
        with open(PATH + "/" + filename, "r") as file:
            config = json.load(file)
            return config.get("cookies", {}), config.get("headers", {})
    except FileNotFoundError:
        print("File not found")


def save_supermarket_info(data, filename):
    """
    Save supermarket info in a csv file

    Parameters:
    ----------
        data (dict/list of dict): data to save
        filename (str): name of the csv file
    """

    df = pd.DataFrame(data)

    df.to_csv(os.path.dirname(PATH) + "/data/" + filename, index=False)


def save_product_info(data, filename):
    """
    Save product info in a csv file

    Parameters:
    ----------
        data (dict): data to save
        filename (str): name of the csv file
    """

    fieldnames = [
        "magasin_id",
        "product_id",
        "category",
        "subcategory",
        "sub_sub_category",
        "product name",
        "price/unity",
        "price",
        "nutri-score",
        "Valeur énergétique en kJ",
        "Valeur énergétique en kCal",
        "Matières grasses",
        "Dont acides gras saturés",
        "Dont acides gras mono-insaturés",
        "Glucides",
        "Dont sucres",
        "Protéines",
        "Fibres alimentaires",
        "Sel",
        "Sodium",
    ]

    # Remove unwanted data (mainly minor nutritional values)
    data = {key: value for key, value in data.items() if key in fieldnames}

    # Create the file if it doesn't exist
    if not os.path.isfile(os.path.dirname(PATH) + "/data/csv_files/" + filename):
        with open(
            os.path.dirname(PATH) + "/data/csv_files/" + filename,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    with open(
        os.path.dirname(PATH) + "/data/csv_files/" + filename,
        mode="a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)


def save_html_to_file(html_content, file_path):
    """
    Save html content to a file.

    Parameters:
    ----------
        html_content (str): The HTML content to be saved.
        file_path (str): The path to the file to be created.

    Returns:
    ----------
    None
    """
    file = open(file_path, "w", encoding="utf-8")
    file.write(html_content)

    file.close()
