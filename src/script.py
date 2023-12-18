import requests
from bs4 import BeautifulSoup as bs

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


def get_product_info(id, headers, cookies):

    print(f"Getting product info for {id}...")

    response = requests.get(
        f"https://www.cora.fr/article/{id}/",
        headers=headers,
        cookies=cookies,
    )
    soup = bs(response.text, features="html.parser")

    try:
        price_kg = soup.find("p", "c-product-detail__unitPrice").text.strip()
    except:
        price_kg = None

    price = soup.find("p", "c-price__amount").find_next().text.strip()

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

    magasin_id = int(cookies["magasin_id"])

    res = {
        "price/kg": price_kg,
        "price": price,
        "product name": prod_name,
        "nutri-score": nutri_score,
        "magasin_id": magasin_id,
    }

    try:
        nut_table = soup.find("div", "c-nutritional-values__table")

        for row in nut_table.find_all("tr"):
            columns = row.find_all(["th", "td"])

            if len(columns) == 2 and len(columns[0]) > 0:
                nutritional_value = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)
                res[nutritional_value] = value
    except:
        pass
         
    return res


def main():
    # stores_info = get_supermarket_info()
    res = get_product_info(13858)
    print(res)

if __name__ == "__main__":
    main()
