<template>
    <div>
    <h1>RETURN BOOK</h1>
    <form>
        <button type="button" @click="returns">Return</button>
    </form>
    <p>{{ this.message }} </p>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    data() {
        return {
            token: null,
            message: null,
            id: null,
            book_id: null,
            user_id: null,
            value: true,
            name: null,
            desc: null
        }
    },
    created(){
        this.book_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        this.user_id = localStorage.getItem('id')
        console.log(this.book_id)
    },
    methods: {
        returns(){
            axios
            .post(`http://localhost:5000/api/return/${this.book_id}`,
            {user_id: this.user_id, status: this.value},
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                this.message = response.data.message
                if (response.status == 201){
                    this.$router.push('/userdash')
                }
            })
            .catch(error => {
                console.log(error);
                this.message = error.response.data.message
            })
        }
    }
}
</script>