<template>
    <div class="big-container">
        <div class="container">
            <div class="app-title">Osuuu!</div>
            <div class="form-name">
                <input @keydown.enter="trigger" v-model="newName" class="input-form-top" placeholder="  気になる人物の名前を入力">
            </div>
        </div>
        <div id="trend_wrapper">
            <div id="trendtitle">現在の検索トレンド!!</div>
            <div v-for="(data, key) in trendInfo" :key="key" class="trends">
                <span @click="pageTransition(data)">{{ data }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    el: '#app',
    data() {
        return {
            name: '',
            newName: '',
            trendInfo: '',
            maxResults: "5",
        };
    },
    mounted() {
        this.getTrend()
    },
    methods: {
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

        getTrend: function() {
            axios.get(process.env.VUE_APP_API_BASE_URL + "/get_trend/", {
                params: {
                    maxResults: this.maxResults
                }
            })
            .then(response => {
                console.log(response)
                this.trendInfo = response.data;
            })
            .catch(error => {
                console.log(error.response)
            })
        },
        pageTransition: function(data) {
            this.$router.push({
                name: 'Celebs',
                params: {
                    celebName: data
                }
            })
        },

    },
}
</script>

<style>
/* .container {
    background-color: #F4D153;
} */

body{
    font-family: Arial, Helvetica, sans-serif;
    margin: 0 auto;
    /*background-color: #F4D153;*/
}
.big-container {
    position:absolute;
    width: 100%;
    margin: 0 auto;
    background-color: #F4D153;
    height: 100%;
}

.app-title {
    font-family: Arial;
    font-style: italic;
    position:static;
    width: 300px;
    height: 37px;
    /*top: 15%;*/
    margin: 0 auto;
    margin-top: 150px;
    /*left: 0;
    right: 0;*/
    color: #FFFFFF;
    text-align: center;
    font-size: 70px;
    font-weight: bold;
}

.input-form-top {
    position: relative;
    margin: 0 auto;
    height: 37px;
    width: 90%;
    padding: 0 5px;
    /*top: 30%;*/
    margin-top: 70px;
    left: 4%;
    background: #FFFFFF;
    border-radius: 5px;
    font-size: 15px;
}

#trend_wrapper{
    margin:0 auto;
    margin-top: 50px;
}

#trendtitle{
    width: 200px;
    margin: 0 auto;
    font-size: 18px;
    text-align:center;
    font-style: italic;
    font-weight: bold;
}

.trends{
    position: static;
    margin: 0 auto;
    margin-top: 15px;
    font-size: 16px;
    text-align: center;
    font-weight: bold;
}
span{
    background-color: rgba(255, 255, 255, .5);
    padding: 4px;
    cursor: pointer;
    color: #07f;
    border: 2px solid #07f;
    border-radius: 3px;
}
span:hover{
    color: #f0f;
    border: 2px solid #f0f;
}
</style>