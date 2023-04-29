<template>
    <div  class="login-box" style="color: white;">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="user-box" >
          
          <input id = 'username' type="text" name="" required="" v-model="username">
     
          <label>Username</label> 
        
      </div>
      <div class="user-box">
        <input id = 'password' type="password" name="" required="" v-model="password">
        <label>Password</label> 
        
      </div>
      <a  type="submit" @click="login">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Submit
            </a>
        <!-- <button type="submit">Submit</button> -->
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
        // Toastify({
        //             text: 'Login',
        //             backgroundColor: 'green',
        //             className: 'toastify-content',
        //     }).showToast();
        this.username = document.getElementById('username').value
        this.password = document.getElementById('password').value
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
                    backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)",
                    className: 'toastify-content',
            }).showToast();
            
          })
          .catch((error) => {
            Toastify({
                    text: 'Login unsuccessful',
                    backgroundColor: 'red',
                    className: 'toastify-content',
            }).showToast();
          });
      },
    },
  };
  </script>
