<template>
    <div>
    <h1>REVOKE BOOK</h1>
    <form>
        <button type="button" @click="revoke">Revoke</button>
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
            value: false,
            name: null,
            desc: null
        }
    },
    created(){
        this.book_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        this.user_id = 0
        console.log(this.book_id)
    },
    methods: {
        revoke(){
            axios
            .post(`http://localhost:5000/api/revoke/${this.book_id}`,
            {status: this.value},
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                this.message = response.data.message
                if (response.status == 201){
                    this.$router.push('/libdash')
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