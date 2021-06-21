import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import firebase from 'firebase'

createApp(App).use(router).mount('#app')

const config = {
    apiKey: "AIzaSyAG5xVAyH8x5mpVnWfW3S3hDf96g79Gxw8",
    authDomain: "hacku-team5.firebaseapp.com",
    projectId: "hacku-team5",
    storageBucket: "hacku-team5.appspot.com",
    messagingSenderId: "635092656486",
    appId: "1:635092656486:web:268a8401148a3ab014a8a7",
    measurementId: "G-GERL1K2ZEY"
}
firebase.initializeApp(config);