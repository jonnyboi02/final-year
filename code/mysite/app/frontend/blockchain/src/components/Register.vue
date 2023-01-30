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
            //     Toastify({
            //     text: "Successful registration",
            //     className: "info",
            //     style: {
            //       background: "linear-gradient(to right, #00b09b, #96c93d)",
            //     }
            //   }).showToast();

            }
            response = fetch("http://127.0.0.1:8000/register/", {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form),
            }).then(()=>   
                Toastify({
                text: "Successful registration",
                className: "info",
                style: {
                  background: "linear-gradient(to right, #00b09b, #96c93d)",
                }
              }).showToast())

         

            if (response.status === 400){
                alert("User already exists!")
            } 
            else{
                alert("Account created")
            }
        
        },

    }

}

</script>