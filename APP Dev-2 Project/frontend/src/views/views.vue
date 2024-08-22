<template>
    <div>
        <h2>View Book</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>
                            <button @click="rateBook(book.id)">LIKE</button>
                        </td>
                    </tr>
                </tbody>
                <p>{{ book.content }}</p>
            </table>
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
            book: [],
            message: null,
            book_id: null,
            id: null,
            sections: null,
            name: null,
            like: null,
            desc: null
        }
    },
    created(){
        this.book_id = this.$route.params.id
        this.token = localStorage.getItem('token')
        this.like = 1
        console.log(this.book_id)
        if (!this.token){
            this.$router.push('/login');
        }else{
            this.fetchbookbyid()
        }
    },
    methods: {

        fetchbookbyid() {
            axios
            .get(`http://localhost:5000/api/userbook/${this.book_id}`,
            {headers: {Authorization: `${this.token}`}}
            )
                .then(response => {
                    if (response.status === 200) {
                        this.book= response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },

        rateBook(id) {
            axios
                .post(`http://localhost:5000/api/like/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    console.log(response);
                    this.message = response.data.message
                })
                .catch(error => {
                    console.log(error);
                    this.message = error.response.data.message
                })
        }

    }
}
</script>