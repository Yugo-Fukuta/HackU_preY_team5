# バックエンドデプロイ手順

1. Pull
```
cd ../HackU_preY_team5_env/
git pull
cd ../HackU_preY_team5/
git pull
```

2. Up
```
docker-compose up -d --build  # --build は基本要らない
```

3. Migration & Seed

まず
```
cp ../HackU_preY_team5_env/seed_*.py ./backend/seed/
```

次に `docker-compose exec backend bash` で backend コンテナに入った後：
```
alembic upgrade head
python seed/seed_api_keys.py
python seed_uid_v1.py
```
backend/db/data がある状態だと seed_api_keys.py は失敗するが気にしなくて良い。

4. 後始末
```
docker-compose down -v
# rm -r db/data  # ?
```