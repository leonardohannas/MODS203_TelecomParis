import csv
import json
import os
import re

import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))


def rename_columns(filename):
    df = pd.read_csv(os.path.dirname(PATH) + "\data\\" + filename)

    columns = {
        "price/um": "price/u [€/u.m]",
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

    df.to_csv(os.path.dirname(PATH) + "\data\\" + filename, index=False)


def clean_value(text):
    text_match = re.search(r"(\d+([.,]{1}\d{1,2}){1}?)", text)
    if text_match:
        float_value = float(text_match.group(1).replace(",", "."))
    else:
        float_value = None

    return float_value


def get_cookies_headers(filename="config.json"):
    try:
        with open(PATH + "/" + filename, "r") as file:
            config = json.load(file)
            return config.get("cookies", {}), config.get("headers", {})
    except FileNotFoundError:
        print("File not found")


def save_supermarket_info(data, filename):
    df = pd.DataFrame(data)

    df.to_csv(os.path.dirname(PATH) + "\data\\" + filename, index=False)


def save_product_info(data, filename):
    fieldnames = [
        "magasin_id",
        "product_id",
        "category",
        "subcategory",
        "sub_sub_category",
        "product name",
        "price/um",
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
    if not os.path.isfile(os.path.dirname(PATH) + "\data\\" + filename):
        with open(
            os.path.dirname(PATH) + "\data\\" + filename,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    with open(
        os.path.dirname(PATH) + "\data\\" + filename,
        mode="a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the data
        writer.writerow(data)
