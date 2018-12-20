import os
import requests
import json

token = os.getenv('TELE_TOKEN')
#getUpdates 는 봇이 메세지를 받고 그 결과를 업데이트
method = 'getUpdates'
#환경 변수에 저장된 토큰을 위해 <token>을 {} 로, name을 {}로
# c9에서 telegram api가 막혀있기 때문에 url우회해서
url = "https://api.hphk.io/telegram/bot{}/{}".format(token,method)


res = requests.get(url).json()
# 뽑을때 {딕셔너리} 이게 있으면 ["xx"]이거로 접근해야하고, [리스트] 이게 있으면 [index]로 접근해야함

user_id = res["result"][0]["message"]["from"]["id"]
msg = "배고프지?"

method = 'sendMessage'
# 각각 {}중괄호 안에 순서대로 적어줌
msg_url = "https://api.hphk.io/telegram/bot{}/{}?chat_id={}&text={}".format(token,method,user_id,msg)
print(msg_url)
# 프린트한 url인데 맨 뒤에 배고프지? 자리에 아무거나 넣어도 그 넣은 값이 채팅으로 넘어가서 자동으로 보내짐
# https://api.hphk.io/telegram/bot732099173:AAGAS6VyCYo-s4aQJ3AIYxjx160pPBt8vck/sendMessage?chat_id=670316113&text=배고프지?

requests.get(msg_url)

