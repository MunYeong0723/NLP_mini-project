import requests
from bs4 import BeautifulSoup
import json
import csv
import time

#--------------<To Do List>------------------
#--------------------------------------------
#--------- 2. 영화상세페이지
#--------- 3.1 사용자가 평가한 작품목록
#--------- 3.2 사용자가 보고싶은 작품목록
#--------------------------------------------
#--------------------------------------------

print("----------------------------")

# 영화상세페이지 -> 코멘트페이지, user_code추출이 목적
##movie_code
movie_code_list = []

with open(r'C:\Users\tiale\Desktop\gwAi\AI_SCHOOL\watchaMovie\watch_top_movie_data.csv', 'r', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    headers = csvreader.fieldnames
    for row in csvreader:
        movie_code_list.append(row['movie_code'])

for movie_code in movie_code_list:
    detail_front_url = 'https://api-pedia.watcha.com/api/contents/'
    detail_last_url = '/comments'
    detail_full_url = detail_front_url + movie_code + detail_last_url
    
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
        'referer': 'https://pedia.watcha.com/ko-KR/contents/md6B3Ad/comments',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_gid=GA1.2.485481806.1598425995; _ga=GA1.1.2013127144.1598425995; _gat=1; _guinness_session=0ntLKJeNo1DogHBJsn1ZRTSBBb3KlF0OKivVIkJ49G6Q56eAzKT2^%^2BcZwY8PhvGsO7vowqoMqhBG52kxPBHlLFqgP--2FEPgHTlDXvabn^%^2Bh--WCOy5L5h0eRsvAgk0y^%^2B^%^2BZQ^%^3D^%^3D; _ga_1PYHGTCRYW=GS1.1.1598507810.8.1.1598507817.0',
        'if-none-match': 'W/^\\^e7daf894832b72848760e238bb91af73^\\^',
    }
    
    watcha_user_data = []
    
    for page in range(1, 7):
        size = 3
        
        params = (
            ('filter', 'all'),
            ('order', 'popular'),
            ('page', page),
            ('size', size),
        )
        
        response = requests.get(detail_full_url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        soup_list = list(soup)[0]
        soup_json = json.loads(soup_list)
        num = len(list(soup_json['result']['result']))
        
        for n in range(num):
            if len(soup_json['result']['result']) != 0:
                user_code = soup_json['result']['result'][n]['user']['code']
                user_name = soup_json['result']['result'][n]['user']['name']
                if soup_json['result']['result'][n]['user_content_action']['rating'] != None:
                    user_rating = round(soup_json['result']['result'][n]['user_content_action']['rating']/2, 1)
                else:
                    user_rating = 'null'
                
                user_data = {'user_code': user_code, 'user_name': user_name, 'user_rating': user_rating}
                
                watcha_user_data.append(user_data)
                
        
    print("\n\n\n왓챠피디아 별점 TOP// 유저데이터// 유저코드/유저닉네임/유저평점/유저텍스트 >>>>\n\n", watcha_user_data)
    time.sleep(10)
print("\n\n\n\n\n\n\n\n\n")

