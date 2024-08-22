<template>
    <div>
    <h1>UPDATE SECTION</h1>
    <form>
        <input type="text" name="" id="" placeholder="Section Name" v-model="this.name"><br><br>
        <input type="text" name="" id="" placeholder="Section Description" v-model="this.desc"><br><br>
        <button type="button" @click="upSection">Update</button>
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
            section_id: null,
            id: null,
            name: null,
            desc: null
        }
    },
    created(){
        this.section_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        // console.log(this.token);
        if (!this.token){
            this.$router.push('/login');
        }else{
            this.fetchsection()
        }
    },
    methods: {
        fetchsection() {
            axios
            .patch(`http://localhost:5000/api/section/${this.section_id}`,
            {headers: {Authorization: `${this.token}`},}
            )
            .then(response => {
                console.log(response);
                // this.message = response.data.message
                if (response.status == 200){
                    // this.categories = response.data.data
                    this.section_id = response.data.id
                }
            })
            .catch(error => {
                console.log(error);
                // this.message = error.response.data.message
            })
        },
        upSection(){
            axios
            .put(`http://localhost:5000/api/section/${this.section_id}`,
            {name: this.name, description: this.desc},
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