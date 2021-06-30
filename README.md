# Team5_AliceとBob

## RestAPIを試す
#### ※コマンドは全てbackendコンテナの/usr/src/app/backend で行う
#### 1.backendディレクトリでマイグレーション実行
```
alembic upgrade head
```

#### ※1.でエラーが出る場合、migrationフォルダを削除して以下コマンドを実行してから1.を実行
```
alembic revision --autogenerate -m 'create oshido'
```

#### 2.以下のページでRestAPIを試せる
```
http://localhost:5000/docs
```


## Docker環境構築

### コンテナ作成について(参考記事)
<https://qiita.com/Yugo-Fukuta/items/a252b6eeeed7a13a9c9c>

#### イメージのビルド
```
docker-compose build
```

#### コンテナ作成
```
docker-compose up -d
```

#### コンテナ一覧表示(全てUPになっているかどうか)
```
docker-compose ps
```

### Vueのインストール(参考記事)
<https://px-wing.hatenablog.com/entry/2020/11/12/065719>

#### frontendコンテナに入る
```
docker-compose exec frontend sh
```

#### frontend用のenvファイルをfrontend/ に配置
https://github.com/Yugo-Fukuta/HackU_preY_team5_env
ここにある3つのenvファイルをfrontend/ 直下に置いてください。

#### Vueサーバーを起動
```
yarn local-serve # ローカル .env.local にある環境変数を読み込む
yarn dev-serve # 開発環境 .env.development にある環境変数を読み込む
yarn prod-serve # 本番環境 .env.production にある環境変数を読み込む
```

#### Vueサーバー停止はCTRL+C。コンテナから出る時はexitと入力。コンテナ停止はdocker-compose stop


## ブラウザ上でbackendとfrontendの動作確認

#### backendのURL(Hello WorldのJSONが表示されたら成功)
```
http://localhost:5000
```

#### frontendのURL(Vueの初期ページが表示されたら成功)
```
http://localhost:3000
```

### mysqlコンテナについて
<https://qiita.com/Yugo-Fukuta/items/a252b6eeeed7a13a9c9c>

### FastAPIの参考記事
<https://px-wing.hatenablog.com/entry/2020/11/17/070007>
