<template>
  <div class="container">
    <img src="./assets/Logo2.png.png" style="transform: translate(-160%, -30%);">
    <nav class="navbar navbar-expand-md navbar-dark bg-primary" style="transform: translate(0%, -320%);" >
      <div class="collapse navbar-collapse" id="navbarCollapse" >
        <ul class="navbar-nav mr-auto flex-row">
          <!-- <li class="nav-item">
            <img src="./assets/Logo2.png.png" style="width: 200px">
          </li> -->
          <li class="nav-item">
            <router-link to="/transaction" class="nav-link">Transaction</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/register" class="nav-link">Registration</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/login2" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/eth_balance" class="nav-link">Balance, Requests and Assets</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/logout" class="nav-link">Log Out</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/deploy_contract" class="nav-link">Request Loan</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/contracts" class="nav-link">Contracts</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/loan_requests" class="nav-link">Loan Requests</router-link>
          </li>
          <!-- <li class="nav-item">
            <router-link to="/assets" class="nav-link">Requests and Assets</router-link>
          </li> -->
        </ul>
      </div>
    </nav>
    <router-view></router-view>

  </div>
  <div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Register from './components/Register.vue'
import Loan from './components/Loan.vue'
import GetAccounts from './components/GetAccounts.vue'
import CreateAccount from './components/CreateAccount.vue'
import SendWei from './components/SendWei.vue'
import RequestLoan from './components/RequestLoan.vue'
import Login2 from './components/Login2.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Register,
    Loan,
    GetAccounts,
    CreateAccount,
    SendWei,
    RequestLoan,
  },
}
</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Anton&family=Delicious+Handrawn&family=Roboto+Condensed:wght@300&display=swap');

#text{
  margin-left: 500px;
  margin-right: 500px;
}

.container{
  margin-bottom: 1000px;
  font-family: 'Roboto Condensed';

}
.container h3{
  font-family: "Anton";
}

#navbarCollapse{
  border-style: solid;
  padding-left: 55px;
  padding-right: 55px;
  border-color: transparent;
  border-radius: 10px;
 background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  

  /* position: fixed; */
  /* z-index: 9999999999999999999999999999999999; */

}

#navbarCollapse .navbar-nav .navitem:hover{
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              /* 0 0 50px #f4e403,
              0 0 100px #d5cf1e; */
}

body {
  /* background-color: #007bff; */
  /* background: rgb(2,0,36);
background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 42%, rgba(0,212,255,1) 100%); */
background: rgb(0,0,0);
background: linear-gradient(90deg, rgba(0,0,0,1) 5%, rgba(48,48,48,0.989233193277311) 49%, rgba(119,110,110,1) 100%);
}

.navbar {
  /* background-color: #007bff; */
}
text{
  color: #000000
}


.nav-link {
  text-align: center;
  color: #fff !important;
  font-size: 1.2rem;
}

li{
  color: rgb(255, 255, 255);
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  /* background-color: rgb(52, 80, 181); */
}

li {
  float: left;
  margin-right: 10px;
  color: #ffffff;
 
  
}
li:hover {
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              /* 0 0 50px #f4e403,
              0 0 100px #d5cf1e; */
}

li router-link {
  display: block;
  padding: 18px;
  border: 50;
  background-color: #dddddd;
  size: 35px;
}

::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1; 
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}


</style>
