<template>
    <div class="container">
        <h2>推し検索</h2>
        <div id="app">
            <div class="form-name">
                <p>名前</p>
                <!-- エラーメッセージを追加 -->
                <p class="error-name">1文字以上入力してください</p>
                <input type="text" name="name" placeholder="名前を入力してください" v-model="name">
            </div>
        </div>
        <div>
            <button @click="sendName">送信する</button>
        </div>
    </div>
</template>

<script>
// import axios from 'axios'
export default {
    el: '#app',
    data() {
        return {
            name: ''
        };
    },
    methods: {
        sendName: function() {
            // axios.get('https://jsonplaceholder.typicode.com/users')
            // .then(response => {
            //     console.log(response)
            //     this.$router.push('Celebs')
            // })
            // .catch(error => {
            //     console.log(error)
            // })
            this.$router.push({
                name: 'Celebs',
                params: {
                    celebName: this.name
                }
            })
            console.log(this.name)
        }
    },
}
</script>