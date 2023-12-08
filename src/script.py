import requests
from bs4 import BeautifulSoup as bs

headers = {
    "authority": "api.cora.fr",
    "accept": "application/vnd.api.v1+json",
    "accept-language": "it-IT,it;q=0.8",
    "app-id": "1",
    "app-signature": "BROWSER;WEB;120.0.0.0;;1.50.4;1;2;Chrome;453;1536",
    "cache-control": "no-cache",
    "cora-auth": "apidrive",
    "origin": "https://www.cora.fr",
    "pragma": "no-cache",
    "referer": "https://www.cora.fr/",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "uuid": "9a1cd94a-33ce-49db-9663-5d5acd961bc9",
    "x-d-token": "3:8jmZyWCaZoeH4oduCZQ35Q==:SpNZSBzdvC6snUkfHexXtkzX1xv7TJBSOTcE3HVGk+dM3BG3gx2iKXU/Jq13ZjFIQ7G2lDT8UmMzN56S5Mu4U3wcaw6yyyhCzRfvUHWza1jgq7LfQ8rHaVfMgxPFKeO4+5i764do8AzPFoP7d/7T8yDlRR6r37vW++j9J1iH7ZaGzudJvd0fo/SRQGckS8SVD0hePdTzwBVzsMhGPXmO+oCQu7qQs4bRuCvWoVusC9W5lhkGaEL/tMsvcbGxcjmUnT6+ZcBP3qmm0ea/VB1HNukNnpBAQ2hmRWff9Cx5p1kXh57mO9yxNcStNT8kMUm6k6gLMy+F4xCDjLvJ939tWQUOvmoLeMS/+U4+OYdIrloA5WOo1rR49XUU8oE7oMv4Ob9R4ByNh+B8476gwfwTUSH1AN64reQHfSKkI6Mcnav4x632pjcnGqbtV0QiIQQqjfZV/tlhg5V7eOsLmkDVeVjKRGUfoV5kTuPD/bHER2zMcuMkJX6c2shzqi05fJMO4imF+VSMvO3cyvMrhVE0+A==:nPiaHspBdRrbhOIOKQCYv/paCiPPystmkoKdYXIlhlI=",
}

cookies = {
    "visid_incap_2483309": "avoloeIDSZuvWoa3hNXvZFr0cWUAAAAAQUIPAAAAAACX2ItXAlLwBBjPVC1eQFH2",
    "uuid": "9a1cd94a-33ce-49db-9663-5d5acd961bc9",
    "nlbi_2483309": "cokVYBgB6TmFdXBKJag8ewAAAAD92EECCs6RXVj+4VLaJ3sQ",
    "visid_incap_2346747": "HDYV5FRQSnqXgqU6/+eHzMPbcmUAAAAAQUIPAAAAAAAhf7TWmGpDjVu2b+V3rey+",
    "nlbi_2346747": "pZK4Miv/TT65lAGLrtkoMQAAAAAUu0FjvZjSfL/KJZICV8Du",
    "incap_ses_1516_2483309": "Fz9EfKp/cj19EZV4reoJFbfqcmUAAAAA7EkHW5sPIJi+yTwovxfmJQ==",
    "incap_ses_1516_2346747": "4kGuBCI1Xh5WUpx4reoJFdTtcmUAAAAAG4L2065/zy4iYJBzldv5Og==",
    "incap_ses_467_2483309": "La8xIp1RHCc06/cKuh97BsxKc2UAAAAAZAFa89CyIPtoDMIGa0EVZw==",
    "show-first-landing-popin": "4",
    "reese84": "3:JePL6X+ewLGj7L+1z7FpWg==:n6rlJKxq2fNJLemScWMB7kR9fEf7OOiCyURlw4E51BSXucYU+G1R4Dp7LHKDvDP8Rt+ESg/kCocON6kUBgcsUg/KhNdahOG91y4bAuSRdGjXdU3Re31VvqWgQBNHJSIzrfcXypl+GlkHYaqZznyBRgjaXeNmp3KjrjnCZLit5yq1NoIEvIcSbO5HIOx8VKLVA//Bo4t8TvzBWCPFVZufblI3M83POY+s2e9mXNehm78HAqNsqRdXhDGlL6Y4IAlEV2nh3unHlhj63kE9EDzMqCZFbdn7XkY5hT8Itx2y3cZ2XURuIZ6KzglY41gaXUrWT+nJ2a2UDVGOBswhpt6JC7SZZl9sY4gQGO0SaAi/6a10YbXxPb6jvGINNtuzgq/1w9nrhERkRl1MdlKTVV2b32/53E7zKhPrAudAkYsAyiTuQ7UKKaNP0roexwT/KZMEfa6TZz6rGqL1jXIjTSQB3imXbDlk9UkExcTNHEmfFsLBY6aX4+NgA30uGMDLBGvD3CLkB/er0muut/ACkt3M9A==:bviO30gX4K1+Nr7jzxgjbfrG+8f8DTCtfTtDqlilx+M=",
    "nlbi_2483309_2147483392": "aIvfDIOIDkBD1np+Jag8ewAAAADNq22WkXk2um9jdxHbkNpZ",
    "visid_incap_2347167": "IT1rnkOYRo2zTYaSx5GZBFBNc2UAAAAAQUIPAAAAAADGHwrqKFKU2OWnjdQslxSu",
    "incap_ses_467_2347167": "xcymbyCo80qfK/wKuh97BlBNc2UAAAAAZALD0oSA+y0jJ/v5w5fZQA==",
    "magasin_id": "147",
}


def get_supermarket_info():
    store_list = []

    for i in range(1, 200):
        response = requests.get(
            f"https://api.cora.fr/api/magasins/{i}", headers=headers
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


def get_product_info(id):
    response = requests.get(
        f"https://www.cora.fr/article/{id}/",
        headers=headers,
        cookies=cookies,
    )

    soup = bs(response.text, "html.parser")

    price_kg = soup.find("p", "c-product-detail__unitPrice").text.strip()
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

    res = {
        "price/kg": price_kg,
        "price": price,
        "product name": prod_name,
        "nutri-score": nutri_score,
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


main()
