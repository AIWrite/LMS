<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/login">    Login   </router-link>
    <router-link to="/register">   Register    </router-link>
    <ul v-if="userRole === 'lib'">
    <router-link to="/createSection">   Create Section    </router-link>
    <router-link to="/createBook">    Create Book   </router-link>
    <router-link :to="{name: 'libDash'}">   Librarian Dashboard   </router-link>
    </ul>
    <ul v-else-if="userRole === 'user'">
    <router-link :to="{name: 'userDash'}">   User Dashboard    </router-link>
    <router-link :to="{name: 'issueBookDash'}">    Issue Book Dashboard    </router-link>
    <router-link to="/updateUser">    Update Profile   </router-link>
    </ul>
    <a @click="logout_fn">    Logout    </a>
  </nav>
<!-- <p>from app.vue</p> -->
  <router-view/>
</template>


<script>
export default {
    computed: {
      userRole() {
      return localStorage.getItem('role');
      },
      loggedIn() {
      return !!this.userRole;
      }
    },
    methods: {
      logout_fn() {
      localStorage.clear();
      this.$router.push('/login');
      window.location.reload(false)
      }
    }
  }

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color:#f0f0f0;
  justify-content: center; /* Center the content horizontally */
  align-items: center; /* Center the content vertically */
  height: 100vh; /* Make the app fill the entire viewport height */
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

