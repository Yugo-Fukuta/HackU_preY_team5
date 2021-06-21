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

#### Vueアプリの作成
```
vue create .
```

#### 質問に答える1 (Yを入力)
```
? Generate project in current directory? (Y/n) Y
```

#### 質問に答える2 (Vue 3を選択)
```
? Please pick a preset: 
  Default ([Vue 2] babel, eslint) 
❯ Default (Vue 3) ([Vue 3] babel, eslint) 
  Manually select features 
```

#### 質問に答える3 (Yarnを選択)
```
? Pick the package manager to use when installing dependencies: (Use arrow keys)
❯ Use Yarn 
  Use NPM 
```
#### 作成Success後にVueを起動
```
yarn serve
```

#### Vue停止はCTRL+C。コンテナから出る時はexitと入力。コンテナ停止はdocker-compose stop


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