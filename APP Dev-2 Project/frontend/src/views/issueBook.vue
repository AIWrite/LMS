<template>
    <div class="issueBookDash">
        <h1>This is an user issue dashboard</h1>
        <input type="text" placeholder="search" v-model="search">
        
        <div v-if="!search">
            <h2>Books (NOT REQUESTED)</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>RATING</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in booksnotrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.like }}</td>
                        <td>
                            <button @click="$router.push({ name: 'request', params: { id: book.id } })">Request</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div v-else>
            <h2>Books (NOT REQUESTED)</h2>
            <p v-if="filteredBooksnotrequested.length === 0">No books found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>RATING</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooksnotrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.like }}</td>
                        <td>
                            <button @click="$router.push({ name: 'request', params: { id: book.id } })">Request</button>
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
            user_id: null,
            booksnotrequested: [],
            search: ''
        }
    },
    computed: {
        filteredBooksnotrequested() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.booksnotrequested.filter(book => book.name.toLowerCase().includes(searchLower) || book.description.toLowerCase().includes(searchLower) || book.authors.toLowerCase().includes(searchLower) || book.content.toLowerCase().includes(searchLower) || book.username.toLowerCase().includes(searchLower));
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        this.user_id = localStorage.getItem('id');
        if (!this.token) {
            this.$router.push('/login');
        } else {
            this.fetchbooksnotrequested();
        }
    },
    methods: {
        fetchbooksnotrequested() {
            axios
                .patch(`http://localhost:5000/api/book`,
                {headers: { Authorization: `${this.token}`}}
                )
                .then(response => {
                    if (response.status === 200) {
                        this.booksnotrequested = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>

