<template>
    <div class="update">
        <h1>UPDATE PROFILE</h1>
        <form>
            <label for="email">Email:</label><br>
            <input type="text" id="email" name="email" v-model="this.emailv"><br>
            
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" v-model="this.passwordv"><br>

            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" v-model="this.usernamev"><br>

            <input type="button" @click="update_fn" value="UPDATE PROFILE">
        </form>
    </div>
</template>
<script>

import axios from 'axios';

export default{
    data() {
        return {
            id: null,
            emailv: '',
            passwordv: '',
            usernamev: ''
        }
    },
    created(){
        this.id = localStorage.getItem('id')
        this.token = localStorage.getItem('token')
        console.log(this.id)
        if (!this.token){
            this.$router.push('/login');
        }
    },
    methods: {
        update_fn() {
        axios
        .put(`http://localhost:5000/api/update/${this.id}`,
            {email: this.emailv, password: this.passwordv, username: this.usernamev},
            {headers: {Authorization: `${this.token}`},}
            )
        .then(response => {
            console.log('catched response: '+ response.status)
            console.log(response.data.message);
            if (response.status == 201) {
                localStorage.clear();
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