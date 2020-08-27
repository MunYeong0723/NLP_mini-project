import requests
from bs4 import BeautifulSoup
import json
import csv
import time

def getMovies(movie_data) :
    headers = {
        'authority': 'api-pedia.watcha.com',
        'x-watcha-client-version': '2.0.0',
        'accept': 'application/vnd.frograms+json;version=20',
        'x-watcha-client-language': 'ko',
        'x-watcha-client': 'watcha-WebApp',
        'x-watcha-remote-addr': '39.114.149.98',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'x-watcha-client-region': 'KR',
        'origin': 'https://pedia.watcha.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://pedia.watcha.com/ko-KR/staffmades/611',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.866190973.1598511669; _c_drh=true; _ga=GA1.1.1832522055.1598511669; _gat=1; _ga_1PYHGTCRYW=GS1.1.1598527836.3.1.1598535412.0; _guinness_session=V5fgQM%2FZNgn4nRplvV%2Bh5TyfksVfd9teX9S53poxZgphpgrwpz4VqP4cVfQo2aTqzNiUe7abv2Lv8dnIVGfz%2Fr%2BO--RbozoCRengK9MPan--BhbpVUH%2FfQAUySAK8u0kVQ%3D%3D',
        'if-none-match': 'W/"c23b19f0180700f241bf6534e263ae70"',
    }

    movie_num = 0
    for page in range(1, 10):
        params = (
            ('page', str(page)),
            ('size', '9'),
        )

        response = requests.get('https://api-pedia.watcha.com/api/staffmades/611/contents', headers=headers, params=params)
        if len(response.text) == 0 :
            print("page : ", page)
            continue

        js = json.loads(response.text)

        for movie in js['result']['result']:
            if movie['content_type'] != "movies":
                continue

            movie_num += 1
            if movie_num % 5 == 0 :
                print("wait 10 sec")
                time.sleep(10)

            movie_one = {
                'code' : movie['code'],
                'title' : movie['title'],
                'year' : movie['year'],
                'genres' : movie['genres'],
                'ratings_avg' : round(movie['ratings_avg']/2, 1)
            }
            print(f"movie {movie_one['title']} start 😎")
            getComment(movie_one)

            movie_data.append(movie_one)
            print(f"movie {movie_one['title']} done 😁")

    print("🧐 crawling done")

def getComment(movie_one):
    referer = f"https://pedia.watcha.com/ko-KR/contents/{movie_one['code']}"
    url = f"https://api-pedia.watcha.com/api/contents/{movie_one['code']}/comments"

    headers = {
        'authority': 'api-pedia.watcha.com',
        'x-watcha-client-version': '2.0.0',
        'accept': 'application/vnd.frograms+json;version=20',
        'x-watcha-client-language': 'ko',
        'x-watcha-client': 'watcha-WebApp',
        'x-watcha-remote-addr': '39.114.149.98',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'x-watcha-client-region': 'KR',
        'origin': 'https://pedia.watcha.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': referer,
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    users = []
    params = (
        ('filter', 'all'),
        ('order', 'popular'),
        ('page', '1'),
        ('size', '10'),
    )

    response = requests.get(url, headers=headers, params=params)
    js = json.loads(response.text)

    for c in js['result']['result']:
        rt = c['user_content_action']['rating']
        if rt is None :
            rt = 0

        u = {
            'user_code' : c['user']['code'],
            'user_name' : c['user']['name'],
            'user_rating' : round(rt/2,1)
        }
        users.append(u)

    movie_one['comments'] = users
    print(f"🙄 movie {movie_one['title']} get comments done ->", len(users))

# csv 파일로 작성하기
def writeCSV(data, filename) :
    header = data[0].keys()
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f :
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def main():
    movie_data = []
    getMovies(movie_data)
    writeCSV(movie_data, 'list_movie2.csv')

if __name__ == "__main__":
    main()