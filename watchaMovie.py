import requests
from bs4 import BeautifulSoup
import json

print("----------------------------")

headers = {
    'authority': 'api-pedia.watcha.com',
    'x-watcha-client-version': '2.0.0',
    'accept': 'application/vnd.frograms+json;version=20',
    'x-watcha-client-language': 'ko',
    'x-watcha-client': 'watcha-WebApp',
    'x-watcha-remote-addr': '58.230.67.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'x-watcha-client-region': 'KR',
    'origin': 'https://pedia.watcha.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pedia.watcha.com/ko-KR/staffmades/267',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_gid=GA1.2.485481806.1598425995; _ga=GA1.1.2013127144.1598425995; _ga_1PYHGTCRYW=GS1.1.1598444213.2.0.1598444213.0; _gat=1; _guinness_session=LSk0yfw^%^2F^%^2F3yZAKPeaGasR6O5iRGdlvc1oUhFbNtC5d34nDp54gA9mtbSRsiGor7gv73T8zGcmRCbPly6S6tX1tpS--EhrSN522kfw8jkX^%^2F--93BtnynHRLURT6sej6hDkw^%^3D^%^3D',
    'if-none-match': 'W/^\\^797643ac55da37e468299cc8be669047^\\^',
}

watcha_movie_data = []
pg = 0

for page in range(35):  
    
    size = 9
    
    params = (
        ('page', page),
        ('size', size),
    )
    
    response = requests.get('https://api-pedia.watcha.com/api/staffmades/267/contents', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_list = list(soup)[0]
    soup_json = json.loads(soup_list)
    
    if pg != 34:
        for n in range(size):
            title = soup_json['result']['result'][n]['title']
            content_type = soup_json['result']['result'][n]['content_type']
            ratings_avg = round(soup_json['result']['result'][n]['ratings_avg']/2, 1)
            movie_code = soup_json['result']['result'][n]['code']
            
            movie_data = {'title': title, 'content_type': content_type, 'ratings_avg': ratings_avg, 'movie_code': movie_code}
            watcha_movie_data.append(movie_data)
    
    else:
        for n in range(3):
            title = soup_json['result']['result'][n]['title']
            content_type = soup_json['result']['result'][n]['content_type']
            ratings_avg = round(soup_json['result']['result'][n]['ratings_avg']/2, 1)
            movie_code = soup_json['result']['result'][n]['code']
            
            movie_data = {'title': title, 'content_type': content_type, 'ratings_avg': ratings_avg, 'movie_code': movie_code}
            watcha_movie_data.append(movie_data)
    
    pg += 1
    
    print("~progressing page: ", pg)

print("\n\n\n왓챠피디아 별점 TOP// 제목/타입/평점 >>>>\n\n", watcha_movie_data)
print("\n\n\n\n\n\n\n\n\n")
