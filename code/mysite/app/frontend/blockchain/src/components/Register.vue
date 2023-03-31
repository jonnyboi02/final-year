<template>
    <div style="color: white;">
    <h3>Hi {{form['username'] }}</h3>

    <div>
        <!-- <form ref="form"> -->
            
            Username: <br>
            <input class = 'form-control' v-model='form["username"]' /><br>
            
            Password: <br>
            <input class = 'form-control' type = 'password' v-model='form["password"]'/> <br>
            <br>
                <button @click="registerUser">Register</button>
            
           
            
            {{message}}
            <p v-if="accountAddress">Account Address: {{ accountAddress }}</p>
            <p v-if="check">Account Address: {{ check }}</p>


        <!-- </form> -->
    </div>
    </div>

</template>

<script>

import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"

export default{
    data(){
        return{
            accountAddress: null,
            errorMessage: null,
            message: "",
            form:{
                username : "",
                password : "",
            },
            check: null,

        }
    },
    methods :{
        async registerUser(){
            if (this.form.username === ""){
               // this.message = "Username cannot be empty!";
                //alert("Username cannot be empty!");
                Toastify({
                    text: 'Username cannot be empty!',
                    backgroundColor: 'red',
                    gravity: 'top',
                    position: 'right'
                }).showToast();
            }
            else{
                
            const response = await fetch("http://127.0.0.1:8000/register/", {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form),
            });
             
            if (response.ok){
                Toastify({
                    text: 'Account Created Successfully! ' ,
                    backgroundColor: 'green',
                    gravity: 'top',
                    position: 'right'
                }).showToast();
                const response = await fetch('http://127.0.0.1:8000/get-user-details/', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 'username': this.form.username }),
                });
                const data = await response.json();
                this.accountAddress = data.public_key;
            //     const api = await fetch("http://127.0.0.1:8000/public_key/", {
            //     method: 'POST',
            //     headers: {
            //     'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify({'username': this.form.username}),
            // }).then(response => {
            //     this.accountAddress = response.data.key
            // })
                
               
            }
            else{
                Toastify({
                    text: 'Account with same username Exists! ',
                    backgroundColor: 'orange',
                    gravity: 'top',
                    position: 'right'
                }).showToast();
            }
    
              
        } 
        },
        // async createAccount() {
        //     try {
        //         const response = await fetch('http://127.0.0.1:8000/create_account/', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/x-www-form-urlencoded'
        //         },
        //         body: JSON.stringify({
        //             'password': this.password
        //         })
        //         });
        //         const data = await response.json();
        //         if (response.ok) {
        //         this.accountAddress = data.address;
        //         this.errorMessage = null;
        //         } else {
        //         this.accountAddress = null;
        //         this.errorMessage = "Failed to create account";
        //         }
        //     } catch (error) {
        //         console.error(error);
        //         this.accountAddress = null;
        //         this.errorMessage = "An error occurred while creating the account";
        //     }
        // },

    }

}

</script>