<template>
  <div class="signup">
    <h2>Sign up</h2>
    <input type="text" placeholder="Email" v-model="email">
    <input type="password" placeholder="Password" v-model="password">
    <button @click="signUp">Register</button>
    <p>Do you have an account? 
      <router-link to="/signin">sign in now!!</router-link>
    </p>
  </div>
</template>

<script>
import firebase from 'firebase'
import axios from 'axios'

export default {
  name: 'Signup',
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    signUp: function() {
        firebase.auth().createUserWithEmailAndPassword(this.email, this.password)
        .then(response => {
            alert('Create account: ', response.user.email)
            this.registerNickname(response.user.uid)
            this.$router.push("/")
        })
        .catch(error => {
            alert(error.message)
        })
    },
    registerNickname: function(uid) {
      axios.post(process.env.VUE_APP_API_BASE_URL + "/register_nickname/", {
          uid: uid,
      })
      .then(response => {
          console.log(response)
      })
      .catch(error => {
          console.log(error.response.data)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.signup {
  margin-top: 20px;
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center
}
input {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #777;
  border-radius: 3px;
}
</style>
