<template>
    <div>
      <h3>Get Ethereum balance</h3>
      <input v-model="account" type="text" placeholder="Enter account address" />
      <button @click="getBalance">Get balance</button>
      <p v-if="balance !== null">Balance: {{ balance }} ETH</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        account: '0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264',
        balance: null,
      };
    },
    methods: {
      getBalance() {
        // Make a GET request to the Django view URL with the account parameter
        fetch(`http://localhost:8000/eth_balance/${this.account}/`)
          .then(response => response.json())
          .then(data => {
            if (data.error) {
              console.error(data.error);
            } else {
              this.balance = data.balance;
            }
          })
          .catch(error => console.error(error));
      },
    },
  };
  </script>
  