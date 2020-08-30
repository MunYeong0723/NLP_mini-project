print("유저코드값으로 '보고싶어요'리스트 가져오기, rating리스트 가져오기")

## csv파일 생성
#with open(r'C:\Users\tiale\Desktop\gwAi\AI_SCHOOL\watchaMovie\user_data.csv', 'w', newline='') as csvfile:
#    fieldnames = ['user_code', 'user_name']
#    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
#    csvwriter.writeheader()
#    for row in watcha_user_data:
#        csvwriter.writerow(row)

#
## 사용자가 평가한 작품목록, 각 영화에 대한 평점 추출이 목적
###user_code
#user_code = 'WRQxDkw965dl9'
#rating_front_url = 'https://pedia.watcha.com/ko-KR/users/'
#rating_last_url = '/movies/ratings'
#rating_full_url = rating_front_url + user_code + rating_last_url
#
#response = requests.get(rating_full_url)
#soup = BeautifulSoup(response.text, 'html.parser')
###path
#soup.select('path')
#
#
## 사용자가 보고싶은 작품목록, 목록 내 우선추천
#user_code = 'WRQxDkw965dl9'
#wish_front_url = 'https://pedia.watcha.com/ko-KR/users/'
#wish_last_url = 'movies/wishes'
#wish_full_url = wish_front_url + user_code + wish_last_url
#
#response = requests.get(wish_full_url)
#soup = BeautifulSoup(response.text, 'html.parser')
###path
#soup.select('path')