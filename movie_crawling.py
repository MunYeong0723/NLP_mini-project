import requests
from bs4 import BeautifulSoup
import json
import csv
import time

def getMovies(movie_data, user_code) :
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
            getComment(movie_one, user_code)

            movie_data.append(movie_one)
            print(f"movie {movie_one['title']} done 😁")

    print("🧐 crawling done")

def getComment(movie_one, user_code):
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
        user_code.append(c['user']['code'])

    movie_one['comments'] = users
    print(f"🙄 movie {movie_one['title']} get comments done ->", len(users))

def getUserScoring(user_code, user_one):
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
        'referer': f'https://pedia.watcha.com/ko-KR/users/{user_code}/contents/movies/ratings',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.866190973.1598511669; _c_drh=true; _ga_1PYHGTCRYW=GS1.1.1598527836.3.1.1598540008.0; _ga=GA1.2.1832522055.1598511669; _guinness_session=7zS%2FD5%2BF1CTyNCZf4msM91oTQouOCO92xAPHiOAYO%2FJxFoGdfDRwdLMCahTYPxtSjggxyPT58T%2FllI3VszLvgajz--h4FUnZcjV%2BkPYWEb--DvM25BwrZgCuM87njQrN7A%3D%3D',
    }

    params = (
        ('order', 'avg_rating'),
        ('page', '1'),
        ('size', '10'),
    )

    response = requests.get(f'https://api-pedia.watcha.com/api/users/{user_code}/contents/movies/ratings', headers=headers, params=params)
    js = json.loads(response.text)

    rt_movie = []
    for r in js['result']['result']:
        rt_movie.append({
            'movie_code' : r['content']['code'],
            'movie_title' : r['content']['title'],
            'movie_rating' : round(r['user_content_action']['rating']/2,1)
        })
    user_one['rt_movie'] = rt_movie


def getUserWish(user_code, user_one):
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
        'referer': f'https://pedia.watcha.com/ko-KR/users/{user_code}/contents/movies/wishes',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.866190973.1598511669; _c_drh=true; _gat=1; _ga_1PYHGTCRYW=GS1.1.1598527836.3.1.1598540550.0; _ga=GA1.2.1832522055.1598511669; _guinness_session=1hygPMLcsT5pR6R1QFiIWIDEnRra5WSaubZQ7mSHd7kWP%2FxNA73mvTW0tcfGD6i11EqRsGZy2Fe7S9qU87GnGEyr--dLjgfAvMfHf97pgy--X0t3Zwog1Qh1ENr9gSRLhA%3D%3D',
    }

    params = (
        ('order', 'avg_rating'),
        ('page', '1'),
        ('size', '10'),
    )

    response = requests.get(f'https://api-pedia.watcha.com/api/users/{user_code}/contents/movies/wishes', headers=headers, params=params)
    js = json.loads(response.text)

    wish_movie = []
    for r in js['result']['result']:
        wish_movie.append({
            'code' : r['content']['code'],
            'title' : r['content']['title'],
            'year' : r['content']['year'],
            'genres' : r['content']['genres'],
            'ratings_avg' : round(r['content']['ratings_avg']/2, 1)
        })
    user_one['wish_movie'] = wish_movie

def getUserData(user_code, user_data):
    user_num = 0
    for user in user_code :
        user_num += 1

        user_one = {}
        getUserScoring(user, user_one)
        getUserWish(user, user_one)

        print("😎 user scoring -> ", len(user_one['rt_movie']))
        print("😎 user wish -> ", len(user_one['wish_movie']))
        user_data.append(user_one)

        # if user_num % 10 == 0:
        #     print("wait 10 sec")
        #     time.sleep(10)

# csv 파일로 작성하기
def writeCSV(data, filename) :
    header = data[0].keys()
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f :
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def main():
    # movie_data = []
    # user_code = []
    # getMovies(movie_data, user_code)
    # writeCSV(movie_data, 'list_movie2.csv')
    
    # print(user_code)
    # user_code = list(set(user_code))

    user_code = []
    with open("user_code.csv", 'r', encoding='utf-8-sig') as f:
        rd = csv.reader(f)
        user_code = next(rd)

    user_data = []
    getUserData(user_code, user_data)
    writeCSV(user_data, "user_data.csv")
    

if __name__ == "__main__":
    main()