<template>
  <div>
    <input v-model="password" type="password" placeholder="Enter Password">
    <button @click="createAccount">Create Account</button>
    <p v-if="accountAddress">Account Address: {{ accountAddress }}</p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>
<script>
import Toastify from 'toastify-js';

export default {
  data() {
    return {
      password: "",
      accountAddress: null,
      errorMessage: null,
    };
  },
  methods: {
    async createAccount() {
      try {
        const response = await fetch('http://127.0.0.1:8000/create_account/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: JSON.stringify({
            'password': this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          this.accountAddress = data.address;
          this.errorMessage = null;
          Toastify({
            text: 'Account created successfully!',
            backgroundColor: 'green',
            gravity: 'top',
            position: 'center'
          }).showToast();
        } else {
          this.accountAddress = null;
          this.errorMessage = "Failed to create account";
          Toastify({
            text: 'Failed to create account',
            backgroundColor: 'red',
            gravity: 'top',
            position: 'center'
          }).showToast();
        }
      } catch (error) {
        console.error(error);
        this.accountAddress = null;
        this.errorMessage = "An error occurred while creating the account";
        Toastify({
          text: 'An error occurred while creating the account',
          backgroundColor: 'red',
          gravity: 'top',
          position: 'center'
        }).showToast();
      }
    }
  }
}
</script>