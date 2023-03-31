<template>
    <div style="color: white;">
      <h3>Login</h3>
      <form @submit.prevent="login">
        <label>Username:</label> <br>
        <input type="text" v-model="username">
        <br>
        <label>Password:</label> <br>
        <input type="password" v-model="password">
        <br>
        <br>
        <button type="submit">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"
  export default {
    data() {
      return {
        username: '',
        password: '',
      }
    },
    methods: {
      login() {
        fetch('http://localhost:8000/login2/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error('Login failed.');
            }
            return response.json();
          })
          .then((data) => {

            localStorage.setItem('token', data.token);
            localStorage.setItem('username', this.username); 
            localStorage.setItem('password', this.password);

            this.$router.push('/dashboard');
            Toastify({
                    text: 'Login successful' + localStorage.getItem('username') +" "+ localStorage.getItem('password'),
                    backgroundColor: 'green',
                    className: 'toastify-content',
            }).showToast();
            
          })
          .catch((error) => {
            console.log(error);
          });
      },
    },
  };
  </script>
  