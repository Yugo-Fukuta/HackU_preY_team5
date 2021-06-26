'''
This is seed_sample.py.
これはseedファイルのサンプルです。
seedlistにseedしたいデータを適宜記述してください。
APIキーを記載しているseedファイルの場合、.gitignoreに   /backend/seed/<seedファイル>   という記述を追加してください。
seedを行う際は、backendコンテナに入り(docker-compose exec backend bash)、その状態(root@???:/usr/src/app/backend#)で、
python seed/seed_sample.py
を実行してください。
'''

import sys
sys.path.append('../backend')
from database import SessionLocal
from models.oshido import OshidoModel
from models.youtube import YouTubeModel
from models.twitter import TwitterModel
from models.news import NewsModel

db = SessionLocal()

def seed():
    #seedlistの内容は適宜変えてください。
    seedlist = [
        {
        'where': 'oshido',
        'uid': 'uid0',
        'celeb_name': 'celeb0',
        'oshido': 20,
        },
        {
        'where': 'youtube',
        'whose': 'user0',
        'nankome': 0,
        'api_key': 'api_key0',
        },
        {
        'where': 'twitter',
        'whose': 'user0',
        'nankome': 0,
        'api_key': 'api_key0',
        'api_key_secret': 'my_key_secret',
        'access_token': 'my_token',
        'access_token_secret': 'my_token_secret',
        },
        {
         'where': 'news',
         'whose': 'user0',
         'nankome': 0,
         'api_key': 'api_key0',
        }]

    for s in seedlist:
        if s['where'] == 'oshido':
            req = OshidoModel(uid=s['uid'], celeb_name=s['celeb_name'], oshido=s['oshido'])
        elif s['where'] == 'youtube':
            req = YouTubeModel(whose=s['whose'], nankome=s['nankome'], api_key=s['api_key'])
        elif s['where'] == 'twitter':
            req = TwitterModel(whose=s['whose'], nankome=s['nankome'], api_key=s['api_key'], api_key_secret=s['api_key_secret'], access_token=s['access_token'], access_token_secret=s['access_token_secret'])
        elif s['where'] == 'news':
            req = NewsModel(whose=s['whose'], nankome=s['nankome'], api_key=s['api_key'])
        else:
            return 400
        db.add(req)
        db.commit()
    return 201

if __name__ == '__main__':
    BOS = '\033[92m'  # 緑色表示用
    EOS = '\033[0m'

    print(f'{BOS}Seeding data...{EOS}')
    status = seed()
    if status and status == 201: 
        print('Done!')
    else:
        print('Oops!! Some Error Occurred!!!')