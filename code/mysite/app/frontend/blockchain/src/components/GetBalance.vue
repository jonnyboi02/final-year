<template>
    
    <div style="color: white;   color: white;
   background: rgba(0,0,0,.6);
    box-sizing: border-box;
    box-shadow: 0 15px 10px rgba(0,0,0,.6);
    border-radius: 10px;
    padding: 10px;
    margin-top: -70px;
    height: 1150px;">
      <!-- <h2>Details</h2> -->
      <BalanceComponent />
      <!-- <input v-model="account" type="text" placeholder="Enter account address" /><br>
      <div style="padding-top: 10px;">
      <button @click="getBalance">Get balance</button>
      </div>
      <p v-if="balance !== null">Balance: {{ balance }} ETH</p> -->
      <div class="evaluate" style="margin-top: -30px;">
        <!-- <h2>Evaluate NFT</h2> -->
        <FundsComponent style="padding-top: 100px;"/>

      </div>
      <div > 
        <!-- <h2>Requested Loans</h2> -->
        <UserLoanRequests style="width: 1145px; margin-left:20px; "/>
      </div>
      
      
    </div>
  </template>
  
  <script>
import BalanceComponent from './BalanceComponent.vue';
import UserLoanRequests from './UserLoanRequests.vue';
import FundsComponent from './FundsComponent.vue';

  export default {
    async mounted() {
        await this.getAddress();
        await this.getBalance();
    },
    data() {
        return {
            account: this.getAddress() ? this.getAddress() : "0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264",
            balance: null,
        };
    },
    methods: {
        async getAddress() {
            const response = await fetch("http://127.0.0.1:8000/get_address/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "username": localStorage.getItem("username"),
                }),
            }).then(response => response.json())
                .then(data => {
                if (data.error) {
                    console.log(error);
                }
                else {
                    this.account = data.key;
                    this.senderPassword = localStorage.getItem("password");
                }
            });
        },
        async getBalance() {
            // Make a GET request to the Django view URL with the account parameter
            fetch(`http://localhost:8000/eth_balance/${this.account}/`)
                .then(response => response.json())
                .then(data => {
                if (data.error) {
                    console.error(data.error);
                }
                else {
                    this.balance = data.balance;
                }
            })
                .catch(error => console.error(error));
        },
    },
    components: { BalanceComponent, UserLoanRequests, FundsComponent }
};
  </script>
  

  <style>
  .evaluate{
    /* border-color: white; */
    /* border-style: solid; */
    border-radius: 10px;
    border-width: thin;
    margin-left: 15px;
    margin-right: 15px
    

  }
  </style>