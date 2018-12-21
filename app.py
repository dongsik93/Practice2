from flask import Flask, request
from pprint import pprint as pp
import os
import requests
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

html = requests.get('https://www.naver.com/').text
soup = BeautifulSoup(html, 'html.parser')
title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
i = []
for data in title_list:
    i.append(data.text)


api_url = 'https://api.hphk.io/telegram'
token = os.getenv('TELE_TOKEN')

@app.route(f'/{token}', methods=['POST'])
def telegram():
    # naver api를 사용하기 위한 변수
    naver_client_id = os.getenv('NAVER_ID')
    naver_client_secret = os.getenv('NAVER_SECRET')
    
    
    
    # tele_dict  = 데이터 덩어리
    tele_dict = request.get_json()
    pp(request.get_json())
    
    # 유저 정보
    chat_id = tele_dict["message"]["from"]["id"]
    # 유저가 입력한 데이터
    text = tele_dict.get("message").get("text")
    
    tran = False
    img = False
    
    # 사용자가 이미지를 넣었는지 체크체크
    if (tele_dict.get('message').get('photo')) is not None:
        img = True
    else:
    #번역 (한칸띄우고) 입력 -> 입력결과가 번역되게
    # text(유저가 입력한 데이터) 중 제일 앞 두글자가 번역인지를 확인
        if (text[:2]=="번역"):
            tran = True
            text = text.replace("번역","") #번역이라는 글씨가 없어짐
            
        
        
    
    if (tran):
        papago = requests.post("https://openapi.naver.com/v1/papago/n2mt",  #요청을 보내는 주소
                    headers = { # 유저 아이디와 비밀번호
                       "X-Naver-Client-Id":naver_client_id,
                       "X-Naver-Client-Secret":naver_client_secret
                    },
                    data = { #source=ko&target=en&text 이 필요하니까 소스 / 타겟 / 텍스트(번역 없앤 글자)
                        'source':'ko',
                        'target':'en',
                        'text':text
                    }
        )
        pp(papago.json())
        text = papago.json()["message"]["result"]["translatedText"]
    elif (img):
        text = "사용자가 이미지를 넣었어요"
        #텔레그램에게 사진 정보 가져오기
        file_id = tele_dict['message']['photo'][-1]['file_id']
        file_path = requests.get(f"{api_url}/bot{token}/getFile?file_id={file_id}").json()['result']['file_path']
        file_url = f"{api_url}/file/bot{token}/{file_path}"
        print(file_url)
        
        #사진을 네이버 유명인식 api로 넘겨주기
        file = requests.get(file_url, stream=True) # 실제 파일을 가져옴
        clova = requests.post("https://openapi.naver.com/v1/vision/celebrity",  #요청을 보내는 주소
                    headers = { # 유저 아이디와 비밀번호
                       "X-Naver-Client-Id":naver_client_id,
                       "X-Naver-Client-Secret":naver_client_secret
                    },
                    files = {
                        'image':file.raw.read() # 원본 데이터를 보내준다
                    }
        )
        #가져온 데이터 중에서 필요한 정보 빼오기
        pp(clova.json())
        #인식이 되었을 때
        if (clova.json().get('info').get('faceCount')):
            text = clova.json()['faces'][0]['celebrity']['value']
        #인식이 되지 않았을 때
        else :
            text = "얼굴이 없어요"
    
    elif (text == "메뉴"):
        menu_list = ["한식","중식","양식","분식","선택식"]
        text = random.choice(menu_list)
    elif (text == "로또"):
        text = random.sample(range(1,46),6)
    elif (text == "실검"):
            text = i
        
    
    # 유저에게 그대로 돌려주기
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    
    return '', 200
    
# 배포할 때 설정을 쉽게 하기위해 설정    
app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))





