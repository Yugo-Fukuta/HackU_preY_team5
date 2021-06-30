<template>
    <div class="container">
        <div class="blank"></div>
        <div class="header">
            <div class="search-box">
                <img src="@/assets/search.png" class="search-icon">
                <input @keydown.enter="trigger" v-model="newName" class="input-form">
                <img v-if="isntOshi" @click="addOshi" src="@/assets/like.png" class="like-button">
                <img v-else @click="deleteOshi" src="@/assets/heart.png" class="like-button">
            </div>
        </div>

        <div v-for="(movie, index) in celebInfo" v-bind:key="movie.videoUrl" class="content-box">
            <img src="@/assets/sns-icon-banner.png" class="sns-icon-banner">
            <img src="@/assets/youtube-icon.png" class="youtube-icon">
            <div class="content">
                <iframe width="330" height="185" class="y-movie" v-bind:src="movie.videoUrl" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <div @click="toggleBtn(index)" v-bind:class="{active:isActive[index]}" class="content content-sub">
                <div class="content-sub-top">
                    <div class="content-mini-box">
                        <div class="ymovie-title">{{ movie.title.substring(0,72)+"..." }}</div>
                        <div class="ymovie-view-count">{{ movie.viewCount }}回視聴</div>
                        <div class="ymovie-publishedat">{{ movie.publishedAt.substring(0,10) }}</div>
                        <img src="@/assets/like-button.png" class="like-icon">
                        <div class="like-count">{{ movie.likeCount }}</div>
                        <img src="@/assets/dislike-button.png" class="dislike-icon">
                        <div class="dislike-count">{{ movie.dislikeCount }}</div>
                    </div>
                </div>
                <div class="content-sub-bottom">
                    <div class="content-mini-box">
                    </div>
                </div>
                <img src="@/assets/content-banner.png" class="content-banner">
            </div>
        </div>

        <div v-for="(tweet, index) in celebTwInfo" v-bind:key="tweet.text" class="content-box">
            <img src="@/assets/sns-icon-banner.png" class="sns-icon-banner">
            <div class="content">
                <div class="content-line">
                    <img v-bind:src="tweet.user.profile_image_url_https" class="tw-profile-image">
                    <div class="tw-username-box">
                        <div class="tw-user-name">{{ tweet.user.name }}</div>
                        <img v-if="tweet.user.verified" src="@/assets/twitter-verified-mark.png" class="tw-verified-img">
                    </div>
                    <div class="tw-text">{{ tweet.text }}</div>
                </div>
            </div>
            <div @click="toggleBtn(index)" v-bind:class="{active:isActive[index]}" class="content content-sub">
                <img src="@/assets/content-banner.png" class="content-banner">
            </div>
        </div>

        <footer>
            <div class="foot-space"></div>
            <div class="foot-nav">
                <div class="oshido-circle2"></div>
                <img src="@/assets/oshido-circle.png" class="oshido-circle-img">
            </div>
        </footer>
    </div>
</template>

<script>
import axios from 'axios'
import firebase from 'firebase'

export default {
    el: '#app',
    data() {
        return {
            uid: '',
            name: this.$route.params.celebName,
            newName: '',
            celebInfo: '',
            celebTwInfo: '',
            params: {
                q: "", // 検索クエリを指定
                part: "snippet",
                type: "video",
                maxResults: "3", // 最大検索数
                key: process.env.VUE_APP_YOUTUBE_API_KEY
            },
            isActive: {
                type: [Boolean],
                default: false
            },
            isntOshi: true,
            oshido: 0
        };
    },
    mounted() {
        this.getYoutube() // Youtubeの動画取得
        this.getTweet() // Twitterの動画取得
        this.isOshi() // ユーザーが検索された有名人を推しているか判定
    },
    watch: {
        '$route' (to) {
            this.trigger(to.event)
        }
    },
    methods: {
        toggleBtn: function(i) {
            this.isActive[i] = !this.isActive[i]
        },
        trigger: function(event) {
            if (event.keyCode != 13) return
            this.name = this.newName
            this.$router.push({
                name: 'Celebs',
                params: {
                    celebName: this.name
                }
            })
        },
        addOshi: function() {
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    axios.post(process.env.VUE_APP_API_BASE_URL + "/register_oshido", {
                        uid: user.uid,
                        celeb_name: this.name,
                        oshido: 0
                    })
                    .then(response => {
                        console.log(response)
                        this.isntOshi = false
                    })
                    .catch(error => {
                        console.log(error.response.data)
                    })
                } else {
                    this.$router.push('/signup')
                }
            });
        },
        deleteOshi: function() {
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    axios.delete(process.env.VUE_APP_API_BASE_URL + "/delete_oshido", {
                        params: {
                            uid: user.uid,
                            celeb_name: this.name,
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.isntOshi = true
                    })
                    .catch(error => {
                        console.log(error.response.data)
                    })
                } else {
                    this.$router.push('/signup')
                }
            });
        },
        getTweet: function() {
            axios.get(process.env.VUE_APP_API_BASE_URL + "/get_twitter_data", {
                params: {
                    q: this.name,
                    maxResults: this.params.maxResults
                }
            })
            .then(response => {
                console.log(response)
                this.celebTwInfo = response.data[0].statuses;
            })
            .catch(error => {
                console.log(error.response)
            })
        },
        getYoutube: function() {
            axios.get(process.env.VUE_APP_API_BASE_URL + "/get_youtube_data", {
                params: {
                    q: this.name,
                    maxResults: this.params.maxResults
                }
            })
            .then(response => {
                console.log(response)
                this.celebInfo = response.data[0]
                this.celebInfo.forEach(element => {
                    element.videoUrl = "https://www.youtube.com/embed/" + element.id
                });
            })
            .catch(error => {
                console.log(error.response)
            })
        },
        isOshi: function() {
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    axios.get(process.env.VUE_APP_API_BASE_URL + "/get_oshido", {
                        params: {
                            uid: user.uid,
                            celeb_name: this.name
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.oshido = response.data[0].oshido
                        if (this.oshido == null) {
                            this.isntOshi = true
                        } else {
                            this.isntOshi = false
                        }
                    })
                    .catch(error => {
                        console.log(error.response)
                    })
                }
            });
        }
    },
}
</script>

<style>
.blank {
    height: 60px;
}

.header {
    position: fixed;
    z-index: 4;
    left: 5%;
    top: 5px;
    width: 90%;
    height: 56px;
    margin-bottom: 14px;
    background: #FFFFFF;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
    border-radius: 10px;
}

.search-box {
    position: absolute;
    width: 80%;
    z-index: 5;
    height: 37px;
    left: 10px;
    top: 10px;;
    background: #E5E5E5;
    border-radius: 5px;
    padding: 1px 2px;
}

.search-icon {
    position: absolute;
    z-index: 6;
    height: 15px;
    left: 5px;
    top: 13px;
}

.input-form {
    position: absolute;
    z-index: 5;
    height: 30px;
    width: 70%;
    left: 20px;
    top: 0;
    background: #E5E5E5;
    border-radius: 5px;
}


.like-button {
    position: absolute;
    z-index: 5;
    height: 20px;
    left: 105%;
    top: 10px;
}

.content-box {
    width: 341px;
    margin: 0 auto 20px auto;
    position: relative;
}

.content {
    width: 341px;
    height: 193px;
    margin: 0 auto 25px auto;
    background: #FFFFFF;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border-radius: 5px;

    transition: 0.5s;
    position: relative;
    z-index: 2;
}

.content-line {
    position: absolute;
    width: 330px;
    height: 185px;
    left: 2px;
    top: 1px;
    z-index: 3;
    border-radius: 5px;
    border: 3px solid #F4D153;
}

.content-sub {
    margin-top: -220px;
    position: relative;
    z-index: 1;
}

.content-mini-box {
    width: 330px;
    margin: 0 auto;
}

.content-sub-top {
    height: 145px;
    border-bottom: 1px solid #DDDDDD;
}

.content-banner {
    width: 100%;
    position: absolute;
    left: 0;
    top: 96%;
    z-index: 6;
}

.active {
    transform: translateY(170px);
    margin-bottom: 196px;
}

.sns-icon-banner {
    position: absolute;
    left: 0;
    top: -18px;
    z-index: 1;
}

.youtube-icon {
    position: absolute;
    width: 16px;
    left: 10px;
    top: -16px;
    z-index: 2;
}

.y-sumnail {
    border-radius: 5px;
    border: 3px solid #F4D153;
}

.y-movie {
    border-radius: 5px;
    border: 3px solid #F4D153;
}

.ymovie-title {
    padding-top: 30px;
    height: 60px;
    font-weight: bold;
    font-size: 14px;
}

.ymovie-view-count {
    padding-top: 5px;
    font-size: 12px;
}

.ymovie-publishedat{
    padding-top: 5px;
    font-size: 12px;
}

.like-count {
    position: absolute;
    left: 120px;
    top: 121px;
    font-size: 8px;
}

.like-icon {
    position: absolute;
    left: 120px;
    top: 95px;
    height: 20px;
}

.dislike-count {
    position: absolute;
    left: 170px;
    top: 121px;
    font-size: 8px;
}

.dislike-icon {
    position: absolute;
    left: 170px;
    top: 95px;
    height: 20px;
}

.tw-profile-image {
    position: absolute;
    left: 5px;
    top: 5px;
    border-radius: 100%;
    border: 1px solid #F4D153;
}

.tw-username-box {
    position: absolute;
    text-align: left;
    width: 80%;
    height: 25px;
    left: 65px;
    top: 5px;
}

.tw-user-name{
    display: inline-block;
    font-weight: bold;
}

.tw-verified-img{
    width: 15px;
    margin-left: 5px;
}

.tw-text{
    position: absolute;
    left: 65px;
    top: 30px;
    width: 75%;
    font-size: 14px;
}

.foot-space{
    height: 75px;
}

.foot-nav {
    position: fixed;
    z-index: 4;
    left: 5%;
    top: 90%;
    width: 90%;
    height: 58px;

    background: #FFFFFF;
    box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.25);
    border-radius: 45px;
}

.oshido-circle-img {
    position: fixed;
    z-index: 5;
    width: 64px;
    height: 64px;
    left: 41.5%;
    top: 89.5%;
}

.oshido-circle2 {
    position: fixed;
    z-index: 4;
    width: 67px;
    height: 67px;
    left: 41.23%;
    top: 89%;

    background: #FFFFFF;
    border-radius: 45px;
}

</style>