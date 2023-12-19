import requests
from bs4 import BeautifulSoup as bs
import re

def get_supermarket_info(headers):
    store_list = []

    for i in range(1, 200):
        response = requests.get(
            f"https://api.cora.fr/api/magasins/{i}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()["data"]["attributes"]

            store_data = {
                "id": i,
                "magasin": data["magasin"],
                "adresse": data["adresse"],
                "cp": data["cp"],
                "ville": data["ville"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
            }

            store_list.append(store_data)

    return store_list


def clean_value(text):
    text_match = re.search(r'(\d+([.,]{1}\d{1,2}){1}?)', text)
    if text_match:
        float_value = float(text_match.group(1).replace(',', '.'))
    else:
        float_value = None
    
    return float_value


def get_product_info(id, headers, cookies):

    print(f"Getting product info for {id}...")

    response = requests.get(
        f"https://www.cora.fr/article/{id}/",
        headers=headers,
        cookies=cookies,
    )
    soup = bs(response.text, features="html.parser")

    try:
        price_um = clean_value(soup.find("p", "c-product-detail__unitPrice").text.strip())
    except:
        price_um = None

    price = clean_value(soup.find("p", "c-price__amount").find_next().text.strip())

    prod_name = soup.find("h1", "c-product-detail__title").text.strip()

    try:
        nutri_score = (
            soup.find("picture", "c-product-detail__nutriscore")
            .find_next()
            .get_attribute_list("alt")[0]
            .split(" ")[1]
        )
    except:
        nutri_score = None

    res = {
        "price/um": price_um,
        "price": price,
        "product name": prod_name,
        "nutri-score": nutri_score,
    }

    try:
        nut_table = soup.find("div", "c-nutritional-values__table")

        for row in nut_table.find_all("tr"):
            columns = row.find_all(["th", "td"])

            if len(columns) == 2 and len(columns[0]) > 0:
                nutrient = columns[0].get_text(strip=True)
                value = clean_value(columns[1].get_text(strip=True))
                res[nutrient] = value
    except:
        pass
         
    return res


def rename_columns(df):
    columns = {
        "price/um": "price/u [€/u.m]",
        "price": "price [€]",
        "Valeur énergétique en kJ": "Valeur énergétique [kJ]",
        "Valeur énergétique en kCal": "Valeur énergétique [kCal]",
        "Matières grasses": "Matières grasses [g]",
        "Dont acides gras saturés": "Dont acides gras saturés [g]",
        "Glucides": "Glucides [g]",
        "Dont sucres": "Dont sucres [g]",
        "Protéines": "Protéines [g]",
        "Sel": "Sel [g]",
        "Fibres alimentaires": "Fibres alimentaires [g]",
        "Sodium": "Sodium [mg]",
        "Acide gras Omega 3": "Acide gras Omega 3 [g]",
    }

    return df.rename(columns=columns)


def main():
    # stores_info = get_supermarket_info()
    res = get_product_info(13858)
    print(res)

if __name__ == "__main__":
    main()
