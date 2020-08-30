import requests
from bs4 import BeautifulSoup
import csv
import json
import time

headers = {
    'authority': 'api-pedia.watcha.com',
    'x-watcha-client-version': '2.0.0',
    'accept': 'application/vnd.frograms+json;version=20',
    'x-watcha-client-language': 'ko',
    'x-watcha-client': 'watcha-WebApp',
    'x-watcha-remote-addr': '49.246.44.236',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'x-watcha-client-region': 'KR',
    'origin': 'https://pedia.watcha.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pedia.watcha.com/ko-KR/decks/OphYTWVoSDLG',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_gid=GA1.2.1313289443.1598426067; _c_drh=true; _gat=1; _ga=GA1.1.1514133107.1598426067; _ga_1PYHGTCRYW=GS1.1.1598518307.3.1.1598519530.0; _guinness_session=nYycWbOZJI8SPdepvFwizNVDJ69JMdRk%2FEIzBs24V4hdPzyczMX%2B8xlRSWNgP97xL0gTEWFVI2icLfVcDKF4wfMr--CQsJ8Sbfaibfj1c8--Q5Je%2Bu3dtUdVdXY9n6WjTw%3D%3D',
}

code_list = []
title_list = []
genre_list = []
rating_list = []

rate_list = []
review_list = []

for page in range(43):
    params = (
        ('page', page),
        ('size', '12'),
    )

    response = requests.get('https://api-pedia.watcha.com/api/decks/OphYTWVoSDLG/items', headers=headers, params=params)
    result = json.loads(response.text)

    for i in range(0,12):
        try:
            code_list.append(result['result']['result'][i]['content']['code'])
            title_list.append(result['result']['result'][i]['content']['title'])
            genre_list.append(result['result']['result'][i]['content']['genres'])
            rating_list.append(int(result['result']['result'][i]['content']['ratings_avg']) / 2)
        except:
            continue


for code in code_list:
    headers = {
        'authority': 'api-pedia.watcha.com',
        'x-watcha-client-version': '2.0.0',
        'accept': 'application/vnd.frograms+json;version=20',
        'x-watcha-client-language': 'ko',
        'x-watcha-client': 'watcha-WebApp',
        'x-watcha-remote-addr': '49.246.44.236',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'x-watcha-client-region': 'KR',
        'origin': 'https://pedia.watcha.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pedia.watcha.com/ko-KR/contents/'+code+'/comments',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.1382601462.1598518297; _ga=GA1.1.1611966965.1598518297; _ga_1PYHGTCRYW=GS1.1.1598518349.1.0.1598518444.0; _guinness_session=N%2Fvq%2FttzP0D8Nv1FU6xeF3LIECAqcenDy0LcczsgcURUEMYT08mQTGakLWCagG0P37xxbdnad2%2BxgyRKCiFTKydG--Ms5DiZyqvha1xHBX--BXQb736U922%2B3aKQLIdd0w%3D%3D',
    }

    params = (
        ('filter', 'all'),
        ('order', 'popular'),
        ('page', '1'),
        ('size', '10000'),
    )

    response = requests.get('https://api-pedia.watcha.com/api/contents/'+code+'/comments', headers=headers, params=params)
    result = json.loads(response.text)

    for i in range(10000):
        try:
            rate_list.append(int(result['result']['result'][i]['user_content_action']['rating']) / 2)
            review_list.append(result['result']['result'][i]['text'])
        except:
            continue

    break

for i in range(len(title_list)):
    for j in range(len(review_list)):
        review_data = {
            'title': title_list[i],
            'genre': genre_list[i],
            'rating': rating_list[i],
            'rate': rate_list[j],
            'review': review_list[j]
        }

        with open("./review_data.csv" , 'a' , encoding='utf_8', newline='') as csvfile:
            header = review_data.keys()
            csvwriter = csv.DictWriter(csvfile,header)
            csvwriter.writerow(review_data)



