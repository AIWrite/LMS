<template>
    <div class="libDash">
        <h1>USER DASHBOARD</h1>
        <input type="text" placeholder="search" v-model="search">
        
        <div v-if="!search">
            <h2>books</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>RETURN DATE</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in books" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.return_at }}</td>
                        <td>
                            <button @click="$router.push({ name: 'views', params: { id: book.id } })">VIEW</button>
                            |
                            <button @click="$router.push({ name: 'returns', params: { id: book.id } })">RETURN</button> 
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div v-else>
            <h2>books</h2>
            <p v-if="filteredBooks.length === 0">No books found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>CONTENT</th>
                        <th>RETURN DATE</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooks" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.content }}</td>
                        <td>{{ book.return_at }}</td>
                        <td>
                            <button @click="$router.push({ name: 'views', params: { id: book.id } })">VIEW</button> 
                            |
                            <button @click="$router.push({ name: 'returns', params: { id: book.id } })">RETURN</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            token: null,
            id: null,
            message: null,
            sections: [],
            books: [],
            search: ''
        }
    },
    computed: {
        filteredBooks() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.books.filter(book => book.name.toLowerCase().includes(searchLower) || book.description.toLowerCase().includes(searchLower) || book.authors.toLowerCase().includes(searchLower) || book.content.toLowerCase().includes(searchLower) || book.username.toLowerCase().includes(searchLower));
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        this.id = localStorage.getItem('id');
        if (!this.token) {
            this.$router.push('/login');
        } else {
            this.fetchbook();
        }
    },
    methods: {
        fetchbook() {
            axios
            .put(`http://localhost:5000/api/userbook/${this.id}`,
            {headers: {Authorization: `${this.token}`}}
            )
                .then(response => {
                    if (response.status === 200) {
                        this.books = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>
