<template>
    <div>
    <h1>GRANT BOOK</h1>
    <form>
        <button type="button" @click="grant">Grant</button>
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
            value: true,
            name: null,
            desc: null
        }
    },
    created(){
        this.book_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        console.log(this.book_id)
    },
    methods: {
        grant(){
            axios
            .post(`http://localhost:5000/api/grant/${this.book_id}`,
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

