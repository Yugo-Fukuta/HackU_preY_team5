<template>
    <div class="container">
        {{ name }}
        {{ celebInfo }}
    </div>
</template>

<script>
import axios from 'axios'

export default {
    el: '#app',
    data() {
        return {
            name: this.$route.params.celebName,
            celebInfo: '',
            params: {
                q: "", // 検索クエリを指定
                part: "snippet",
                type: "video",
                maxResults: "5", // 最大検索数
                key: process.env.VUE_APP_YOUTUBE_API_KEY
            }
        };
    },
    mounted() {
        this.params.q = this.name;
        axios.get("https://www.googleapis.com/youtube/v3/search", {
            params: this.params
        })
        .then(response => {
            console.log(response)
            this.celebInfo = response
        })
        .catch(error => {
            console.log(error)
        })
    }
}
</script>