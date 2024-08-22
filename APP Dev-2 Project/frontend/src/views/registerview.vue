<template>
    <div class="register">
        <h1>USER REGISTERATION</h1>
        <form>
            <label for="email">Email:</label><br>
            <input type="text" id="email" name="email" v-model="this.emailv"><br>
            
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" v-model="this.passwordv"><br>

            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" v-model="this.usernamev"><br>

            <input type="button" @click="register_fn" value="SIGN-UP">
        </form>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'RegisterView',
  data() {
    return {
      emailv: '',
      passwordv: '',
      usernamev: ''
    }
  },
  methods: {
    register_fn() {
        axios
        .post('http://localhost:5000/api/register', {
            email: this.emailv,
            password: this.passwordv,
            username: this.usernamev
        })
        .then(response => {
            console.log('catched response: '+ response.status)
            console.log(response.data.message);
            if (response.status == 201) {
                this.$router.push('/login');
            }
            
        })
        .catch(error => {
            console.log('catched error: ' + error)
        })
    }
  }
}
</script>