# Team5_AliceとBob

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

#### Vueサーバーを起動
```
yarn serve
```

#### Vueサーバー停止はCTRL+C。コンテナから出る時はexitと入力。


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
