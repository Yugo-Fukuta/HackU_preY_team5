<template>
    <div class="big-container">
        <div class="container">
            <div class="app-title">Osuuu!</div>
            <div class="form-name">
                <input @keydown.enter="trigger" v-model="newName" class="input-form-top" placeholder="名前を入力してください">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    el: '#app',
    data() {
        return {
            name: '',
            newName: ''
        };
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
        }
    },
}
</script>

<style>
/* .container {
    background-color: #F4D153;
} */

.big-container {
    background-color: #F4D153;
    height: 800px;
}

.app-title {
    position: absolute;
    width: 60%;
    height: 37px;
    top: 15%;
    margin: auto;
    left: 0;
    right: 0;
    color: #FFFFFF;
    text-align: center;
    font-size: 60px;
    font-weight: bold;
}

.input-form-top {
    position: absolute;
    height: 37px;
    width: 90%;
    top: 30%;
    left: 4%;
    background: #FFFFFF;
    border-radius: 5px;
}

</style>