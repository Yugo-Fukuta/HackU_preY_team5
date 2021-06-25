<template>
    <div class="container">
        <div class="form-name">
            <input type="text" name="name" placeholder="名前を入力してください" v-model="name" class="input-form-top">
        </div>
        <div>
            <button @click="sendName" class="osu-button">Osu</button>
        </div>
    </div>
</template>

<script>
export default {
    el: '#app',
    data() {
        return {
            name: ''
        };
    },
    methods: {
        sendName: function() {
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

<style>
.input-form-top {
    position: absolute;
    height: 37px;
    width: 90%;
    top: 30%;
    left: 4%;
    background: #E5E5E5;
    border-radius: 5px;
}

.osu-button {
    
}

</style>