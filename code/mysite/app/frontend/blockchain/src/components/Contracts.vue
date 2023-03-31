<template>
  <div id="header">
    <h2><span style="font-weight: bold;">Welcome</span> {{ username}}</h2>
  </div>

  <div id="funds">
    <p> You currently have: {{ balance }} ETH. </p>
  </div>

<div class="grid-container-element">
    <div class="grid-child-element purple" >
        <h3 style="color: white;">List of Smart Contracts</h3>
        <!-- <select v-model="currentChoice" style="padding-left: 145px;padding-right: 145px;">
              <option v-for="choice in choices" :key="choice" :value="choice" style="">
                {{ choice }}
              </option>
        </select> -->

      <div  v-if=true>
          <nav id="lists" style="margin-left: 0px; color: white; padding-top: 20px;">
            <ul v-if="contractAddresses && contractAddresses.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in contractAddresses" :key="address" :value="address" @click="selectItem(index)" style="padding: 2px; border-style: solid; border-radius: 20px; align: center; padding-left: 20px; padding-right: 15px; ">
                  {{  address }}
                </li>
              </div>
            </ul>
           
          </nav>
          <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractAddresses[selectedItem] }}</p>
          <p v-else class='message'>Select a smart contract address</p>
          <button @click="getLoanDetails">Get Contract Details</button> 


      </div>

    </div>
    <div class="grid-child-element green">
      <p v-if="loanDetails" style="color: white;">
              Borrower: {{ loanDetails.borrower }}<br>
              Lender: {{ loanDetails.lender }}<br>
              Owner: {{ loanDetails.owner }}<br>
              Amount: {{ loanDetails.amount }}<br>
              Rate: {{ loanDetails.rate }}<br>
              Duration: {{ loanDetails.duration }}<br>
              Due Date: {{ loanDetails.dueDate }}<br>
              Is Repaid: {{ loanDetails.isRepaid }}<br>
              Collateral Amount: {{ loanDetails.collateralAmount }}<br>
              Collateral Holder: {{ loanDetails.collateralHolder }}<br>
              Collateral URL : {{loanDetails.collateralUrl }} <br>
              Contract Price : {{loanDetails.price  }}<br>
            </p>
    </div>

    <div class="grid-child-element purple" style="color: white;">
      <h3>Loaned Contracts </h3>
        <nav id="list" style="margin-left: 0px; color: white; padding-top: 20px;">
            <ul v-if="loanedContracts && loanedContracts.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in loanedContracts" :key="address" :value="address" @click="selectLoanItem(index)" style="padding: 2px; border-style: solid; border-radius: 20px; align: center; padding-left: 20px; padding-right: 15px; ">
                  {{  address }}
                </li>
              </div>
            </ul>
            <ul v-else>
              <li style="padding-left: 100px; padding-right: 100px; border-style: solid; border-radius: 25px;">No contracts For Sale</li>
            </ul>
           
          </nav>
          <!-- {{ loanedContracts }} -->
                    <!-- <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractsForSale[selectedItem] }}</p> -->
          <!-- <p v-else class='message'>Select a smart contract address</p> -->
          
          <button @click="getLoanDetails" class = 'btn'>Get Contract Details</button> 
          <button class = 'btn'>Repay Loan</button>
          
          
         

      

    </div>
    <div class="grid-child-element green" style="color: white;">
      
      <h3> Contracts for Sale</h3>
          <nav id="list" style="margin-left: 0px; color: white; padding-top: 20px;">
            <ul v-if="contractsForSale && contractsForSale.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in contractsForSale" :key="address" :value="address" @click="selectBuyItem(index)" style="padding: 2px; border-style: solid; border-radius: 20px; align: center; padding-left: 20px; padding-right: 15px; ">
                  {{  address }}
                </li>
              </div>
            </ul>
            <ul v-else>
              <li style="padding-left: 100px; padding-right: 100px; border-style: solid; border-radius: 25px;">No contracts For Sale</li>
            </ul>
           
          </nav>
          
          <!-- <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractsForSale[selectedItem] }}</p> -->
          <!-- <p v-else class='message'>Select a smart contract address</p> -->
          {{ selectedAddressBuy }}
          {{ loanContractInstance }}
          <button @click="getLoanDetails"  class = 'btn'>Get Contract Details</button> 
          <button class = 'btn' @click="buyContract" > Purchase contract</button>
          
      </div>
      

    {{ test }}
</div>

</template>

<script>
import Web3 from 'web3';
import Toastify from 'toastify-js';
import 'toastify-js/src/toastify.css';
import LoanABI from './contracts/LoanABI.json'
export default {
  data() {
    return {
      contractAddresses: null,
      selectedAddress: null,
      selectedAddressLoan: null,
      selectedAddressBuy: null,
      loanDetails: null,
      choices: ['Sale', 'Owned', 'Loaned'],
      currentChoice: 'For Sale',
      selectedItem: null,
      contractsForSale: null,   
      loanedContracts: null, 
      account: null,
      test: "ok",
      username: "",
      accountInstance: null,
      loanContractInstance: null,
    };
  },

  async mounted(){
    await this.getAddress();
    await this.getContract();
    await this.getSaleContracts();
    await this.getLoanedContracts();
    await this.getAccountInstance();
    await this.getBalance();
    this.selectedAddress = this.contractAddresses[0]
  },

  methods: {
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


      //to fix

      async buyContract(){
        const web3 = new Web3('http://localhost:8547');
            const accounts = await web3.eth.getAccounts();
        this.loanContractInstance = new web3.eth.Contract(
            LoanABI, 
            this.selectedAddressBuy,
          ) 

          try {
            const accounts = await web3.eth.getAccounts();
          await this.loanContractInstance.methods.changeOwner(this.accountInstance).send({
            from: accounts[0],
            gas: 3000000,
          });
          Toastify({
            text: `Owner Changed to` + this.accountInstance,
            backgroundColor: 'green',
            position: 'center',
          }).showToast();
        } catch (error) {
          Toastify({
            text: 'Error Occurred when changing owner',
            backgroundColor: 'red',
            position: 'center',
          }).showToast();
        }
        await this.getLoanDetails()
      },



    async getAccountInstance(){
      const web3 = new Web3('http://localhost:8547');
      const accounts = await web3.eth.getAccounts();
      for(let i = 0 ; i<accounts.length; i++){
        let curAccount = accounts[i]
        if (JSON.stringify(curAccount.toLowerCase()) === JSON.stringify(this.account.toLowerCase())){
          this.accountInstance = curAccount
          break;
        }
      }
      //       Toastify({
      //       text: "The contract has not been deployed yet" + this.accountInstance,
      //       backgroundColor: 'orange',
      //       position: 'center',
      // }).showToast()
      
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
                    this.account = data.key
                    this.username = localStorage.getItem('username')
                }
            })
          },
    selectItem(index) {
      this.selectedItem = index;
      this.selectedAddress = this.contractAddresses[index]
    },
    selectLoanItem(index) {
      //this.selectedItem = index;
      this.selectedAddress = this.loanedContracts[index]
      this.selectedAddressLoan = this.loanedContracts[index]
    },
    selectBuyItem(index){
      this.selectedAddress = this.contractsForSale[index]
      this.selectedAddressBuy = this.contractsForSale[index]
      // Toastify({
      //       text: "The contract has not been deployed yet",
      //       backgroundColor: 'orange',
      //       position: 'center',
      // }).showToast()
    },

    async getContract() {
      try {
        const response = await fetch('http://127.0.0.1:8000/contracts/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data); // Log the response data to the console for debugging
        this.contractAddresses = data;
        let set = new Set()
        for(let i = 0; i< this.contractAddresses.length; i++){
          set.add(this.contractAddresses[i])
        }
        this.contractAddresses = Array.from(set)
      } catch (error) {
        console.error(error); // Log any errors to the console
      }
    },
    async getSaleContracts(){
      const web3 = new Web3('http://localhost:8547');
      const accounts = await web3.eth.getAccounts();
      let arr = []
      
      for (let i = 0; i< this.contractAddresses.length; i++){
        let address = this.contractAddresses[i]
        try{
            const LoanContract = new web3.eth.Contract(
              LoanABI,
              address,
            );
            let collateralHolder = this.account;
            const result = await LoanContract.methods.getLoanDetails().call();

            if (JSON.stringify(result[9].toLowerCase()) !== JSON.stringify(collateralHolder.toLowerCase())){
              arr.push(address)
            }
        }catch(error){
          continue;
        }
      }
      this.test = arr.length
      this.contractsForSale=arr;

    },

    async getLoanedContracts(){
      const web3 = new Web3('http://localhost:8547');
      const accounts = await web3.eth.getAccounts();
      let arr = []
     
      for (let i = 0; i< this.contractAddresses.length; i++){
        let address = this.contractAddresses[i];
        try{
            const LoanContract = new web3.eth.Contract(
            LoanABI,
            address,
          );
          let collateralHolder = this.account;
          const result = await LoanContract.methods.getLoanDetails().call();
          // this.test = result[9]
          // this.test = result[9].length + ", "+collateralHolder.length
          if (JSON.stringify(result[9].toLowerCase()) === JSON.stringify(collateralHolder.toLowerCase())){
            // this.test = result[9]
            arr.push(address)
          }
        }catch(error){
          continue;
        }
        

      }
      //this.test = arr.length
      this.loanedContracts=arr;
      

    },
    async getLoanDetails(){
        try{
          const web3 = new Web3('http://localhost:8547');
          const accounts = await web3.eth.getAccounts();
        // const web3 = new Web3('http://localhost:8545');
        const LoanContract = new web3.eth.Contract(
          LoanABI,
          this.selectedAddress,
        );
          const result = await LoanContract.methods.getLoanDetails().call();
          this.loanDetails = {
            borrower: result[0],
            lender: result[1],
            owner: result[2],
            amount: result[3],
            rate: result[4],
            duration: result[5],
            dueDate: result[6],
            isRepaid: result[7],
            collateralAmount: result[8],
            collateralHolder: result[9],
            collateralUrl: result[10],
            price: result[11],
          };
        }catch (error){
          Toastify({
            text: "The contract has not been deployed yet",
            backgroundColor: 'orange',
            position: 'center',
          })
        }

      },

  },
};
</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Arimo&display=swap');
/* 
#information{
  border-style: solid;
  border-color: white;
  width: 800px;
  height: 300px;
  margin-left: 50px;

} */
#funds{
  color: white;
  border-style: solid;
  border-radius: 25px ;
  margin-left: 15px;
  margin-right: 15px;
}


#header{
  font-family: 'Arimo';
  font-size: 20px;
  color: white;
}

.btn{
  margin-right: 10px;
}

#lists{
  height:200px;
  width:101%;
  overflow:hidden; 
  overflow-y:scroll;
  color: white;

}

#list{
  height:100px;
  width:101%;
  overflow:hidden; 
  overflow-y:scroll;
  color: white;
}

#noinfo{
  border-style: solid;
  border-color: white;
  border-radius: 25px;
}

.grid-container-element { 
    display: grid; 
    grid-template-columns: 1fr 1fr; 
    grid-gap: 5px; 
    /* border: 1px solid black;  */
    width: 50%; 
  
    padding-top: 10px;
    width: 1920/2;
} 
.grid-child-element { 
    padding: 10px;
    margin-left: 30px;
    margin-right: 30px;
    margin: 10px; 
    border: 1px solid rgb(255, 255, 255); 
    border-radius: 25px;
    width: 375px
}
.message{
 color: white;
}
</style>