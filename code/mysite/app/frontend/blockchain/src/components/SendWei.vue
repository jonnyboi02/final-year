<template>
  <GetAccounts/>
  <h3>Send Ether</h3>
  <div>
    <form @submit.prevent="sendTransaction">
      <label for="sender_address">Sender Address</label>
      <input type="text" id="sender_address" v-model="senderAddress">
      <br>
      <label for="sender_password">Sender Password</label>
      <input type="password" id="sender_password" v-model="senderPassword">
      <br>
      <label for="recipient_address">Recipient Address</label>
      <input type="text" id="recipient_address" v-model="recipientAddress">
      <br>
      <label for="value">Value (in wei)</label>
      <input type="text" id="value" v-model="value">
      <br>
      <!-- <br>
      <label for="gas">Gas Limit</label>
      <input type="text" id="gas" v-model="gas">
      <br>
      <label for="gas_price">Gas Price (in wei)</label>
      <input type="text" id="gas_price" v-model="gasPrice">
      <br> -->
      <button type="submit">Send Transaction</button>
      
    </form>
    <button @click="getAddress">Test</button>
  </div>
</template>

<script>
import Toastify from 'toastify-js';
import GetAccounts from './GetAccounts.vue';

export default {
    data() {
        return {
            senderAddress: "0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264",
            senderPassword: "123456789",
            recipientAddress: "0xc63AB01569680E6388A7B4EbbdBaf260be9870dc",
            value: "0x20000000000000000000",
            // gas: '',
            // gasPrice: ''
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
                    this.senderAddress = data.key
                    this.senderPassword = localStorage.getItem('password')
                }
            })
            
            
        },
        sendTransaction() {
            const data = {
                sender_address: this.senderAddress,
                sender_password: this.senderPassword,
                recipient_address: this.recipientAddress,
                value: this.value,
            };
            fetch("http://127.0.0.1:8000/send_transaction/", {
                method: "POST",
                body: new URLSearchParams(data)
            })
                .then(response => response.json())
                .then(response => {
                console.log(response);
                Toastify({
                    text: "Transaction sent successfully!",
                    duration: 3000,
                    close: true,
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                    stopOnFocus: true
                }).showToast();
            })
                .catch(error => {
                console.error(error);
            });
        }
    },
    components: { GetAccounts }
};
</script>
