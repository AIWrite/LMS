<template>
    <div>
    <h1>UPDATE BOOK</h1>
    <form>
        <input type="text" name="" id="" placeholder="Book Name" v-model="this.name"><br><br>
        <input type="text" name="" id="" placeholder="Authors" v-model="this.authors"><br><br>
        <input type="text" name="" id="" placeholder="Description" v-model="this.desc"><br><br>
        <input type="text" name="" id="" placeholder="Content" v-model="this.content"><br><br>
        <label for="cars">Choose a section:</label>
            <select name="cars" id="cars" v-model="this.id" v-if="sections">
                <option v-for="section in this.sections" :key="section.id"  :value=" section.id ">{{ section.name }}</option>
            </select>
        <button type="button" @click="upBook">Update</button>
    </form>
    <p>{{ this.message }} </p>
    </div>
</template>
<script>
import axios from 'axios';
export default{
    data() {
        return {
            authors: null,
            content: null,
            token: null,
            message: null,
            book_id: null,
            id: null,
            sections: null,
            name: null,
            desc: null
        }
    },
    created(){
        this.book_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        console.log(this.book_id)
        if (!this.token){
            this.$router.push('/login');
        }else{
            this.fetchsection()
        }
    },
    methods: {
        fetchsection() {
            axios
            .get('http://localhost:5000/api/section', {
                headers: { Authorization: `${this.token}` },
            })
            .then(response => {
                if (response.status === 200) {
                    this.sections = response.data.data;
                }
            })
            .catch(error => {
                console.log(error);
            });
        },

        upBook(){
            axios
            .put(`http://localhost:5000/api/book/${this.book_id}`,
            {name: this.name, authors: this.authors, description: this.desc, content: this.content, section_id: this.id},
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