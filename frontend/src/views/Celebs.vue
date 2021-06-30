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
                <iframe  @click="addOshido" width="330" height="185" class="y-movie" v-bind:src="movie.videoUrl" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <div @click="toggleBtn(index)" v-bind:class="{active:isActive[index]}" class="content content-sub">
                <div class="content-sub-top">
                    <div class="content-mini-box">
                        <div class="ymovie-title">{{ movie.title.substring(0,72) }}</div>
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
                        <div class="tw-user-name">{{ tweet.user.name.substring(0,20) }}</div>
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
            <div class="foot-box">
                <router-link to="/iconlist">[icons]</router-link>
                <div>Designed by Freepik and distributed by Flaticon</div>
            </div>
            <div class="foot-space"></div>
            <div class="foot-nav">
                <img src="@/assets/ranking.png" class="ranking-icon">
                <img v-if="oshido>=100" src="@/assets/gold-medal.png" class="medal gold-medal medal-1">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-1">
                <img v-if="oshido>=50" src="@/assets/silver-medal.png" class="medal silver-medal medal-2">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-2">
                <img v-if="oshido>=20" src="@/assets/bronze-medal.png" class="medal bronze-medal medal-3">
                <img v-else src="@/assets/no-medal.png" class="medal no-medal medal-3">
                <img src="@/assets/home.png" class="home-icon">
                <img src="@/assets/user.png" class="user-icon">
                <img v-if="sideMenuActive!=true" @click="toggleList" src="@/assets/list.png" class="list-icon">
                <img v-else @click="toggleList" src="@/assets/list-open.png" class="list-icon">
                <img src="@/assets/footer.png" class="footer-img">
                <div class="oshido">{{ watchedContentCount }}</div>
            </div>
        </footer>

        <!-- <transition name="slide"> -->
            <div v-show="sideMenuActive" class="side-menu">
                <img src="@/assets/hammburger.png" class="side-menu">
                <table class="side-menu-content-box">
                    <tr v-for="oshi in oshiList" v-bind:key="oshi.name">
                        <td class="oshi-list-name">{{ oshi.celeb_name.substring(0,10) }}</td>
                        <td class="oshi-list-oshido-label">オシ度</td>
                        <td class="oshi-list-oshido">{{ oshi.oshido }}</td>
                    </tr>
                </table>
            </div>
        <!-- </transition> -->

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
            maxResults: "5",
            isActive: {
                type: [Boolean],
                default: false
            },
            sideMenuActive: false,
            isntOshi: true,
            oshido: '',
            oshiList: '',
            scrollY: 0,
            watchedCount: 0
        };
    },
    mounted() {
        this.getYoutube() // Youtubeの動画取得
        this.getTweet() // Twitterの動画取得
        this.isOshi() // ユーザーが検索された有名人を推しているか判定
        this.getOshiList() // ユーザーの推しリストを取得
        window.addEventListener('scroll', this.onScroll)
    },
    computed: {
        watchedContentCount: function() {
            if(this.scrollY % 200 == 0 && this.scrollY != 0) {
                this.addWatchedCount()
                this.updateOshido()
            }
            return this.oshido
        }
    },
    methods: {
        resetScrollY: function() {
            this.scrollY = 0
        },
        addWatchedCount: function() {
            this.oshido++
        },
        onScroll: function() {
            this.scrollY = window.pageYOffset
        },
        toggleBtn: function(i) {
            this.isActive[i] = !this.isActive[i]
        },
        toggleList: function() {
            this.sideMenuActive = !this.sideMenuActive
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
                    axios.post("http://localhost:5000/register_oshido", {
                        uid: user.uid,
                        celeb_name: this.name,
                        oshido: 0
                    })
                    .then(response => {
                        console.log(response)
                        this.isntOshi = false
                        this.getOshiList()
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
                    axios.delete("http://localhost:5000/delete_oshido", {
                        params: {
                            uid: user.uid,
                            celeb_name: this.name,
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.isntOshi = true
                        this.getOshiList()
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
            axios.get("http://localhost:5000/get_twitter_data", {
                params: {
                    q: this.name,
                    maxResults: this.maxResults
                }
            })
            .then(response => {
                console.log(response)
                this.celebTwInfo = response.data[0];
            })
            .catch(error => {
                console.log(error.response)
            })
        },
        getYoutube: function() {
            axios.get("http://localhost:5000/get_youtube_data", {
                params: {
                    q: this.name,
                    maxResults: this.maxResults
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
                    axios.get("http://localhost:5000/get_oshido", {
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
        },
        getOshiList: function() {
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    axios.get("http://localhost:5000/get_oshido_list", {
                        params: {
                            uid: user.uid,
                        }
                    })
                    .then(response => {
                        console.log(response)
                        this.oshiList = response.data[0]
                    })
                    .catch(error => {
                        console.log(error.response)
                    })
                }
            });
        },
        addOshido: function() {
            this.oshido++
        },
        updateOshido: function() {
            firebase.auth().onAuthStateChanged((user) => {
                if (user) {
                    axios.put("http://localhost:5000/update_oshido", {
                            uid: user.uid,
                            celeb_name: this.name,
                            oshido: this.oshido
                    })
                    .then(response => {
                        console.log(response)
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
    margin-left: 2px;
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
    font-size: 13px;
}
/* ---footer--- */
.foot-space {
    height: 75px;
}

.foot-box {
    width: 341px;
    height: 50px;
    margin: 40px auto 0 auto;
    font-size: 14px;
    text-align: center;
    background-color: rgb(63, 63, 63);
    color: #FFFFFF;
}

.foot-nav {
    position: fixed;
    z-index: 7;
    left: 0;
    right: 0;
    margin: auto;
    top: 90%;
    width: 341px;
    text-align: center;
}

.footer-img {
    display: inline;
    inline-size: 341px;
}

.oshido {
    position: fixed;
    z-index: 8;
    width: 20px;
    left: 0;
    right: 2px;
    margin: auto;
    text-align: center;
    top: 92%;
    color: white;
    font-family: Noto Sans JP;
    font-style: normal;
    font-weight: bold;
}

.medal {
    position: absolute;
    width: 25px;
}

.no-medal {
    opacity: 20%;
}

.medal-1 {
    left: 48px;
    top: 25px;
}

.medal-2 {
    left: 78px;
    top: 25px;
}

.medal-3 {
    left: 108px;
    top: 25px;
}

.gold-medal {
    left: 51px;
}

.silver-medal {
    left: 81px;
}

.bronze-medal {
    left: 111px;
}

.home-icon {
    position: absolute;
    width: 23px;
    left: 210px;
    top: 25px;
}

.user-icon {
    position: absolute;
    width: 23px;
    left: 255px;
    top: 25px;
}

.list-icon {
    position: absolute;
    width: 23px;
    left: 300px;
    top: 25px;
}

.ranking-icon {
    position: absolute;
    width: 26px;
    left: 13px;
    top: 23px;
}
/* ---side menu--- */
.side-menu {
    position: fixed;
    width: 362px;
    height: 812px;
    top: 0;
    right: -35px;
    z-index: 6;
}

.side-menu-content-box {
    position: absolute;
    left: 40px;
    top: 100px;
    width: 250px;
    z-index: 7;
    font-family: Noto Sans JP;
    font-style: normal;
    font-weight: bold;
    color: white;
}

.oshi-list-name {
    font-size: 20px;
    line-height: 35px;
}

.oshi-list-oshido-label {
    font-size: 12px;
    line-height: 26px;
    width: 40px;
    padding-left: 60px;
}

.oshi-list-oshido {
    font-size: 24px;
    line-height: 43px;
    padding-left: 10px;
}

/* .active2{
    transform: translateX(170px);
} */

/* .slide-enter, .slide-leave-to {
    transform: translateX(100%);
}
.slide-enter-to, .slide-leave {
    transform: translateX(0);
}
.slide-enter-active, .slide-leave-active {
    transition: transform 1s;
} */

</style>