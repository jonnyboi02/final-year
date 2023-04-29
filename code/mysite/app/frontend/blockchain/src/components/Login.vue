<template>
    <h3>Login</h3>
    <div>
        <form @submit.prevent="login">
            Username: <input type="text">
            <br>
            Password: <input type="password"> 
            <br>
            <button type = 'submit'>Login</button>
        </form>
    </div>
    

</template>

<script>

import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"
import {user} from "../user.js";

user.init()

const apiUrl = 'http://localhost:8000'; // replace this with your API's URL

function login(username, password) {
  return fetch('http://localhost:8000/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then(data => {
      const { token } = data;
      localStorage.setItem('token', token); // store the token in localStorage
      
      return data;
    });
    
}

//import login from 'api.js'
export default{
    data(){
        return{
            username: "",
            password: "",
        }
    },
    methods:{
        login(){
            login(this.username, this.password)
            .then (() => { 
                this.$router.push({name: 'Send Transaction'})
                Toastify({
                    text: 'Login successful' + user.username,
                    backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)",
                    className: 'toastify-content',
                }).showToast();
            })
            .catch(error => {
                Toastify({
                text: 'Login failed',
                backgroundColor: 'red',
                className: 'toastify-content',
            }).showToast();
                console.log('Login Error');
            });
        }

    }
}

</script>