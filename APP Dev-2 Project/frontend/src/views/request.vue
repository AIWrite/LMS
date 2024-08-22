<template>
    <div>
    <h1>REQUEST BOOK</h1>
    <form>
        <button type="button" @click="issue">Request</button>
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
            book_id: null,
            id: null,
            user_id: null,
            value: false,
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
        issue(){
            axios
            .post(`http://localhost:5000/api/request/${this.book_id}`,
            {user_id: this.user_id, status: this.value},
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                this.message = response.data.message
                if (response.status == 201){
                    this.$router.push('/issueBook')
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