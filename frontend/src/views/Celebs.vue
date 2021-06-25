<template>
    <div class="container">
        <div class="blank"></div>
        <div class="header">
            <div class="search-box">
                <img src="@/assets/search.png" class="search-icon">
                <input @keydown.enter="trigger" v-model="newName" class="input-form">
                <img @click="addOshi" src="@/assets/like.png" class="like-button">
                <!-- <img @click="deleteOshi" src="@/assets/like.png" class="like-button"> -->
            </div>
        </div>
        <div v-for="(movie, index) in celebInfo" v-bind:key="movie.videoUrl">
                <div class="ycontent">
                    <iframe width="330" height="185" class="y-movie" v-bind:src="movie.videoUrl" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                <div @click="toggleBtn(index)" v-bind:class="{active:isActive[index]}" class="ycontent ycontent-sub">
                    <img src="@/assets/content-banner.png" class="content-banner">
                </div>
        </div>

        <footer>
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
            params: {
                q: "", // 検索クエリを指定
                part: "snippet",
                type: "video",
                maxResults: "5", // 最大検索数
                key: process.env.VUE_APP_YOUTUBE_API_KEY
            },
            isActive: {
                type: [Boolean],
                default: false
            },
        };
    },
    mounted() {
        this.params.q = this.name;
        axios.get("http://localhost:5000/get_youtube_data", {
            params: {
                q: this.params.q,
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
                    axios.post("http://localhost:5000/register_oshido", {
                        uid: user.uid,
                        celeb_name: this.params.q,
                        oshido: 0
                    })
                    .then(response => {
                        console.log(response)
                        this.celebInfo = response.data.items
                    })
                    .catch(error => {
                        console.log(error.response.data)
                    })
                } else {
                    this.$router.push('/signup')
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

.ycontent {
    width: 341px;
    height: 193px;
    margin: 0 auto 20px auto;
    background: #FFFFFF;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
    border-radius: 5px;

    transition: 0.5s;
    position: relative;
    z-index: 2;
}

.ycontent-sub {
    margin-top: -210px;
    position: relative;
    z-index: 1;
}

.y-sumnail {
    border-radius: 5px;
    border: 3px solid #F4D153;
}

.y-movie {
    border-radius: 5px;
    border: 3px solid #F4D153;
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

.content-banner {
    width: 100%;
    position: absolute;
    left: 0;
    top: 94%;
    z-index: 6;
}

.active {
    transform: translateY(170px);
    margin-bottom: 190px;
}

</style>