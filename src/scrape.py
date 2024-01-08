import os
import random
import sys
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from utils import (
    PATH,
    clean_value,
    get_cookies_headers,
    rename_columns,
    save_html_to_file,
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
    ----------
        store_list (list of dict): list of all the supermarkets info
    """

    store_list = []

    for i in range(1, 200):
        response = requests.get(
            f"https://api.cora.fr/api/magasins/{i}", headers=headers
        )

        response_text = response.text

        # if the status code is 200, it means that the supermarket exists
        if response.status_code == 200:
            # Create new folder for that supermarket
            if not os.path.exists(
                os.path.dirname(PATH) + f"/data/html_files/store_{i}"
            ):
                os.mkdir(os.path.dirname(PATH) + f"/data/html_files/store_{i}")

            # Saving the response in a html file.
            file_name = f"store_info_{i}.html"
            file_path = (
                os.path.dirname(PATH) + f"/data/html_files/store_{i}/" + file_name
            )
            save_html_to_file(response_text, file_path)

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
    ----------
        categories (list): list of all the categories
    """

    # set the magasin_id cookie in order to get the categories of the store
    cookies.__setitem__("magasin_id", str(magasin_id))

    print(f"Getting categories for supermarket {magasin_id}...")

    file_name = f"categories.html"
    file_path = (
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/"
        + file_name
    )

    # If the html file does not exist, we get it from the web and save it
    if not os.path.isfile(file_path):
        response_sub = requests.get(
            "https://www.cora.fr/faire_mes_courses-c-176362",
            cookies=cookies,
            headers=headers,
        )

        response_text = response_sub.text
        save_html_to_file(response_text, file_path)
    else:
        with open(file_path, "r", encoding="utf8") as file:
            response_text = file.read()

    soup_sub = bs(response_text, features="html.parser")

    categories = soup_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return categories[4:12]  # we take only category concerning food


def get_subcategories(category):
    """
    Get all the subcategories of a specific category

    Parameters:
    ----------
        category: category

    Returns:
    ----------
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

    # Create new folder for that category
    if not os.path.exists(
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/"
    ):
        os.mkdir(
            os.path.dirname(PATH)
            + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/"
        )

    file_name = f"cat_{title_cat}.html"
    file_path = (
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/"
        + file_name
    )

    # If the html file does not exist, we get it from the web and save it
    if not os.path.isfile(file_path):
        # Get all the subcategories
        response_sub = requests.get(
            link_abs,
            cookies=cookies,
            headers=headers,
        )

        response_text = response_sub.text
        save_html_to_file(response_text, file_path)
    else:
        with open(file_path, "r", encoding="utf8") as file:
            response_text = file.read()

    soup_sub = bs(response_text, features="html.parser")

    subcategories = soup_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return title_cat, subcategories


def get_subsubcategories(title_cat, subcat):
    """
    Get all the subcategories of a specific subcategory

    Parameters:
    ----------
        title_cat (str): title of the category
        subcat: subcategory

    Returns:
    ----------
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

    # Create new folder for that sub_category
    if not os.path.exists(
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/"
    ):
        os.mkdir(
            os.path.dirname(PATH)
            + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/"
        )

    file_name = f"subcategory_{title_sub}.html"
    file_path = (
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/"
        + file_name
    )

    # If the html file does not exist, we get it from the web and save it
    if not os.path.isfile(file_path):
        # Get all the subcategories
        response_sub_sub = requests.get(
            link_abs_sub,
            cookies=cookies,
            headers=headers,
        )

        response_text = response_sub_sub.text
        save_html_to_file(response_text, file_path)
    else:
        with open(file_path, "r", encoding="utf8") as file:
            response_text = file.read()

    soup_sub_sub = bs(response_text, features="html.parser")

    sub_subcategories = soup_sub_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")

    return title_sub, sub_subcategories


def get_product_info(id, headers, cookies, title_cat, title_sub, title_sub_sub):
    """
    Get all the info of a specific product

    Parameters:
    ----------
        id (str): id of the product
        headers (dict): headers to use for the request
        cookies (dict): cookies to use for the request
        title_cat (str): title of the category
        title_sub (str): title of the subcategory
        title_sub_sub (str): title of the subsubcategory

    Returns:
    ----------
        res (dict): dict containing all the info of the product
    """

    # The price/unity, the nutri-score and the nutritional values are not always available,
    # we add a try/except to check if they are available

    print(f"Getting product info for {id}...")

    # Create new folder for that products
    if not os.path.exists(
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/products/"
    ):
        os.mkdir(
            os.path.dirname(PATH)
            + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/products/"
        )

    # Cheking if the file already exists.
    file_name = f"product_{id}.html"
    file_path = (
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/products/"
        + file_name
    )

    # If the html file does not exist, we get it from the web and save it
    if not os.path.isfile(file_path):
        response = requests.get(
            f"https://www.cora.fr/article/{id}/",
            headers=headers,
            cookies=cookies,
        )

        response_text = response.text
        save_html_to_file(response_text, file_path)

        # Random sleep between requests
        time.sleep(random.randint(100, 1000) / 1000)
    else:
        with open(file_path, "r", encoding="utf8") as file:
            response_text = file.read()

    soup = bs(response_text, features="html.parser")

    try:
        price_unity = clean_value(
            soup.find("p", "c-product-detail__unitPrice").text.strip()
        )
    except Exception as e:
        print(
            f"Error trying to clean/retrieve price/unity for product {id} and store {cookies['magasin_id']}.\nError: {e}",
            file=sys.stderr,
        )
        price_unity = None

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
        "price/unity": price_unity,
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

    # Create new folder for that sub_sub_category
    if not os.path.exists(
        os.path.dirname(PATH)
        + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/"
    ):
        os.mkdir(
            os.path.dirname(PATH)
            + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/"
        )

    # get all the products
    i = 0
    while True:
        i += 1

        # Cheking if the file already exists.
        file_name = f"subsubcategory_{title_sub_sub}_page_{i}.html"
        file_path = (
            os.path.dirname(PATH)
            + f"/data/html_files/store_{cookies['magasin_id']}/{title_cat}/{title_sub}/{title_sub_sub}/"
            + file_name
        )

        # If the html file does not exist, we get it from the web and save it
        if not os.path.isfile(file_path):
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

            response_text = response_prod.text
            save_html_to_file(response_text, file_path)
        else:
            with open(file_path, "r", encoding="utf8") as file:
                response_text = file.read()

        soup_prod = bs(response_text, features="html.parser")

        prods = soup_prod.find(
            "ul",
            class_="c-list c-product-list-container-products c-product-list-container-products--grid",
        ).find_all(
            "li",
            class_="c-list__item c-product-list-container-products__item Desk_DP_Tuile c-product-list-container-products__item--grid",
        )

        for prod in prods:
            disabled = prod.find(
                "div",
                class_="c-product-list-item__disabled c-product-list-item--grid__disabled",
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

            # get and save product info
            # If something goes bad, we caught the exception and print it.
            try:
                data.update(
                    get_product_info(
                        id_prod, headers, cookies, title_cat, title_sub, title_sub_sub
                    )
                )
                save_product_info(
                    data, "store_" + cookies["magasin_id"] + "_products" + ".csv"
                )
            except Exception as e:
                print(
                    f"An error occurred while scraping the product {id_prod} of the store {cookies['magasin_id']}. Cat: {title_cat}, subCat: {title_sub}, subSubCat: {title_sub_sub}.\nError: {e}",
                    file=sys.stderr,
                )
                print("Skipping product...")


def main():
    # we get all the info of all the supermarkets

    # if the file already exists, we do not retrieve the info again
    if not os.path.isfile((os.path.dirname(PATH) + "/data/supermarkets.csv")):
        print("Getting supermarkets info from the web...")
        store_list = get_supermarket_info(headers)
        save_supermarket_info(store_list, "supermarkets" + ".csv")
        # stores_info = pd.DataFrame(store_list)
        # print(stores_info.head())
    else:
        # we get the info about the stores from the supermarkets.csv file
        print("Getting supermarkets info from the csv file...")
        stores_info = pd.read_csv(os.path.dirname(PATH) + "/data/supermarkets.csv")

    # we get the id of the stores
    stores_id = stores_info["magasin_id"].tolist()

    # since the info about the store is in the cookie, we modify the cookies with the id of the store
    for store_id in stores_id:
        # first we get all the info of products of a specific supermarket
        try:
            categories = get_categories(store_id)
        except Exception as e:
            print(
                f"An error occurred while scraping the categories of the store {store_id}.\nError: {e}",
                file=sys.stderr,
            )
            continue

        for cat in categories:
            try:
                title_cat, subcategories = get_subcategories(cat)
            except Exception as e:
                print(
                    f"An error occurred while scraping the subcategories of the store {store_id}.\nError: {e}",
                    file=sys.stderr,
                )
                continue

            for subcat in subcategories:
                try:
                    title_sub, sub_subcategories = get_subsubcategories(
                        title_cat, subcat
                    )
                except Exception as e:
                    print(
                        f"An error occurred while scraping the subsubcategories of the store {store_id}.\nError: {e}",
                        file=sys.stderr,
                    )
                    continue

                for sub_subcat in sub_subcategories:
                    try:
                        get_products(sub_subcat, title_cat, title_sub)
                    except Exception as e:
                        print(
                            f"An error occurred while scraping the products of the store {store_id}.\nError: {e}",
                            file=sys.stderr,
                        )
                        continue

        # add unit of measure to csv header
        try:
            rename_columns("store_" + cookies["magasin_id"] + "_products" + ".csv")
        except Exception as e:
            print(
                f"An error occurred while renaming the columns of the store {store_id}.\nError: {e}",
                file=sys.stderr,
            )
            continue


if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(PATH) + "/data/html_files"):
        os.mkdir(os.path.dirname(PATH) + "/data/html_files")

    if not os.path.exists(os.path.dirname(PATH) + "/data/logs"):
        os.mkdir(os.path.dirname(PATH) + "/data/logs")

    if not os.path.exists(os.path.dirname(PATH) + "/data/csv_files"):
        os.mkdir(os.path.dirname(PATH) + "/data/csv_files")

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y%m%d_%H%M%S")

    with open(
        os.path.dirname(PATH) + "/data/logs/" + formatted_time + "_errors.txt",
        "w",
        encoding="utf8",
    ) as file:
        # Redirect stdout to the file
        sys.stderr = file
        print("Init...\n", file=sys.stderr)

        main()
