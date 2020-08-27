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
        'if-none-match': 'W/"ef10c54e124b543e955cd0db7b4f2b2e"',
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
                'ratings_avg' : movie['ratings_avg']
            }
            print(f"movie {movie_one['title']} start 😎")
            getCollections(movie_one)
            getSimilars(movie_one)

            movie_data.append(movie_one)
            print(f"movie {movie_one['title']} done 😁")

    print("🧐 crawling done")

def getCollections(movie_one):
    referer = "https://pedia.watcha.com/ko-KR/contents/" + movie_one['code']
    url = f"https://api-pedia.watcha.com/api/contents/{movie_one['code']}/decks"
    
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
        'cookie': '_gid=GA1.2.304919113.1598425998; _c_drh=true; _ga_1PYHGTCRYW=GS1.1.1598442806.2.1.1598443137.0; _guinness_session=ol5LZPXpaDsiJwHMQc4E2Bx9gSe6x9%2FmJuFsCVJlI54ds6zFrGbb5yX5NB%2F3SPBaBNlNGS0IpPcGn4HnrjmAxx9E--d5Tk603x1gLE2pJd--%2BxeeGIjWMq9aEqfINLPtXQ%3D%3D; _ga=GA1.2.1070950575.1598425998',
    }
    
    collect_list = []
    for i in range(1,4):
        params = (
            ('page', str(i)),
            ('size', '20'),
        )

        response = requests.get(url, headers=headers, params=params)
        js = json.loads(response.text)
        for collect in js['result']['result']:
            collect_list.append(collect['title'])

    movie_one['collection'] = collect_list
    print(f"🙄 movie {movie_one['title']} done -> ", len(collect_list))

def getSimilars(movie_one):
    referer = 'https://pedia.watcha.com/ko-KR/contents/' + movie_one['code']
    url = f"https://api-pedia.watcha.com/api/contents/{movie_one['code']}/similars"
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
        'cookie': '_gid=GA1.2.304919113.1598425998; _c_drh=true; _ga_1PYHGTCRYW=GS1.1.1598442806.2.1.1598443137.0; _guinness_session=ol5LZPXpaDsiJwHMQc4E2Bx9gSe6x9%2FmJuFsCVJlI54ds6zFrGbb5yX5NB%2F3SPBaBNlNGS0IpPcGn4HnrjmAxx9E--d5Tk603x1gLE2pJd--%2BxeeGIjWMq9aEqfINLPtXQ%3D%3D; _ga=GA1.2.1070950575.1598425998',
    }

    similars_list = []
    for i in range(1,4):
        params = (
            ('page', str(i)),
            ('size', '20'),
        )

        response = requests.get(url, headers=headers, params=params)
        js = json.loads(response.text)
        for s in js['result']['result']:
            if s['content_type'] != "movies": continue

            mv = {
                'code' : s['code'],
                'title' : s['title'],
                'ratings_avg' : s['ratings_avg']
            }
            similars_list.append(mv)

    movie_one['similars'] = similars_list
    print(f"🙄 movie {movie_one['title']} done -> ", len(similars_list))


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
    writeCSV(movie_data, 'list_movie.csv')

if __name__ == "__main__":
    main()