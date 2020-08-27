import requests
from bs4 import BeautifulSoup
import json
import csv

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
        'referer': 'https://pedia.watcha.com/ko-KR/staffmades/267',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.304919113.1598425998; _c_drh=true; _ga_1PYHGTCRYW=GS1.1.1598426026.1.1.1598427123.0; _ga=GA1.2.1070950575.1598425998; _guinness_session=Yhk2q%2FrcUjzedlRQXbCro3DeB29wnKyf6FMF7473CaIv%2F%2B6m1EOt%2FvVDlfC3IHdFIGrHow%2B4PVCeZ%2BGYOi%2BF%2Faj9--zaAD1140tzEvv7Gh--zH4b8mkDVNn1J6Ve1eHR7A%3D%3D',
    }

    for page in range(1, 34):
        params = (
            ('page', str(page)),
            ('size', '9'),
        )

        response = requests.get('https://api-pedia.watcha.com/api/staffmades/267/contents', headers=headers, params=params)
        js = json.loads(response.text)
        for movie in js['result']['result']:
            if movie['content_type'] != "movies":
                continue

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
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.866190973.1598511669; _c_drh=true; _gat=1; _guinness_session=9LFtKexXAEwfrulXaDIW4zvo8LN3%2BC3JJdqxSmZtm2TjaJ5eB45SPUNajgUnOJ2gLOJvtHhNmrg42ggGS1lFSGdu--okgGjiz8sVIXbpR5--S8w3Jxy2uV8ht8%2BWe1WHeg%3D%3D; _ga_1PYHGTCRYW=GS1.1.1598524754.2.1.1598525021.0; _ga=GA1.2.1832522055.1598511669',
    }

    users = []
    for i in range(1,20):
        params = (
            ('filter', 'all'),
            ('order', 'popular'),
            ('page', str(i)),
            ('size', '20'),
        )

        response = requests.get(url, headers=headers, params=params)
        js = json.loads(response.text)    

        for c in js['result']['result']:
            rt = c['user_content_action']['rating']
            if rt is None :
                rt = 0

            u = {
                'user_rating' : round(rt/2,1),
                'comment' : c['text'],
                'user_code' : c['user']['code'],
                'user_name' : c['user']['name']
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

def readCSV(filename, data):
    with open(filename, 'r', encoding='utf-8-sig') as f :
        rd = csv.reader(f)
        keys = next(rd)
        for rows in rd :
            data.append({
                keys[0] : rows[0],
                keys[1] : rows[1]
            })

def main():
    movie_data = []
    getMovies(movie_data)
    # writeCSV(movie_data, 'list_movie.csv')

    # movie_code = []
    # readCSV("list_movie.csv", movie_code)
    # print(movie_code)

    # users_list = []
    # getComment(movie_code, users_list)

if __name__ == "__main__":
    main()