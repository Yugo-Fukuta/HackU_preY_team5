import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import firebase from 'firebase'

createApp(App).use(router).mount('#app')

const config = {
    apiKey: "AIzaSyCfSympENN-cf5R_hbE7He231v6oK07eHs",
    authDomain: "hacku-team5-ys.firebaseapp.com",
    projectId: "hacku-team5-ys",
    storageBucket: "hacku-team5-ys.appspot.com",
    messagingSenderId: "1011613001527",
    appId: "1:1011613001527:web:a402ee663df73204be1cb2",
    measurementId: "G-64W9EFSXD4"
}
firebase.initializeApp(config);
