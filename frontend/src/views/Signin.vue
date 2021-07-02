<template>
  <div class="signin">
    <h2>Sign in</h2>
    <input type="text" placeholder="Email" v-model="email">
    <input type="password" placeholder="Password" v-model="password">
    <button @click="signIn">Signin !!</button>
    <p>You don't have an account? 
      <router-link to="/signup">create account now!!</router-link>
    </p>
  </div>
</template>

<script>
import firebase from 'firebase'

export default {
  name: 'Signin',
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
      signIn: function () {
      firebase.auth().signInWithEmailAndPassword(this.email, this.password).then(
        user => {
          alert('Success!', user.email)
          this.$router.push('/')
        },
        err => {
          alert(err.message)
        }
      )
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
.signin {
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
  width: 250px;
  font-size: 15px;
}
button{
margin-top:10px;
font-size: 17px;
background-color:#0af;
border:none;
padding: 6px 10px;
border-radius: 3px;
}
</style>
