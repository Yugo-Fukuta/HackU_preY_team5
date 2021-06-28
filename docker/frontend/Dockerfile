FROM node:lts-alpine

WORKDIR /usr/src/app/frontend

RUN yarn global add @vue/cli @vue/cli-init
RUN yarn add axios vue-axios

RUN  yarn
RUN  yarn install
RUN  npm install -g firebase-tools
