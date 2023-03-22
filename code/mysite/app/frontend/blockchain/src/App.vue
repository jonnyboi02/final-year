<template>
  <div class="container">
    <nav class="navbar navbar-expand-md navbar-dark bg-primary">
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link to="/transaction" class="nav-link">Transaction</router-link>
          </li>
          <!-- <li class="nav-item">
            <router-link to="/create_account" class="nav-link">Create Account</router-link>
          </li> -->
          <li class="nav-item">
            <router-link to="/register" class="nav-link">Registration</router-link>
          </li>
          <!-- <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li> -->
          <li class="nav-item">
            <router-link to="/login2" class="nav-link">Login2</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/eth_balance" class="nav-link">Balance</router-link>
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
        </ul>
      </div>
    </nav>
    <router-view></router-view>
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
body {
  background-color: #fff;
}

.navbar {
  background-color: #007bff;
}

.nav-link {
  color: #fff !important;
}
</style>
