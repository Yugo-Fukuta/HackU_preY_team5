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
            celebInfo: ''
        };
    },
    mounted() {
        axios.get('https://jsonplaceholder.typicode.com/users')
        .then(response => {
            console.log(response)
            this.celebInfo = response.data[0]
        })
        .catch(error => {
            console.log(error)
        })
    }
}
</script>