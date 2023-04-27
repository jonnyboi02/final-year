<template>
    <div style="color: white;">
    <!-- <h3>Hi {{form['username'] }}</h3> -->

    <div class="login-box">
        <!-- <form ref="form"> -->
            <h2>Register</h2>
            <form>
            <div class="user-box" >
                <input id = 'username' type="text" name="" required="" v-model='form["username"]'>
                <label>Username</label>
            </div>
            <div class="user-box">
                <input id = 'password' type="password" name="" required="" v-model='form["password"]' >
                <label>Password</label>
        </div>
            <!-- Username: <br>
            <input class = 'user-box' v-model='form["username"]' /><br>
            
            Password: <br>
            <input class = 'user-box' type = 'password' v-model='form["password"]'/> <br>
            <br> -->
            <a  type="submit" @click="registerUser">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Register
            </a>
                <!-- <button @click="registerUser">Register</button> -->
            </form>
           
            
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
            this.form.username = document.getElementById('username').value
            this.form.password = document.getElementById('password').value

            if (this.form.username === ""){
               // this.message = "Username cannot be empty!";
                //alert("Username cannot be empty!");
                Toastify({
                    text: 'Username cannot be empty!',
                    backgroundColor: 'red',
                    gravity: 'top',
                    position: 'right'
                }).showToast();
                return;
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

<style>
.login-box {
  position: absolute;
  top: 40%;
  left: 50%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
 background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;

}

.login-box h2 {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
}

.login-box .user-box {
  position: relative;
}

.login-box .user-box input {
  width: 100%;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 30px;
  border: none;
  border-bottom: 1px solid #fff;
  outline: none;
  background: transparent;
}

.login-box .user-box label {
  position: absolute;
  top:0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.login-box .user-box input:focus ~ label,
.login-box .user-box input:valid ~ label {
  top: -24px;
  left: 0;
  color: #f68e44;
  font-size: 12px;
}

.login-box form a {
  position: relative;
  display: inline-block;
  padding: 10px 10px;
  color: #b79726;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px
}

.login-box a:hover {
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              0 0 50px #f4e403,
              0 0 100px #d5cf1e;
}

.login-box a span {
  position: absolute;
  display: block;
}

.login-box a span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f4c003);
  animation: btn-anim1 1s linear infinite;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%,100% {
    left: 100%;
  }
}

.login-box a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #f4bc03);
  animation: btn-anim2 1s linear infinite;
  animation-delay: .25s
}

@keyframes btn-anim2 {
  0% {
    top: -100%;
  }
  50%,100% {
    top: 100%;
  }
}

.login-box a span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #f4dc03);
  animation: btn-anim3 1s linear infinite;
  animation-delay: .5s
}

@keyframes btn-anim3 {
  0% {
    right: -100%;
  }
  50%,100% {
    right: 100%;
  }
}

.login-box a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #f4b003);
  animation: btn-anim4 1s linear infinite;
  animation-delay: .75s
}

@keyframes btn-anim4 {
  0% {
    bottom: -100%;
  }
  50%,100% {
    bottom: 100%;
  }
}


</style>