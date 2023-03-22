<template>
  <div>
    <h2>List of Smart Contracts</h2>
    <select v-model="currentChoice">
      <option v-for="choice in choices" :key="choice" :value="choice" >
        {{ choice }}
      </option>
    </select>
    <div v-if=false>

    </div>
    
    <!-- <button @click="getContract">Get List</button> -->
    <!-- <ul>
      <li v-for="address in contractAddresses" :key="address">{{ address }}</li>
    </ul> -->
    <div v-else>
    <div>
    <select v-if="contractAddresses && contractAddresses.length > 0" v-model="selectedAddress">
      <option v-for="address in contractAddresses" :key="address" :value="address">
        {{ address }}
      </option>
    </select>
  </div>
  <button @click="getLoanDetails">Get Contract Details</button> 
  <div>
    <p v-if="loanDetails">
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
  </div>
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
      loanDetails: null,
      choices: ['For Sale', 'Owned', 'Loaned'],
      currentChoice: 'For Sale',
      
    };
  },

  async mounted(){
    await this.getContract();
    this.selectedAddress = this.contractAddresses[0]

  },

  methods: {
    async getContract() {
      try {
        const response = await fetch('http://127.0.0.1:8000/contracts/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data); // Log the response data to the console for debugging
        this.contractAddresses = data;
      } catch (error) {
        console.error(error); // Log any errors to the console
      }
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
