import os

import requests
from bs4 import BeautifulSoup as bs
from utils import (
    PATH,
    clean_value,
    get_cookies_headers,
    rename_columns,
    save_product_info,
    save_supermarket_info,
)

MAIN_URL = "https://www.cora.fr"
cookies, headers = get_cookies_headers()


def get_supermarket_info(headers):
    """
    Get all the info of all the supermarkets

    Parameters:
    ----------
        headers (dict): headers to use for the request

    Returns:
    -------
        store_list (list of dict): list of all the supermarkets info
    """

    store_list = []

    for i in range(1, 200):
        response = requests.get(
            f"https://api.cora.fr/api/magasins/{i}", headers=headers
        )

        # if the status code is 200, it means that the supermarket exists
        if response.status_code == 200:
            print(f"Getting info for supermarket {i}...")

            data = response.json()["data"]["attributes"]

            store_data = {
                "magasin_id": i,
                "name": data["magasin"],
                "adress": data["adresse"],
                "postal code": data["cp"],
                "city": data["ville"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
            }

            store_list.append(store_data)

    return store_list


def get_categories(magasin_id=120):
    """
    Get all the categories of a specific supermarket

    Parameters:
    ----------
        magasin_id (int): id of the supermarket

    Returns:
    -------
        categories (list): list of all the categories
    """

    # set the magasin_id cookie in order to get the categories of the store
    cookies.__setitem__("magasin_id", str(magasin_id))

    print(f"Getting categories for supermarket {magasin_id}...")

    response_sub = requests.get(
        "https://www.cora.fr/faire_mes_courses-c-176362",
        cookies=cookies,
        headers=headers,
    )
    soup_sub = bs(response_sub.text, features="html.parser")

    categories = soup_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return categories[3:11]  # we take only category concerning food


def get_subcategories(category):
    """
    Get all the subcategories of a specific category

    Parameters:
    ----------
        category: category

    Returns:
    -------
        title_cat (str): title of the category
        subcategories (list): list of all the subcategories
    """

    link_rel = category.find(
        "a",
        class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
    ).get("href")
    link_abs = MAIN_URL + link_rel

    title_cat = category.find("div", class_="c-title-image__label").text.strip()

    print("Title cat: ", title_cat)

    # get all the subcategories
    response_sub = requests.get(link_abs, cookies=cookies, headers=headers)
    soup_sub = bs(response_sub.text, features="html.parser")

    subcategories = soup_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return title_cat, subcategories


def get_subsubcategories(subcat):
    """
    Get all the subcategories of a specific subcategory

    Parameters:
    ----------
        subcat: subcategory

    Returns:
    -------
        title_sub (str): title of the subcategory
        sub_subcategories (list): list of all the subcategories
    """

    link_rel_sub = subcat.find(
        "a",
        class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
    ).get("href")
    link_abs_sub = MAIN_URL + link_rel_sub

    title_sub = subcat.find("div", class_="c-title-image__label").text.strip()

    print("------Title sub: ", title_sub)

    # get all the subcategories
    response_sub_sub = requests.get(link_abs_sub, cookies=cookies, headers=headers)
    soup_sub_sub = bs(response_sub_sub.text, features="html.parser")

    sub_subcategories = soup_sub_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return title_sub, sub_subcategories


def get_product_info(id, headers, cookies):
    """
    Get all the info of a specific product

    Parameters:
    ----------
        id (str): id of the product
        headers (dict): headers to use for the request
        cookies (dict): cookies to use for the request

    Returns:
    -------
        res (dict): dict containing all the info of the product
    """

    # The price/um, the nutri-score and the nutritional values are not always available,
    # we add a try/except to check if they are available

    print(f"Getting product info for {id}...")

    response = requests.get(
        f"https://www.cora.fr/article/{id}/",
        headers=headers,
        cookies=cookies,
    )
    soup = bs(response.text, features="html.parser")

    try:
        price_um = clean_value(
            soup.find("p", "c-product-detail__unitPrice").text.strip()
        )
    except:
        price_um = None

    price = clean_value(soup.find("p", "c-price__amount").find_next().text.strip())

    prod_name = soup.find("h1", "c-product-detail__title").text.strip()

    try:
        nutri_score = soup.find("div", "c-product-detail__line").find(
            "picture", class_="c-product-detail__nutriscore"
        )
        if nutri_score is None:
            nutri_score = soup.find("div", "c-product-detail__line").find(
                "picture", class_="c-product-detail__nutriscore__first_picto"
            )
        nutri_score = nutri_score.find("img").get_attribute_list("alt")[0].split(" ")[1]
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


def get_products(sub_subcat, title_cat, title_sub):
    """
    Get all the products of a specific subsubcategory

    Parameters:
    ----------
        sub_subcat: subsubcategory
        title_cat (str): title of the category
        title_sub (str): title of the subcategory
    """

    link_rel_sub_sub = sub_subcat.find(
        "a",
        class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
    ).get("href")
    link_abs_sub_sub = MAIN_URL + link_rel_sub_sub

    title_sub_sub = sub_subcat.find("div", class_="c-title-image__label").text.strip()

    print("-------------Title sub sub: ", title_sub_sub)

    # get all the products
    i = 0

    while True:
        i += 1

        params = {
            "pageindex": str(i),
        }

        response_prod = requests.get(
            link_abs_sub_sub,
            params=params,
            cookies=cookies,
            headers=headers,
        )

        # if there is a redirect, break. This means that there are no more products in this subcategory
        if response_prod.history:
            break

        soup_prod = bs(response_prod.text, features="html.parser")

        prods = soup_prod.find(
            "ul",
            class_="c-list c-product-list-container-products c-product-list-container-products--grid",
        ).find_all(
            "li",
            class_="c-list__item c-product-list-container-products__item Desk_DP_Tuile c-product-list-container-products__item--grid",
        )

        for prod in prods:
            disabled = prod.find(
                "div", class_="c-product-list-item--grid__disabled-text"
            )

            # if the product is disabled, we do not get the info and we continue
            if disabled:
                continue

            id_prod = (
                prod.find(
                    "a",
                    class_="c-link-to c-product-list-item--grid__title c-link-to--hover-primary-light",
                )
                .get("href")
                .split("/")[2]
            )
            id_prod = str(id_prod)

            magasin_id = int(cookies["magasin_id"])

            data = {
                "magasin_id": magasin_id,
                "product_id": id_prod,
                "category": title_cat,
                "subcategory": title_sub,
                "sub_sub_category": title_sub_sub,
            }

            # get product info
            data.update(get_product_info(id_prod, headers, cookies))

            save_product_info(data, cookies["magasin_id"] + "_products" + ".csv")


def main():
    # first we get all the info of products of a specific supermarket
    categories = get_categories()

    for cat in categories:
        title_cat, subcategories = get_subcategories(cat)

        for subcat in subcategories:
            title_sub, sub_subcategories = get_subsubcategories(subcat)

            for sub_subcat in sub_subcategories:
                get_products(sub_subcat, title_cat, title_sub)

    # add unit of measure to csv header
    rename_columns(cookies["magasin_id"] + "_products" + ".csv")

    # then we get all the info of all the supermarkets

    # if the file already exists, we do not get the info again
    if not os.path.isfile((os.path.dirname(PATH) + "\data\\supermarkets.csv")):
        store_list = get_supermarket_info(headers)
        save_supermarket_info(store_list, "supermarkets" + ".csv")


if __name__ == "__main__":
    main()
