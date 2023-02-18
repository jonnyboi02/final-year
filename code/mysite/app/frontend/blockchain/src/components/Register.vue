<template>
    Hi {{form['username'] }}

    <div>
        <form ref="form">
            <div>
            Username:<input class = 'form-control' v-model='form["username"]' />
            </div> 
            <div>
            Password:<input class = 'form-control' type = 'password' v-model='form["password"]'/>
            </div>
            <button @click="registerUser">Register</button>
            {{message}}

        </form>
    </div>
    
    

</template>

<script>

import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"

export default{
    data(){
        return{
            message: "",
            form:{
                username : "",
                password : "",
            },

        }
    },
    methods :{
        async registerUser(){
            if (form['username'] === ""){
                message = "Username cannot be empty!";
                alert("Username cannot be empty!");
            }
            response = fetch("http://127.0.0.1:8000/register/", {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form),
            }).then(response => {
                if (response.status === 200){
                    Toastify({
                    text: "Successful registration",
                    className: "info",
                    style: {
                    background: "linear-gradient(to right, #00b09b, #96c93d)",
                    }
                }).showToast()

                }
            })    
        
        
        },
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
                } else {
                this.accountAddress = null;
                this.errorMessage = "Failed to create account";
                }
            } catch (error) {
                console.error(error);
                this.accountAddress = null;
                this.errorMessage = "An error occurred while creating the account";
            }
        },

    }

}

</script>