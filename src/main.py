import requests
from bs4 import BeautifulSoup as bs

import pandas as pd

MAIN_URL = 'https://www.cora.fr'

def main():

    columns = ['title', 'nutriScore', 'price', 'price_kg_u', 'category', 'subcategory']
    df = pd.DataFrame(columns=columns)
    
    cookies = {
        'visid_incap_2483309': 'DJ+ltefNRJ2QxFDd9uFs2HpicGUAAAAAQUIPAAAAAACvUU/aqsTVaXjO8ROgqKN4',
        'uuid': '0f53236c-b53d-4ac9-9f22-41e591b30278',
        'atuserid': '%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22e9dae216-cbaa-4903-ba7b-b937dbeeb8c5%22%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T12%3A01%3A00.220Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Dec+08+2023+17%3A17%3A29+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=31f75c1a-0dcb-4caf-b8da-42ea56ecab21&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0001%3A1%2CC0002%3A0&geolocation=%3B&AwaitingReconsent=false',
        'reese84': '3:EA+dseAfehT30MX/XzhIrg==:e21qaCMAoFP8cnhUpLRPSMSE8yh/5/m4POYcSOTGc+XK6BtsFwRbQvAcLCQSl4oo/adU8vlm25FjWNFaqaY7b4iBpOLhMGI/v1oueS7U28RyBw9jINi/NPuJ67neWhv0/vtnDrS238lTlO+qPi50ARkUQPAEKuq+KI+y2ONufj/MlmsiV6jMae2EqG2bdZG/5D43mwfgBCCczAJyb2gQSXwW1QuaIW5mhJOxqGuvO/jtsYeS2sJuT9Trs+fBMxaf8VfKiuN7UbBamgUe3HeaIBdFokghPrLuhYAhWhlCnbwDW3qcVg/BDHgztC6OHnySIzws5NgJvCyU9GVsCeYOuBgvf4Xg/WdwSv3V6LplnEPW+SgYnPGDoh9QOe57xaVuZZbDUia5NczpgXW9mfNlOxT8reh+cFr4FV8dhBDXW8jufuelGR2iJUrRpQgp6STyllyCesnnkdDvv+XmV1hRyc0hDn9KlvL36aRUJznaE4R1lH5lahW71SbJQ7zjhqDerxYH9c/sqzefzpK1YrhI1Q==:sgjV0IFmkQKLqoX7qRxLIS0VvNBTFgREj0WVQUdIu6s=',
        'OptanonAlertBoxClosed': '2023-12-06T12:01:04.793Z',
        'atauthority': '%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-01-08T16%3A17%3A28.649Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
        'magasin_id': '120',
        'visid_incap_2347167': 'ipXvHdwrTnCRNdZRGAXgDWFjcGUAAAAAQUIPAAAAAABDAX0L0UDGv6Sc6goGiyCx',
        'nlbi_2483309': '/bhBMC1mcWFvcqTDJag8ewAAAAAemYFjl+VPJL3ZJBZJ1h3W',
        'incap_ses_467_2483309': 'AtBcc1wE5jHyu+QKuh97Bmk/c2UAAAAAGq9qfjdSrGwVvra4oS5fTQ==',
        'nlbi_2483309_2147483392': '6IvNI4dKW2NeiYWcJag8ewAAAAD/hsHyDOQejSPIDRbM4f2f',
        'show-first-landing-popin': '4',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Cookie': 'visid_incap_2483309=DJ+ltefNRJ2QxFDd9uFs2HpicGUAAAAAQUIPAAAAAACvUU/aqsTVaXjO8ROgqKN4; uuid=0f53236c-b53d-4ac9-9f22-41e591b30278; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22e9dae216-cbaa-4903-ba7b-b937dbeeb8c5%22%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T12%3A01%3A00.220Z%22%2C%22path%22%3A%22%2F%22%7D%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Dec+08+2023+17%3A17%3A29+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=31f75c1a-0dcb-4caf-b8da-42ea56ecab21&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0001%3A1%2CC0002%3A0&geolocation=%3B&AwaitingReconsent=false; reese84=3:EA+dseAfehT30MX/XzhIrg==:e21qaCMAoFP8cnhUpLRPSMSE8yh/5/m4POYcSOTGc+XK6BtsFwRbQvAcLCQSl4oo/adU8vlm25FjWNFaqaY7b4iBpOLhMGI/v1oueS7U28RyBw9jINi/NPuJ67neWhv0/vtnDrS238lTlO+qPi50ARkUQPAEKuq+KI+y2ONufj/MlmsiV6jMae2EqG2bdZG/5D43mwfgBCCczAJyb2gQSXwW1QuaIW5mhJOxqGuvO/jtsYeS2sJuT9Trs+fBMxaf8VfKiuN7UbBamgUe3HeaIBdFokghPrLuhYAhWhlCnbwDW3qcVg/BDHgztC6OHnySIzws5NgJvCyU9GVsCeYOuBgvf4Xg/WdwSv3V6LplnEPW+SgYnPGDoh9QOe57xaVuZZbDUia5NczpgXW9mfNlOxT8reh+cFr4FV8dhBDXW8jufuelGR2iJUrRpQgp6STyllyCesnnkdDvv+XmV1hRyc0hDn9KlvL36aRUJznaE4R1lH5lahW71SbJQ7zjhqDerxYH9c/sqzefzpK1YrhI1Q==:sgjV0IFmkQKLqoX7qRxLIS0VvNBTFgREj0WVQUdIu6s=; OptanonAlertBoxClosed=2023-12-06T12:01:04.793Z; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-01-08T16%3A17%3A28.649Z%22%2C%22path%22%3A%22%2F%22%7D%7D; magasin_id=120; visid_incap_2347167=ipXvHdwrTnCRNdZRGAXgDWFjcGUAAAAAQUIPAAAAAABDAX0L0UDGv6Sc6goGiyCx; nlbi_2483309=/bhBMC1mcWFvcqTDJag8ewAAAAAemYFjl+VPJL3ZJBZJ1h3W; incap_ses_467_2483309=AtBcc1wE5jHyu+QKuh97Bmk/c2UAAAAAGq9qfjdSrGwVvra4oS5fTQ==; nlbi_2483309_2147483392=6IvNI4dKW2NeiYWcJag8ewAAAAD/hsHyDOQejSPIDRbM4f2f; show-first-landing-popin=4',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    # Faire mes courses page. In order to get all the categories we are interested in
    response_sub = requests.get('https://www.cora.fr/faire_mes_courses-c-176362', cookies=cookies, headers=headers)
    soup_sub = bs(response_sub.text, features="html.parser")

    # Get all the categories
    categories = soup_sub.find('ul', class_='c-list children-categories__list').find_all('li', class_='c-list__item children-categories__list-item')
    categories = categories[3:-5]

    for cat in categories:
        link_rel = cat.find('a', class_='c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border').get('href')
        link_abs = MAIN_URL+link_rel

        title_cat = cat.find('div', class_='c-title-image__label').text.strip()

        print("Title cat: ", title_cat)

        # Get all the subcategories
        response_sub = requests.get(link_abs, cookies=cookies, headers=headers)
        soup_sub = bs(response_sub.text, features="html.parser")

        subcategories = soup_sub.find('ul', class_='c-list children-categories__list').find_all('li', class_='c-list__item children-categories__list-item')

        for subcat in subcategories:
            link_rel_sub = subcat.find('a', class_='c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border').get('href')
            link_abs_sub = MAIN_URL+link_rel_sub

            title_sub = subcat.find('div', class_='c-title-image__label').text.strip()

            print("------Title sub: ", title_sub)

            # Get all the subcategories
            response_sub_sub = requests.get(link_abs_sub, cookies=cookies, headers=headers)
            soup_sub_sub = bs(response_sub_sub.text, features="html.parser")

            sub_subcategories = soup_sub_sub.find('ul', class_='c-list children-categories__list').find_all('li', class_='c-list__item children-categories__list-item')

            for sub_subcat in sub_subcategories:
                link_rel_sub_sub = sub_subcat.find('a', class_='c-title-image c-children-categories__item c-button c-title-image--radius-full c-title-image--border').get('href')
                link_abs_sub_sub = MAIN_URL+link_rel_sub_sub

                title_sub_sub = sub_subcat.find('div', class_='c-title-image__label').text.strip()

                print("-------------Title sub sub: ", title_sub_sub)

                # Get all the products
                i=0
                info = []
                while True:
                    i+=1

                    params = {
                        'pageindex': str(i),
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

                    prods = soup_prod.find('ul', class_='c-list c-product-list-container-products c-product-list-container-products--grid').find_all('li', class_='c-list__item c-product-list-container-products__item Desk_DP_Tuile c-product-list-container-products__item--grid')

                    for prod in prods:

                        title_prod = prod.find('h2',class_='c-product-list-item__intitule-slice').get_text()
                        #clean title
                        title_prod = title_prod.replace('\n','').strip()

                        price = prod.find('p', class_='c-price__amount').find('span').get_text()
                        price = float(price.replace(',','.'))

                        try:
                            price_kg_u = prod.find('p', class_='c-product-list-item__unit-price u-mt-xs').find('span').get_text()
                            price_kg_u = float(price_kg_u.split()[0].replace(',', '.'))
                        except:
                            price_kg_u = None

                        try:
                            nutri = prod.find('div', class_='c-product-list-item--grid__score-promo-slice').find('picture').find('img')['alt'][-1]
                            #clean nutri
                            nutri = nutri.replace('\n','').strip()
                        except:
                            nutri = None

                        # save information in dictionary
                        data = dict()
                        data['title'] = title_prod
                        data['nutriScore'] = nutri
                        data['price'] = price
                        data['price_kg_u'] = price_kg_u
                        data['category'] = title_cat
                        data['subcategory'] = title_sub
                        data['sub_sub_category'] = title_sub_sub
                        
                        info.append(data)

                d2 = pd.DataFrame.from_dict(info)
                if df.empty:
                    df = d2
                else:
                    df = pd.concat([df, d2])

                print()

                # break # Only first subsubcategory

            # break # Only first subcategory

        # break # Only first category

    # print(df)
    df.to_csv('231208cora.csv', index=True)

if __name__ == "__main__":
    main()