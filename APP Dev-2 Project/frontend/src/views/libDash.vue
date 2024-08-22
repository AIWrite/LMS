<template>
    <div class="libDash">
        <h1>LIBRARIAN DASHBOARD</h1>
        <input type="text" placeholder="search" v-model="search">
        
        <div v-if="!search">
            <h2>sections</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>DESCRIPTION</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="section in sections" :key="section.id">
                        <td>{{ section.name }}</td>
                        <td>{{ section.description }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateSection', params: { id: section.id } })">UPDATE</button>
                            | 
                            <button @click="deleteSection(section.id)">DELETE</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        
            <h2>Books (NOT REQUESTED)</h2>
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
                    <tr v-for="book in booksnotrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h2>Books (REQUESTED)</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>REQUESTED BY</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in booksrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.username }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                            |
                            <button @click="$router.push({ name: 'grant', params: { id: book.id } })">GRANT</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h2>Books (ISSUED)</h2>
            <table>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>ISSUED TO</th>
                        <th>REVOKE ON</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in booksissued" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.username }}</td>
                        <td>{{ book.return_at }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                            |
                            <button @click="$router.push({ name: 'revoke', params: { id: book.id } })">REVOKE</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <button @click="downloadCSV()">Download CSV</button>

            <h2>Users</h2>
            <table>
                <thead>
                    <tr>
                        <th>USERNAME</th>
                        <th>Email</th>
                        <th>Granted/Requested</th>
                        <th>Revoked/Returned</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.granted }}</td>
                        <td>{{ user.revoked }}</td>
                        <td>
                            <button @click="deleteUser(user.id)">DELETE</button>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>
        
        <div v-else>
            <h2>section</h2>
            <p v-if="filteredSections.length === 0">No section found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>DESCRIPTION</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="section in filteredSections" :key="section.id">
                        <td>{{ section.name }}</td>
                        <td>{{ section.description }}</td>
                        <td>{{ section.status }} | {{ section.delete }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateSection', params: { id: section.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteSection(section.id)">DELETE</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <h2>Books (NOT REQUESTED)</h2>
            <p v-if="filteredBooksnotrequested.length === 0">No books found</p>
            <table v-else>
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
                    <tr v-for="book in filteredBooksnotrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h2>Books (REQUESTED)</h2>
            <p v-if="filteredBooksrequested.length === 0">No books found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>REQUESTED BY</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooksrequested" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.username }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                            |
                            <button @click="$router.push({ name: 'grant', params: { id: book.id } })">GRANT</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h2>Books (ISSUED)</h2>
            <p v-if="filteredBooksissued.length === 0">No books found</p>
            <table v-else>
                <thead>
                    <tr>
                        <th>NAME</th>
                        <th>AUTHORS</th>
                        <th>DESCRIPTION</th>
                        <th>SECTION</th>
                        <th>ISSUED TO</th>
                        <th>REVOKE ON</th>
                        <th>ACTION</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="book in filteredBooksissued" :key="book.id">
                        <td>{{ book.name }}</td>
                        <td>{{ book.authors }}</td>
                        <td>{{ book.description }}</td>
                        <td>{{ book.section_name }}</td>
                        <td>{{ book.username }}</td>
                        <td>{{ book.return_at }}</td>
                        <td>
                            <button @click="$router.push({ name: 'updateBook', params: { id: book.id } })">UPDATE</button> 
                            | 
                            <button @click="deleteBook(book.id)">DELETE</button>
                            |
                            <button @click="$router.push({ name: 'revoke', params: { id: book.id } })">REVOKE</button>
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
            message: null,
            sections: [],
            id: null,
            user_id: null,
            users: [],
            booksnotrequested: [],
            booksrequested: [],
            booksissued: [],
            search: ''
        }
    },
    computed: {
        filteredSections() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.sections.filter(section => section.name.toLowerCase().includes(searchLower));
        },
        filteredBooksnotrequested() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.booksnotrequested.filter(book => book.name.toLowerCase().includes(searchLower) || book.description.toLowerCase().includes(searchLower) || book.authors.toLowerCase().includes(searchLower));
        },
        filteredBooksrequested() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.booksrequested.filter(book => book.name.toLowerCase().includes(searchLower) || book.description.toLowerCase().includes(searchLower) || book.authors.toLowerCase().includes(searchLower) || book.username.toLowerCase().includes(searchLower));
        },
        filteredBooksissued() {
            const searchLower = this.search ? this.search.toLowerCase() : '';
            return this.booksissued.filter(book => book.name.toLowerCase().includes(searchLower) || book.description.toLowerCase().includes(searchLower) || book.authors.toLowerCase().includes(searchLower) || book.username.toLowerCase().includes(searchLower));
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        this.user_id = localStorage.getItem('id');
        if (!this.token) {
            this.$router.push('/login');
        } else {
            this.fetchsection();
            this.fetchbooksnotrequested();
            this.fetchbooksrequested();
            this.fetchbooksissued();
            this.fetchusers();
        }
    },
    methods: {
        downloadCSV(){
            axios
                .get('http://localhost:5000/createcsv')
                .then(response => {
                    if (response.status === 200) {
                        console.log(response);
                        window.location.href = "http://localhost:5000/downloadcsv"
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        fetchusers() {
            axios
                .get('http://localhost:5000/api/allusers', {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 200) {
                        this.users = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
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
        fetchbooksnotrequested() {
            axios
            .patch(`http://localhost:5000/api/book`,
            {headers: {Authorization: `${this.token}`}}
            )
                .then(response => {
                    if (response.status === 200) {
                        this.booksnotrequested = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        fetchbooksrequested() {
            axios
            .post(`http://localhost:5000/api/book/${this.user_id}`,
            {headers: {Authorization: `${this.token}`}}
            )
                .then(response => {
                    if (response.status === 200) {
                        this.booksrequested = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        fetchbooksissued() {
            axios
            .patch(`http://localhost:5000/api/book/${this.user_id}`,
            {headers: {Authorization: `${this.token}`}}
            )
                .then(response => {
                    if (response.status === 200) {
                        this.booksissued = response.data.data;
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteUser(id) {
            axios
                .delete(`http://localhost:5000/api/revoke/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 201) {
                        this.fetchusers();
                        this.fetchbooksnotrequested();
                        this.fetchbooksrequested();
                        this.fetchbooksissued();
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteSection(id) {
            axios
                .delete(`http://localhost:5000/api/section/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 201) {
                        this.fetchsection();
                    }
                })
                .catch(error => {
                    console.log(error);
                });
        },
        deleteBook(id) {
            axios
                .delete(`http://localhost:5000/api/book/${id}`, {
                    headers: { Authorization: `${this.token}` },
                })
                .then(response => {
                    if (response.status === 201) {
                        this.fetchbooksnotrequested();
                        this.fetchbooksrequested();
                        this.fetchbooksissued();
                        console.log(this.token)
                    }
                })
                .catch(error => {
                    console.log(error);
                    console.log(this.token)
                });
        }
    }
}
</script>
