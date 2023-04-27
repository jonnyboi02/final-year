<template >
<div style="color: white;  background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px; padding: 10px; margin-top: -70px;">
  <!-- <GetAccounts /> -->

  <h2 style="color: white;">Send Ether</h2>
  <BalanceComponent/>
  <!-- <div id="funds">
    <p> You currently have: {{ balance }} ETH. </p>
  </div> -->
  <div id = 'info'>
    Please make sure that you select the correct address to receive the Ethers as this operation is <span style="color: red;">IRRREVERSIBLE</span>
  </div>
  <div style="padding-top: 10px;">
    <form @submit.prevent="sendTransaction" >
      <!-- <label for="sender_address">Sender Address</label><br>
      <input type="text" id="sender_address" v-model="senderAddress">
      <br>
      <label for="sender_password">Sender Password</label><br>
      <input type="password" id="sender_password" v-model="senderPassword">
      <br> -->
      <!-- <label for="recipient_address">Recipient Address</label><br>
      <input type="text" id="recipient_address" v-model="recipientAddress">
      <br> -->
      <div style="padding-bottom: 10px;">
      <label for="value"  >Value (in Ethers):</label><br>
    </div>
      <input type="text" id="value" v-model="value">
      <br>
      <label>Recipient Address</label> <br>
      <select v-if="accounts && accounts.length > 0" v-model="recipientAddress">
      <option v-for="account in accounts" :key="account" :value="account">
        {{ account }}
      </option>
    </select>
      <!-- <br>
      <label for="gas">Gas Limit</label>
      <input type="text" id="gas" v-model="gas">
      <br>
      <label for="gas_price">Gas Price (in wei)</label>
      <input type="text" id="gas_price" v-model="gasPrice">
      <br> -->
      <div style="padding-top: 10px;">
        <!-- <a  type="submit" @click="sendTransaction">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Send Transaction
            </a> -->
      <button type="submit">Send Transaction</button>

      <!-- {{ output }} -->
    </div>
    </form>

    <!-- <button @click="getAddress">Test</button> -->
  </div>
</div>
</template>

<script>
import Toastify from 'toastify-js';
import GetAccounts from './GetAccounts.vue';
import Web3 from 'web3';
import BalanceComponent from './BalanceComponent.vue';
export default {

    async mounted(){
        await this.getAccounts();
        await this.getAddress();
        await this.getBalance();
        //this.recipientAddress = accounts[0]
    },
    data() {
        return {
            senderAddress: localStorage.getItem('username') ? localStorage.getItem('username') : "0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264",
            senderPassword: "123456789",
            recipientAddress: "0xc63AB01569680E6388A7B4EbbdBaf260be9870dc",
            value: "",
            accounts: [],
            selectedAccount: null,
            output: "hey",
            balance: null,
            // gas: '',
            // gasPrice: ''
        };
    },
    methods: {
      getBalance() {
        // Make a GET request to the Django view URL with the account parameter
        fetch(`http://localhost:8000/eth_balance/${this.senderAddress}/`)
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
      
        

        
        async getAccounts() {
        const url = 'http://localhost:8000/get_accounts/'
        fetch(url)
          .then(response => response.json())
          .then(data => {
            this.accounts = data.accounts
            this.recipientAddress = this.accounts[0]
          })
          .catch(error => {
            console.error(error)
          })
      },
    
        

        
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
          //checking the data to make sure it is good
          if (this.value===""){
            Toastify({
                      text: "Value cannot be empty!",
                      duration: 3000,
                      close: true,
                      backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                      stopOnFocus: true
                  }).showToast();
                  return;
          }
          const check = /^[0-9.]+$/;
          var num = null
          if (check.test(this.value)){
            try{
              const weiAmount = Web3.utils.toWei(this.value.toString(), 'ether')/10**3;
              const weiAmountWithPrefix = '0x' + weiAmount;
              this.value = weiAmountWithPrefix

            }catch{
              Toastify({
                      text: "Value must be decimals!",
                      duration: 3000,
                      close: true,
                      backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                      stopOnFocus: true
                  }).showToast();
                  return;
            }
          }
   
          
         

          const regex2 = /^0x[0-9a-fA-F]+$/;
          this.output=this.value

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
                .then(data => {
                console.log(data);
                this.output =data;
                if (data.transaction==null){
                  Toastify({
                      text: "Insuffient funds",
                      duration: 3000,
                      close: true,
                      backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                      stopOnFocus: true
                  }).showToast();

                }
                else{
                  Toastify({
                      text: "Transaction sent successfully!",
                      duration: 3000,
                      close: true,
                      backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                      stopOnFocus: true
                  }).showToast();
              }
            })
                .catch(error => {
                console.error(error);
            });
        },
        
    },

     components: { GetAccounts, BalanceComponent }
};
</script>


<style>
#funds{
  margin-bottom: 10px;
  padding-right: 10px;
  padding-left: 10px;
}
#info{
    border-style: solid;
    border-color: white;
    border-radius: 10px;
    padding: 10px;
    border-width: thin;
    

}
form a {
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

a:hover {
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              0 0 50px #f4e403,
              /* 0 0 100px #d5cf1e; */
}

a span {
  position: absolute;
  display: block;
}

a span:nth-child(1) {
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

a span:nth-child(2) {
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

a span:nth-child(3) {
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

a span:nth-child(4) {
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