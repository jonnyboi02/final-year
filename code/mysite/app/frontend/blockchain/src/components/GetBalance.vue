<template>
    <div style="color: white;">
      <h3>Get Ethereum balance</h3>
      <input v-model="account" type="text" placeholder="Enter account address" /><br>
      <div style="padding-top: 10px;">
      <button @click="getBalance">Get balance</button>
      </div>
      <p v-if="balance !== null">Balance: {{ balance }} ETH</p>
    </div>
  </template>
  
  <script>
  export default {
    async mounted(){
      getAddress();
    },

    data() {
      return {
        account:this.getAddress() ? this.getAddress() :  '0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264',
        
        balance: null,
      };
    },
    methods: {
      async getAddress(){
            const response = fetch("http://127.0.0.1:8000/get_address/", {
                method: "POST", 
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': localStorage.getItem('username'), 
                }),
                
            }).then(response => response.json())
            .then(data=>{
                if (data.error){
                    console.log(error)
                }
                else{
                    this.account = data.key
                    this.senderPassword = localStorage.getItem('password')
                }
            })
            
            
            
        },



      getBalance() {
        // Make a GET request to the Django view URL with the account parameter
        fetch(`http://localhost:8000/eth_balance/${this.account}/`)
          .then(response => response.json())
          .then(data => {
            if (data.error) {
              console.error(data.error);
            } else {
              this.balance = data.balance;
            }
          })
          .catch(error => console.error(error));
      },
    },
  };
  </script>
  