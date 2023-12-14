import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

from datetime import datetime
from script import get_product_info

MAIN_URL = "https://www.cora.fr"

def main():
    df = pd.DataFrame()

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
        "magasin_id": "120",
    }

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


    # headers = {
    #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    #     # 'Accept-Encoding': 'gzip, deflate, br',
    #     "Connection": "keep-alive",
    #     # 'Cookie': 'visid_incap_2483309=DJ+ltefNRJ2QxFDd9uFs2HpicGUAAAAAQUIPAAAAAACvUU/aqsTVaXjO8ROgqKN4; uuid=0f53236c-b53d-4ac9-9f22-41e591b30278; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22e9dae216-cbaa-4903-ba7b-b937dbeeb8c5%22%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T12%3A01%3A00.220Z%22%2C%22path%22%3A%22%2F%22%7D%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Dec+08+2023+17%3A17%3A29+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=31f75c1a-0dcb-4caf-b8da-42ea56ecab21&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0001%3A1%2CC0002%3A0&geolocation=%3B&AwaitingReconsent=false; reese84=3:EA+dseAfehT30MX/XzhIrg==:e21qaCMAoFP8cnhUpLRPSMSE8yh/5/m4POYcSOTGc+XK6BtsFwRbQvAcLCQSl4oo/adU8vlm25FjWNFaqaY7b4iBpOLhMGI/v1oueS7U28RyBw9jINi/NPuJ67neWhv0/vtnDrS238lTlO+qPi50ARkUQPAEKuq+KI+y2ONufj/MlmsiV6jMae2EqG2bdZG/5D43mwfgBCCczAJyb2gQSXwW1QuaIW5mhJOxqGuvO/jtsYeS2sJuT9Trs+fBMxaf8VfKiuN7UbBamgUe3HeaIBdFokghPrLuhYAhWhlCnbwDW3qcVg/BDHgztC6OHnySIzws5NgJvCyU9GVsCeYOuBgvf4Xg/WdwSv3V6LplnEPW+SgYnPGDoh9QOe57xaVuZZbDUia5NczpgXW9mfNlOxT8reh+cFr4FV8dhBDXW8jufuelGR2iJUrRpQgp6STyllyCesnnkdDvv+XmV1hRyc0hDn9KlvL36aRUJznaE4R1lH5lahW71SbJQ7zjhqDerxYH9c/sqzefzpK1YrhI1Q==:sgjV0IFmkQKLqoX7qRxLIS0VvNBTFgREj0WVQUdIu6s=; OptanonAlertBoxClosed=2023-12-06T12:01:04.793Z; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-01-08T16%3A17%3A28.649Z%22%2C%22path%22%3A%22%2F%22%7D%7D; magasin_id=120; visid_incap_2347167=ipXvHdwrTnCRNdZRGAXgDWFjcGUAAAAAQUIPAAAAAABDAX0L0UDGv6Sc6goGiyCx; nlbi_2483309=/bhBMC1mcWFvcqTDJag8ewAAAAAemYFjl+VPJL3ZJBZJ1h3W; incap_ses_467_2483309=AtBcc1wE5jHyu+QKuh97Bmk/c2UAAAAAGq9qfjdSrGwVvra4oS5fTQ==; nlbi_2483309_2147483392=6IvNI4dKW2NeiYWcJag8ewAAAAD/hsHyDOQejSPIDRbM4f2f; show-first-landing-popin=4',
    #     "Upgrade-Insecure-Requests": "1",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "none",
    #     "Sec-Fetch-User": "?1",
    #     # Requests doesn't support trailers
    #     # 'TE': 'trailers',
    # }

    # Faire mes courses page. In order to get all the categories we are interested in
    response_sub = requests.get(
        "https://www.cora.fr/faire_mes_courses-c-176362",
        cookies=cookies,
        headers=headers,
    )
    soup_sub = bs(response_sub.text, features="html.parser")

    # Get all the categories
    categories = soup_sub.find(
        "ul", class_="c-list children-categories__list"
    ).find_all("li", class_="c-list__item children-categories__list-item")
    # categories = categories[3:-6]
    categories = categories[7:8] #surgeles

    for cat in categories:
        link_rel = cat.find(
            "a",
            class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
        ).get("href")
        link_abs = MAIN_URL + link_rel

        title_cat = cat.find("div", class_="c-title-image__label").text.strip()

        print("Title cat: ", title_cat)

        # Get all the subcategories
        response_sub = requests.get(link_abs, cookies=cookies, headers=headers)
        soup_sub = bs(response_sub.text, features="html.parser")

        subcategories = soup_sub.find(
            "ul", class_="c-list children-categories__list"
        ).find_all("li", class_="c-list__item children-categories__list-item")

        for subcat in subcategories:
            link_rel_sub = subcat.find(
                "a",
                class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
            ).get("href")
            link_abs_sub = MAIN_URL + link_rel_sub

            title_sub = subcat.find("div", class_="c-title-image__label").text.strip()

            print("------Title sub: ", title_sub)

            # Get all the subcategories
            response_sub_sub = requests.get(
                link_abs_sub, cookies=cookies, headers=headers
            )
            soup_sub_sub = bs(response_sub_sub.text, features="html.parser")

            sub_subcategories = soup_sub_sub.find(
                "ul", class_="c-list children-categories__list"
            ).find_all("li", class_="c-list__item children-categories__list-item")

            for sub_subcat in sub_subcategories:
                link_rel_sub_sub = sub_subcat.find(
                    "a",
                    class_="c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border",
                ).get("href")
                link_abs_sub_sub = MAIN_URL + link_rel_sub_sub

                title_sub_sub = sub_subcat.find(
                    "div", class_="c-title-image__label"
                ).text.strip()

                print("-------------Title sub sub: ", title_sub_sub)

                # Get all the products
                i = 0
                info = []
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

                    # If there is a redirect, break. This means that there are no more products in this subcategory
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
                        
                        disabled = prod.find("div", class_="c-product-list-item--grid__disabled-text")

                        if disabled:
                            continue

                        id_prod = prod.find("a", class_="c-link-to c-product-list-item--grid__title c-link-to--hover-primary-light").get("href").split("/")[2]
                        id_prod = str(id_prod)

                        # Get product info
                        data = get_product_info(id_prod, headers, cookies)

                        # save information in dictionary
                        data["category"] = title_cat
                        data["subcategory"] = title_sub
                        data["sub_sub_category"] = title_sub_sub

                        info.append(data)

                d2 = pd.DataFrame.from_dict(info)
                if df.empty:
                    df = d2
                else:
                    df = pd.concat([df, d2])

                print(df)
                break # Only first subsubcategory

            break # Only first subcategory

        break # Only first category
        
        print()

    # print(df)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(timestamp+"_cora.csv", index=False)


if __name__ == "__main__":
    main()
