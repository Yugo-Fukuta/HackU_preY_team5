<template>
  <router-view :key="$route.fullPath"></router-view>
</template>

<style>
#app {
  font-family: "Segoe UI", Meiryo, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}
#nav a.router-link-exact-active {
  color: #42b983;
}
.container {
    width: 95%;
    margin: 0 auto;
}
input {
    border: none;
}
input:focus {
outline: none;
}
</style>
