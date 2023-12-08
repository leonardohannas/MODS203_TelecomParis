import requests
from bs4 import BeautifulSoup as bs

import pandas as pd

cookies = {
    'visid_incap_2483309': '7ZzVRalVQTS72xJVEqR5A56kcGUAAAAAQUIPAAAAAAC7GsrV967iLFDKSBQ8x/MJ',
    'nlbi_2483309': 'zPqMamiQ6wC2ZwIsJag8ewAAAAD50aX1VNIsBgvmBiZVdZUm',
    'incap_ses_467_2483309': 'caiTPOiYNF4nm5sHuh97Bp6kcGUAAAAAbdjdtnCkcxWRqkvDIVQaKA==',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Dec+06+2023+17%3A46%3A00+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=ff0d2c54-74d4-4446-92e7-8178ca31424d&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0001%3A1%2CC0002%3A0&geolocation=%3B&AwaitingReconsent=false',
    'uuid': 'd1d24f33-ff02-47dc-9de6-bfa41526bf74',
    'first-landing-change-shop-from-header': 'false',
    'atuserid': '%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2215e8dc2b-7104-472b-b926-1ab261faf79c%22%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T16%3A43%3A14.824Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
    'atauthority': '%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T16%3A46%3A00.026Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
    'magasin_id': '164',
    'show-first-landing-popin': '4',
    'nlbi_2483309_2147483392': 'W8o1WySNUHduwMKlJag8ewAAAABc96giYMZDf+Fy3gCSCNlH',
    'reese84': '3:BRq2Rw0xeWB7I0Gy3Bt9zA==:9D7lBd2pXAIyxS25wFhR2SwuMXl+DAwx/WQq8qnVd+kFRT+CMQSicZogUGuAjuGSm2lt1pB1RlcUKkb7ZbNYzbdHl8I1YQBBA4ut7p+5EBv0dAkuS2Mw2SK6YEnfahyZjJTVVzxLIS82jSOLb+7MXeaQxRFu6rQnkDhHx2GzEwBnPbQe28ON2iScvuh7hFucrLB9/DBdVLP0wHtZ49rtLJin2seBgI0ANoX3oeYeQbGAog0jovUHdR3ycR2eGa92aXH2AYhS4FoInCawVtelZ9Ci35vdrNLyj/5gURKnd9VXUsRj1GTvsfFvjJ6zXAksUtcVRzulOXF6mx4QJe/vfKeG/GFZb8BofeWgMn8RjpQa7DsaJR2ILPc3FzlvWOVI6wnvYDH9IPw5LvCmhnHKIALFhwR7yZVTog+VaSYCTJnT3vemQSWQXBO6ByK09jcHaTXOnhE7SAIbWgsdQvHDiiv6HvMQz2DKeupjcpXCAbrt68OLE4Ma3igfNmGouX35u3psNsUkaoMxqHLF5u8xpg==:KxtQSmmdMg1hACmNml+5jtE+eYboMkwLVkcqv9EAMEk=',
    'OptanonAlertBoxClosed': '2023-12-06T16:43:18.879Z',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'visid_incap_2483309=7ZzVRalVQTS72xJVEqR5A56kcGUAAAAAQUIPAAAAAAC7GsrV967iLFDKSBQ8x/MJ; nlbi_2483309=zPqMamiQ6wC2ZwIsJag8ewAAAAD50aX1VNIsBgvmBiZVdZUm; incap_ses_467_2483309=caiTPOiYNF4nm5sHuh97Bp6kcGUAAAAAbdjdtnCkcxWRqkvDIVQaKA==; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Dec+06+2023+17%3A46%3A00+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=ff0d2c54-74d4-4446-92e7-8178ca31424d&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A0%2CC0003%3A0%2CC0001%3A1%2CC0002%3A0&geolocation=%3B&AwaitingReconsent=false; uuid=d1d24f33-ff02-47dc-9de6-bfa41526bf74; first-landing-change-shop-from-header=false; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%2215e8dc2b-7104-472b-b926-1ab261faf79c%22%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T16%3A43%3A14.824Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22cnil%22%2C%22visitor_mode%22%3A%22exempt%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-01-06T16%3A46%3A00.026Z%22%2C%22path%22%3A%22%2F%22%7D%7D; magasin_id=164; show-first-landing-popin=4; nlbi_2483309_2147483392=W8o1WySNUHduwMKlJag8ewAAAABc96giYMZDf+Fy3gCSCNlH; reese84=3:BRq2Rw0xeWB7I0Gy3Bt9zA==:9D7lBd2pXAIyxS25wFhR2SwuMXl+DAwx/WQq8qnVd+kFRT+CMQSicZogUGuAjuGSm2lt1pB1RlcUKkb7ZbNYzbdHl8I1YQBBA4ut7p+5EBv0dAkuS2Mw2SK6YEnfahyZjJTVVzxLIS82jSOLb+7MXeaQxRFu6rQnkDhHx2GzEwBnPbQe28ON2iScvuh7hFucrLB9/DBdVLP0wHtZ49rtLJin2seBgI0ANoX3oeYeQbGAog0jovUHdR3ycR2eGa92aXH2AYhS4FoInCawVtelZ9Ci35vdrNLyj/5gURKnd9VXUsRj1GTvsfFvjJ6zXAksUtcVRzulOXF6mx4QJe/vfKeG/GFZb8BofeWgMn8RjpQa7DsaJR2ILPc3FzlvWOVI6wnvYDH9IPw5LvCmhnHKIALFhwR7yZVTog+VaSYCTJnT3vemQSWQXBO6ByK09jcHaTXOnhE7SAIbWgsdQvHDiiv6HvMQz2DKeupjcpXCAbrt68OLE4Ma3igfNmGouX35u3psNsUkaoMxqHLF5u8xpg==:KxtQSmmdMg1hACmNml+5jtE+eYboMkwLVkcqv9EAMEk=; OptanonAlertBoxClosed=2023-12-06T16:43:18.879Z',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

i=0
info = []

while True:
    i+=1
    
    params = {
        'pageindex': str(i),
    }

    response = requests.get(
        'https://www.cora.fr/faire_mes_courses/surgeles/legumes_et_fruits-c-176918',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    if response.history:
        break

    soup = bs(response.text, features="html.parser")
    # print(soup.prettify())

    list = soup.find('ul',class_="c-list c-product-list-container-products c-product-list-container-products--grid")
    # print(list)

    prods = list.findAll('li', class_="c-list__item c-product-list-container-products__item Desk_DP_Tuile c-product-list-container-products__item--grid")
    # print(len(prods))
    
    for prod in prods:

        title = prod.find('h2',class_='c-product-list-item__intitule-slice').get_text()
        #clean title
        title = title.replace('\n','').strip()

        price = prod.find('p', class_='c-price__amount').find('span').get_text()
        price = float(price.replace(',','.'))

        price_kg = prod.find('p', class_='c-product-list-item__unit-price u-mt-xs').find('span').get_text()
        price_kg = float(price_kg.split()[0].replace(',', '.'))

        try:
            nutri = prod.find('div', class_='c-product-list-item--grid__score-promo-slice').find('picture').find('img')['alt'][-1]
            #clean nutri
            nutri = nutri.replace('\n','').strip()
        except:
            nutri = 'Non Specified'
        
        # save information in dictionary
        data = dict()
        data['title'] = title
        data['nutriScore'] = nutri
        data['price'] = price
        data['price_kg'] = price_kg
        
        info.append(data)
        
df = pd.DataFrame.from_dict(info)
print(df.head())
