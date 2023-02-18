<template>
    <div>
      <h2>List of Accounts</h2>
      <table>
        <thead>
          <tr>
            <th>Account Address</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account in accounts" :key="account">
            <td>{{ account }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        accounts: []
      }
    },
    mounted() {
      this.getAccounts()
    },
    methods: {
      getAccounts() {
        const url = 'http://localhost:8000/get_accounts/'
        fetch(url)
          .then(response => response.json())
          .then(data => {
            this.accounts = data.accounts
          })
          .catch(error => {
            console.error(error)
          })
      }
    }
  }
  </script>
  