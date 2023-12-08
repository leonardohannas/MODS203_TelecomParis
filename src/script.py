import requests
from bs4 import BeautifulSoup as bs

# faire_mes_courses-c-176362


def get_supermarket():
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

    for i in range(1, 2):
        response = requests.get(
            f"https://api.cora.fr/api/magasins/{i}", headers=headers
        )

        if response.status_code == 200:
            print(response.json()["data"])


def main():
    # get_supermarket()

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

    response = requests.get(
        "https://api.cora.fr/api/magasins/102/navigation-content/C-176652",
        headers=headers,
    )
    print(response.json())


main()
