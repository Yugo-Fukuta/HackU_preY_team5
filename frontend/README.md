# frontend

## 立ち上げ方
```sh
# 共通
git clone git@github.com:Yugo-Fukuta/HackU_preY_team5.git
cd HackU_preY_team5

git checkout ys
docker-compose up -d --build
docker-compose exec frontend sh
```

## Vue.jsでのデプロイ方法
```sh
firebase login

# Vue.jsのプロジェクトをfirebase上で動かせるようにbuild
yarn build

firebase init hosting
? What do you want to use as your public directory? dist
? Configure as a single-page app (rewrite all urls to /index.html)? No
? File dist/index.html already exists. Overwrite? No

firebase deploy
```

### 参考
- [Vue.js によるアプリを Firebase で Hosting する最短の道(Qiita)](https://qiita.com/Satachito/items/4a00b402970d657a88f3)
- [Firebaseでデプロイしよう！](https://qiita.com/hiroki-harada/items/ca22ac177db68e3c3796)

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
