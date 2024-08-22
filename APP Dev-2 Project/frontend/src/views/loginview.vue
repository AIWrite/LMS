<template>
    <div class="login">
      <h1>LOGIN PAGE</h1>
      <form>
        <label for="username">Email:</label><br>
        <input type="text" id="username" name="username" v-model="this.emailv"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" v-model="this.passwordv"><br><br>
        <input type="button" @click="combinedFn" value="login">
      </form>
    </div>
</template>
<script>
import axios from 'axios'

export default {

    data() {
        return {
            emailv: '',
            passwordv: ''
        }
    },
    methods: {

        combinedFn() {
        this.logout_fn();
        this.login_fn();
        },
        
        logout_fn() {
        localStorage.clear();
        this.$router.push('/login');
        },

        login_fn() {    
        console.log('Login page mounted.')
        console.log('username: ' +this.emailv);
        console.log('password: '+this.passwordv);

        axios
        .post('http://localhost:5000/api/login', {
            email: this.emailv,
            password: this.passwordv
        })
        .then(response => {
            console.log(response);
            console.log(response.data);
            console.log(response.data.email);
            console.log(response.data.id);
            console.log(response.data.token);
            console.log(response.data.role);
            console.log(response.data.message);
            if (response.status == 200) {
                localStorage.setItem('token', response.data.authToken);
                localStorage.setItem('id', response.data.id);
                localStorage.setItem('email', response.data.email);
                localStorage.setItem('role', response.data.role);
                this.$router.push('/');
                window.location.reload(false)
            }
            
        })
        .catch(error => {
            console.log('catched error: ' + error)
        })
        
    } 
}
}
</script>
