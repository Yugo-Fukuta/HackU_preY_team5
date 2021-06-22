# frontend

## 立ち上げ方
```sh
git clone git@github.com:Yugo-Fukuta/HackU_preY_team5.git | cd HackU_preY_team5/

git checkout yf
docker-compose up -d --build
docker-compose exec frontend sh

# コンテナ内
# vue create .　これを実行するとsrc以下のファイルが書き換えられる
yarn serve # 実行出来ない場合はyarnをまず実行する
```

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
