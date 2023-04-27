<template>



<div class="contractinfo" >
    <h2><span style="color: white">Welcome {{ username}}</span> </h2>

  <BalanceComponent ref="funds" :key="componentKey" />
  <!-- <div id="funds">
    <p> You currently have: {{ balance }} ETH. </p>
  </div> -->
<div style = 'margin-top: 50px;position: absolute; right: 23%;  background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  '>
<div class="grid-container-element">
    <div class="grid-child-element purple" >
        <h3 style="color: white;">List of Owned Contracts</h3>
        <!-- <select v-model="currentChoice" style="padding-left: 145px;padding-right: 145px;">
              <option v-for="choice in choices" :key="choice" :value="choice" style="">
                {{ choice }}
              </option>
        </select> -->

      <div  v-if="ownedContracts && ownedContracts.length>0">
          <nav id="lists" style="margin-left: 0px; color: white; padding-top: 10px;">
            <ul v-if="ownedContracts && contractAddresses.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in ownedContracts" :key="address" :value="address" @click="selectItem(index)" style="padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; width: 425px; ">
                  {{  address }}
                </li>
              </div>
            </ul>
           
          </nav>
          <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractAddresses[selectedItem] }}</p>
          <p v-else class='message'>Select a smart contract address</p>
          <button @click="getLoanDetails">Get Contract Details</button> 


      </div>
      <div v-else>
        <ul style="margin-left: 10px; color: white; padding-top: 10px;">
            <li style="padding-left: 100px; padding-right: 100px; border-style: solid; border-radius: 10px; width: 240px;">No contracts Owned</li>
        </ul>

      </div>

    </div>
    <div class="grid-child-element green" >
      <div v-if="loanDetails">
      <p v-if = 'dayToPay' style="border-style: solid; border-radius: 10px; border-color: white; border-width: thin; color: white">The loan is due to be paid: {{ dayToPay }}</p>
      <p v-if="loanDetails" style="color: white;">
              <!-- Borrower: {{ loanDetails.borrower }}<br> -->
              Lender: <span class="address">{{ loanDetails.lender }}</span><br>
              Lendee: <span class="address">{{ loanDetails.collateralHolder }}</span><br>
              Owner: <span class="address">{{ loanDetails.owner }}</span><br>
              Amount: {{ loanDetails.amount }}<br>
              Rate: {{ loanDetails.rate }}<br>
              Duration: {{ loanDetails.duration }}<br>
              Due Date: {{ loanDetails.dueDate }}<br>
              Is Repaid: {{ loanDetails.isRepaid }}<br>
              Collateral Amount: {{ loanDetails.collateralAmount }}<br>
              Amount Received: {{ loanDetails.amountreceived }} <br>
             
              <!-- Collateral URL : {{loanDetails.collateralUrl }} <br> -->
              <!-- Contract Price : {{loanDetails.price  }}<br> -->
            </p>
            <div v-if = 'loanDetails'  style="border-style: solid; border-radius: 15px; border-color: white; border-width: thin;">
                <p v-if = 'loanDetails'><span style="color: white; text-decoration: underline; ">Contract Price: {{ loanDetails.price  }} ETH</span></p>
              <p><span style="color: white; text-decoration: underline; ">NFT Original Owner: {{ originalnftOwner }}</span></p>
              <p><span style="color: white; text-decoration: underline; ">NFT Current Owner: {{ nftOwner }}</span></p>

            </div>
           
          </div>
          <br>
          <button @click="getNFT" v-if="loanDetails">View NFT</button>
          <!-- <v-alert
            :value="alert.show"
            :type="alert.type"
            :close-text="alert.dismissLabel"
            @input="alert.show = false"
            @click:close="onCloseAlert"
          >
            {{ alert.message }}
          </v-alert> -->
    </div>

    <div class="grid-child-element purple" style="color: white;">
      <h3>Loaned Contracts </h3>
        <nav id="list" style="margin-left: 0px; color: white; padding-top: 10px;">
            <ul v-if="loanedContracts && loanedContracts.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in loanedContracts" :key="address" :value="address" @click="selectLoanItem(index)" :class="{ 'selected': selectedAddress === address }" style="padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; width: 425px;">
                  <span v-if='contractStatus[index] == true' style="color: #b79726">{{ address }}</span>
                  <span v-else :class="{ 'selected': selectedAddress === address }">{{ address }}</span>
                </li>


              </div>
            </ul>
            <ul v-else>
              <li style=" padding-left: 100px; padding-right: 100px; border-style: solid; border-radius: 10px;">No contracts For Sale</li>
            </ul>
           
          </nav>
          <!-- {{ loanedContracts }} -->
                    <!-- <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractsForSale[selectedItem] }}</p> -->
          <!-- <p v-else class='message'>Select a smart contract address</p> -->
          <!-- <p v-if="selectedItem" class='message'>
            You have selected: {{ contractAddresses[selectedItem] }}
          </p> -->
          <br>
          <!-- <p v-else class='message'>Select a smart contract address</p> -->
          <button @click="getLoanDetails" class = 'btn'>Get Contract Details</button> 
          <button v-if='selectedAddress' @click ="showMessage"  class = 'btn'>Repay Loan</button>
          <transition name="fade">
          <div v-if="showOverlay " class="overlay">
            
            <div class="content">
              <h2>Repay Loan</h2>
              <BalanceComponent :key="componentKey" style="width: 400px;"/>
             
              <div style="border-style: solid; border-color: transparent; padding: 10px; border-width: thin; border-radius: 10px; padding-bottom: 0px;">
                <div style="padding-bottom: 30px;">
                There are {{ daysLeft }} days till repayment.
                <br>
                You need to pay {{ payRequired}} ETH.
                <!-- {{ repay.amount }} -->
                </div>
              <div class = 'user-box'>
                <input v-model="repay.amount">
                <label >Enter amount to pay:</label>
              </div>
              <button  @click="makeRepayment">Send Payment</button>
              <br>
              <br>
              
              <button @click="hideMessage" style="position: absolute; transform: translate(-510%, -1050%); background-color: transparent; color: white;; "> X </button>
            </div>
          </div>
          </div>
        </transition>
          
       
          
    </div>
    <div class="grid-child-element green" style="color: white;">
      
      <h3> Contracts for Sale</h3>
          <nav id="list" style="margin-left: 0px; color: white; padding-top: 10px;">
            <ul v-if="contractsForSale && contractsForSale.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(address, index) in contractsForSale" :key="address" :value="address" @click="selectBuyItem(index)" :class="{ 'selected': selectedAddress === address }" style="padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; width: 425px;">
                  {{  address }}
                 
                </li>
              </div>
            </ul>
            <ul v-else>
              <li style="width: 260px; padding-left: 100px; padding-right: 100px; border-style: solid; border-radius: 10px;">No contracts For Sale</li>
            </ul>
           
          </nav>
          
          <!-- <p v-if="selectedItem !== null" class='message'>You have selected: {{ contractsForSale[selectedItem] }}</p> -->
          <!-- <p v-else class='message'>Select a smart contract address</p> -->
          <!-- You have selected: {{ selectedAddressBuy }} -->
          <!-- {{ loanContractInstance }} -->
          <br>
          <button @click="getLoanDetails"  class = 'btn'>Get Contract Details</button> 
          <button class = 'btn' @click="showConfirmation(); "  > Purchase contract</button>
          <!-- buy contract -->
          <div class="overlay" v-if="isOverlayVisible">
            <div class="content" style="padding: 30px;">
              <h2>Are you sure you want to purchase this contract?</h2>
              <BalanceComponent :key="componentKey" style="width: 400px;"/>
              <br>
              <div style="border-style: solid; border-radius: 10px; border-width: thin;">
                <div>
                  The Contract Price is: {{ contractPrice }} ETH
                </div>
                <div v-if="canBuyContract">
                  <span style="color: greenyellow">You can afford this.</span>
                </div>
                <div v-else>
                  <span style="color: red">You cannot afford this.</span>
                </div>
              </div>
              <br>
              <button class="confirm-btn" @click="buyContract">Confirm</button>
              <button class="cancel-btn" @click="hideConfirmation" style="background-color: transparent; color:white; position: absolute; transform: translate(-630%, -750%);">X</button>
            </div>
          </div>
      </div>
      </div>
<!-- 
    {{ test }}
    {{ selectedItem}} -->
    {{ account }}
</div>
</div>
</template>

<script>
import Web3 from 'web3';
import Toastify from 'toastify-js';
import 'toastify-js/src/toastify.css';
import LoanABI from './contracts/LoanABI.json'
import BalanceComponent from './BalanceComponent.vue';
import nftABI from './contracts/MyNFT.json'
 
//function to calculate the price of a contract that user want to buy
function calculateBondPrice(loanAmount, durationDays, apr) {
  // Calculate the daily discount rate as a decimal
  const r = apr / 36500;

  // Calculate the sum of discounted cash flows
  let sumOfDiscountedCashflows = 0;
  for (let t = 1; t <= durationDays; t++) {
    const cashFlow = (t === durationDays) ? (loanAmount + (loanAmount * r * durationDays)) : (loanAmount / durationDays);
    sumOfDiscountedCashflows += cashFlow / Math.pow((1 + r), t/365);
  }

  // Calculate the interest earned on the bond
  const interest = (loanAmount * apr * durationDays) / 36500;

  // Calculate the bond price
  const price = (loanAmount / sumOfDiscountedCashflows) + interest;

  return price;
}

function calculateReducedLoanAmount(apr, loanAmount, remainingDays){
  const dailyInterestRate = (apr / 365) / 100;

  // Calculate the daily payment
  const dailyPayment = loanAmount * dailyInterestRate /
                        (1 - (1 / Math.pow(1 + dailyInterestRate, remainingDays)));

  // Calculate the remaining loan balance after the specified number of days
  const remainingBalance = loanAmount * Math.pow(1 + dailyInterestRate, remainingDays) -
                            (dailyPayment * (Math.pow(1 + dailyInterestRate, remainingDays) - 1) / dailyInterestRate);

  // Calculate the interest savings if the remaining balance is paid in full
  const interestSavings = remainingBalance * dailyInterestRate * remainingDays;

  // Return the reduced loan amount
  return loanAmount - interestSavings;
}

function calculateLateLoanAmount(apr, loanedAmount, daysLate) {
  const dailyInterestRate = apr / 365;
  const interestAccrued = loanedAmount * dailyInterestRate * daysLate;
  const totalLoanAmount = loanedAmount + interestAccrued;
  return totalLoanAmount;
}

//function to convert the unix time into normal date
const unixToDate = (unixTime) => {
  const date = new Date(unixTime * 1000);

  // use the Date object's built-in methods to extract the date components
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();

  // construct the date string using the extracted components
  const dateString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  return dateString;
}

function getDaysLeft(startDateUnix, endDateUnix) {
  // convert Unix timestamps to Date objects
  const startDate = new Date(startDateUnix * 1000);
  const endDate = new Date(endDateUnix * 1000);

  // calculate the difference in milliseconds between the two dates
  const diffMillis = endDate.getTime() - startDate.getTime();

  // calculate the number of days between the two dates and round down to the nearest integer
  const diffDays = Math.floor(diffMillis / (1000 * 60 * 60 * 24));

  // return the number of days left
  return diffDays;
}
function notifyRepaymentLeft(startDateUnix, endDateUnix){
  const startDate = new Date();
  const endDate = new Date(endDateUnix * 1000);
    // calculate the difference in milliseconds between the two dates
  const diffMillis = endDate.getTime() - startDate.getTime();

  // calculate the number of days between the two dates and round down to the nearest integer
  const diffDays = Math.floor(diffMillis / (1000 * 60 * 60 * 24));
  if (diffDays <= 3) {
    // show red toast notification for 3 days or less
    //toast.error(`Only ${diffDays} days left!`, { autoClose: false });
        Toastify({
            text: `Only ${diffDays} days left!`,
            backgroundColor: "red",
            position: "center",
        }).showToast();
  } else if (diffDays <= 7) {
    // show orange toast notification for 7 days or less
    Toastify({
            text: `Only ${diffDays} days left!`,
            backgroundColor: "orange",
            position: "center",
        }).showToast();
  }
  else{
    // Toastify({
    //         text: `${diffDays} days till Repayment!`,
    //         backgroundColor: "green",
    //         position: "center",
    //     }).showToast();

  }
  return diffDays;

}

export default {
  watch:{
    showOverlay(newValue) {
      if (newValue) {
        this.setLoanPayment();
      }
    },

    isOverlayVisible(newValue){
      if (newValue){
        this.contractSalePrice();
      }
    }
  },
    data() {
        return {
          isOverlayVisible: false,



          showOverlay: false,
          overlayInput: '',  



            balanceKey: 0,

            contractAddresses: null,
            selectedAddress: null,
            selectedAddressLoan: null,
            selectedAddressBuy: null,
            loanDetails: null,
            choices: ["Sale", "Owned", "Loaned"],
            currentChoice: "For Sale",
            selectedItem: null,
            contractsForSale: null,
            loanedContracts: null,
            ownedContracts: null,
            account: null,
            test: "ok",
            username: "",
            accountInstance: null,
            loanContractInstance: null,
            dayToPay: null,
            nftOwner: "",
            originalnftOwner: "",

            alert:{
              message: "",
              show: false,
              type: 'success',
              dismissLabel: 'Dismiss',
            },
            balance: 0,
            daysLeft: null,
            payRequired: null,

            repay : {
              amount: "",
            },
            shouldRender: true,
            componentKey: 0,
            contractStatus: [],

            contractPrice: null,
          
        };
    },
    async mounted() {
        await this.getAddress();
        await this.getBalance();
        await this.getContract(); 
        await this.getOwnedContracts();
        await this.getSaleContracts();
        await this.getLoanedContracts();
        await this.getAccountInstance();
        await this.getOwnedContracts();
        this.selectedAddress = this.contractAddresses[0];
        await this.getBalance();
    },
    methods: {
      //to rerender item
    //   toggleShouldRender() {
    //   this.shouldRender = !this.shouldRender
    // },
    canBuyContract(){
      let balance = this.balance;
      let price = this.contractPrice;
      return price<balance ? true : false
    },
    rerenderComponent() {
      this.componentKey += 1;
    },

    rerenderBalance(){
      this.balanceKey+=1;
    },
    // rerenderChild() {
    //   this.shouldRender = !this.shouldRender
    // },

    showConfirmation() {
      this.isOverlayVisible = true;
    },
    hideConfirmation() {
      this.isOverlayVisible = false;
    },



      errorMessage(){
        Toastify({
            text: `Select a Loan Contract`,
            backgroundColor: "green",
            position: "center",
        }).showToast();
      },

      showMessage() {
      this.showOverlay = true;
    },
    hideMessage() {
      this.showOverlay = false;
    },
    saveOverlayInput() {
      // Save overlay input to local state
      this.$data.overlayInput = this.overlayInput;
      this.hideMessage();
    },

    //calculate thhe price of the loan contract
    async contractSalePrice(){
      const web3 = new Web3("http://localhost:8547");
      const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddressBuy);
      const result = await LoanContract.methods.getLoanDetails().call(); 

      let duration = result[5]/86400;
      let apr = result[3]/100;
      let amount = result[2];
      let calculatedPrice = calculateBondPrice(amount, duration, apr)
      this.contractPrice = calculatedPrice;

    },
    //checks if the loan has been repaid yet
    async loanisPaid(){
      const web3 = new Web3("http://localhost:8547");
      const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddressLoan);
      const result = await LoanContract.methods.getLoanDetails().call(); 

      console.log(result[6])
      if (JSON.stringify(result[6]) === JSON.stringify(true)){
        console.log("Loan Repaid")
        Toastify({
          text: "Loan repaid",
          backgroundColor: "red",
          position: "center",
          duration: 3000,

        }).showToast();
        return true;
      } 
      return false;

    },

    //sets the pay required based on late or early repayments
    async setLoanPayment(){

      const web3 = new Web3("http://localhost:8547");
      const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddressLoan);
      const result = await LoanContract.methods.getLoanDetails().call();

      //checks if the loan has been repaid
      if (JSON.stringify(result[6]) === JSON.stringify(true)){
         this.showOverlay=false;
        console.log("Loan Repaid")
        Toastify({
          text: "Loan repaid",
          backgroundColor: "red",
          position: "center",
          duration: 3000,

        }).showToast();
      }
      
      
      let dueDate = result[5];
      let apr = result[3]/100;
      let loanedAmount = result[2];

      //calculates using unix time,
      const dueDateInMilliseconds = dueDate * 1000; // Convert Unix time to milliseconds
      const currentDate = new Date();
      const dueDateObject = new Date(dueDateInMilliseconds);
      const timeDifference = dueDateObject.getTime() - currentDate.getTime();
      const daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));

      this.daysLeft =daysDifference ;

      console.log(daysDifference);
      if (daysDifference>=0){
        this.payRequired = calculateReducedLoanAmount(apr, loanedAmount, daysDifference)
      }
      else{
        this.payRequired = calculateLateLoanAmount(apr, loanedAmount, Math.abs(daysDifference))
      }
      //this.payRequired = payRequired;
    },
    async makeRepayment(){
      const web3 = new Web3("http://localhost:8547");
      const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddressLoan);
      const result = await LoanContract.methods.getLoanDetails().call();

      let requiredPay = this.payRequired;
      let userInput = this.repay.amount;
      if (userInput<requiredPay){
        Toastify({
          text: "Enter the amount required",
          backgroundColor: "red",
          position: "center",
          duration: 3000,
          // gravity: "bottom",
          // offset: { y: 100 },
          // onClick: function() {
          //   window.open(NFTurl, "_blank");
          // }
        }).showToast();
      }
      else{
        //web3.eth.defaultAccount = this.accountInstance
        await web3.eth.personal.unlockAccount(this.accountInstance, localStorage.getItem("password"), 600);
        let amountInWei = web3.utils.toWei((userInput), "ether");
        LoanContract.methods.makeRepayment().send({
          from: this.accountInstance,
          value: amountInWei,
        })
        console.log("success")

        //renders the balance again.
        this.rerenderComponent();
        this.rerenderBalance();
        Toastify({
          text: "Payment made!",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
          position: "center",
          duration: 3000,
          // gravity: "bottom",
          // offset: { y: 100 },
          // onClick: function() {
          //   window.open(NFTurl, "_blank");
          // }
        }).showToast();
      }


    },




      async repayLoan(){
        const web3 = new Web3("http://localhost:8547");
        const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
        

      },
      async alertUser(){

      },
      async getOriginalNFTOwner(){
        const web3 = new Web3("http://localhost:8547");
        const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
        const result = await LoanContract.methods.getLoanDetails().call();
        const NFTid = result[9]
        let data = await req.json()
        let NFTaddress = data.address;

        let NFTcontract = new web3.eth.Contract(nftABI, NFTaddress);
        let nftowner = await NFTcontract.methods.originalOwnerOf(NFTid).call()
        this.nftOwner = nftowner;

      },

      //retrive NFT url from smart contract
      async getNFT(){
        const web3 = new Web3("http://localhost:8547");
        const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
        const result = await LoanContract.methods.getLoanDetails().call();
        const NFTid = result[9]
        const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
        let data = await req.json()
        let NFTaddress = data.address;

        let NFTcontract = new web3.eth.Contract(nftABI, NFTaddress);
        // Toastify({
        //     text: "hi",
        //     backgroundColor: "green",
        //     position: "center",
        // }).showToast();
        let NFTurl = await NFTcontract.methods.tokenURI(NFTid).call()
        let msg = document.createElement("div");
        //msg.innerHTML = "The NFT is available: <a href='" + NFTurl + "' target='_blank'>" + NFTurl + "</a> under id: " + NFTid;

        Toastify({
          text: "Click here to view the NFT for "+this.selectedAddress+" Contract!",
          backgroundColor: "green",
          position: "center",
          duration: 3000,
          gravity: "bottom",
          offset: { y: 100 },
          onClick: function() {
            window.open(NFTurl, "_blank");
          }
        }).showToast();
      },

      


      async getOwnedContracts(){
        const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            let arr = [];
            for (let i = 0; i < this.contractAddresses.length; i++) {
                let address = this.contractAddresses[i];
                try {
                    const LoanContract = new web3.eth.Contract(LoanABI, address);
                    let collateralHolder = this.account;
                    const result = await LoanContract.methods.getLoanDetails().call();
                    if (JSON.stringify(result[8].toLowerCase()) !== JSON.stringify(collateralHolder.toLowerCase()) && JSON.stringify(result[1].toLowerCase()) === JSON.stringify(collateralHolder.toLowerCase())) {
                        arr.push(address);
                    }
                }
                catch (error) {
                    continue;
                }
            }
            this.ownedContracts = arr;
        
      },
        getBalance() {
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
        //to fix
        async buyContract() {

          const check = /^[0-9.]+$/;
          const web3 = new Web3("http://localhost:8547");
          let contractPrice = this.contractPrice;
          const weiAmount = web3.utils.toWei(String(contractPrice), 'ether')  / (Math.pow(10, 3));
          


          // this.$refs.funds.getBalance();

            //const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            this.loanContractInstance = new web3.eth.Contract(LoanABI, this.selectedAddressBuy);

            const data = {
                sender_address:this.accountInstance,
                sender_password: localStorage.getItem('password'),
                recipient_address: accounts[0],
                value: weiAmount,
            };
            fetch("http://127.0.0.1:8000/send_transaction/", {
                method: "POST",
                body: new URLSearchParams(data)
            })
                .then(response => response.json())
                .then(data => {
                console.log(data);
                //this.output = data;
                if (data.transaction == null) {
                    Toastify({
                        text: "Insuffient funds"+data,
                        duration: 3000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true
                    }).showToast();
                }
                
                this.rerenderComponent();
                this.rerenderBalance();
                return;
            })
            try {
                const accounts = await web3.eth.getAccounts();
                await this.loanContractInstance.methods.changeOwner(this.accountInstance).send({
                    from: accounts[0],
                    gas: 3000000,
                });
                Toastify({
                    text: `Contract bought by` + this.accountInstance,
                    backgroundColor: "green",
                    position: "center",
                }).showToast();
            }
            catch (error) {
                Toastify({
                    text: "Error Occurred when changing owner",
                    backgroundColor: "red",
                    position: "center",
                }).showToast();
            }
            await this.getLoanDetails();
        },
        async getAccountInstance() {
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            for (let i = 0; i < accounts.length; i++) {
                let curAccount = accounts[i];
                if (JSON.stringify(curAccount.toLowerCase()) === JSON.stringify(this.account.toLowerCase())) {
                    this.accountInstance = curAccount;
                    break;
                }
            }
            //       Toastify({
            //       text: "The contract has not been deployed yet" + this.accountInstance,
            //       backgroundColor: 'orange',
            //       position: 'center',
            // }).showToast()
        },
        async getAddress() {
            const response = fetch("http://127.0.0.1:8000/get_address/", {
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
                    this.username = localStorage.getItem("username");
                }
            });
        },
        selectItem(index) {
            this.selectedItem = index;
            this.selectedAddress = this.ownedContracts[index]//this.contractAddresses[index];
            
        },
        selectLoanItem(index) {
            //this.selectedItem = index;
            this.selectedAddress = this.loanedContracts[index];
            this.selectedAddressLoan = this.loanedContracts[index];
            console.log(this.selectedAddressLoan)
        },
        selectBuyItem(index) {
            this.selectedAddress = this.contractsForSale[index];
            this.selectedAddressBuy = this.contractsForSale[index];
            console.log(this.selectedAddressLoan)
            // Toastify({
            //       text: "The contract has not been deployed yet",
            //       backgroundColor: 'orange',
            //       position: 'center',
            // }).showToast()
        },
        async getContract() {
            try {
                const response = await fetch("http://127.0.0.1:8000/contracts/");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log(data); // Log the response data to the console for debugging
                this.contractAddresses = data;
                let set = new Set();
                for (let i = 0; i < this.contractAddresses.length; i++) {
                    set.add(this.contractAddresses[i]);
                }
                this.contractAddresses = Array.from(set);
            }
            catch (error) {
                console.error(error); // Log any errors to the console
            }
        },
        async getSaleContracts() {
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            let arr = [];
            for (let i = 0; i < this.contractAddresses.length; i++) {
                let address = this.contractAddresses[i];
                try {
                    const LoanContract = new web3.eth.Contract(LoanABI, address);
                    let collateralHolder = this.account;
                    const result = await LoanContract.methods.getLoanDetails().call();
                    if (JSON.stringify(result[8].toLowerCase()) !== JSON.stringify(collateralHolder.toLowerCase()) && JSON.stringify(result[1].toLowerCase())===JSON.stringify(accounts[0].toLowerCase())) {
                        arr.push(address);
                    }
                }
                catch (error) {
                    continue;
                }
            }
            this.test = arr.length;
            this.contractsForSale = arr;
        },
        async getLoanedContracts() {
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            let arr = [];
            let contractStatus = [];
            for (let i = 0; i < this.contractAddresses.length; i++) {
                let address = this.contractAddresses[i];
                try {
                    const LoanContract = new web3.eth.Contract(LoanABI, address);
                    let collateralHolder = this.account;
                    const result = await LoanContract.methods.getLoanDetails().call();
                    // this.test = result[9]
                    // this.test = result[9].length + ", "+collateralHolder.length
                    if (JSON.stringify(result[8].toLowerCase()) === JSON.stringify(collateralHolder.toLowerCase())) {
                        // this.test = result[9]
                        arr.push(address);
                        contractStatus.push(result[6]);
                    }
                }
                catch (error) {
                    continue;
                }
            }
            //this.test = arr.length
            this.loanedContracts = arr;
            this.contractStatus = contractStatus;
        },
        async getLoanDetails() {
            try {
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                // const web3 = new Web3('http://localhost:8545');
                const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
                const result = await LoanContract.methods.getLoanDetails().call();

                //What the user would see when they get the details of a page
                // this.loanDetails = {
                //     borrower: result[0],
                //     lender: result[1],
                //     owner: result[2],
                //     amount: result[3],
                //     rate: result[4],
                //     duration: getDaysLeft((result[6]-result[5]), (result[6])) + " days",
                //     dueDate: unixToDate(result[6]),
                //     isRepaid: result[7] ? "Yes" : "No",
                //     collateralAmount: result[8],
                //     collateralHolder: result[9],
                //     collateralUrl: result[10],
                //     price: result[11],
                // };
                this.loanDetails = {
                    lender: result[0],
                    owner: result[1],
                    amount: result[2],
                    rate: result[3]/100,
                    duration: notifyRepaymentLeft((result[5]-result[4]), (result[5])) + " days",
                    dueDate: unixToDate(result[5]),
                    isRepaid: result[6] ? "Yes" : "No",
                    collateralAmount: result[7],
                    collateralHolder: result[8],
                    collateralUrl: result[9],
                    price: result[10],
                    amountreceived: result[11]

                }
                this.dayToPay = notifyRepaymentLeft((result[5]-result[4]), result[5]) + " days";
                


                //const result = await LoanContract.methods.getLoanDetails().call();
                const NFTid = await result[9]
                const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
                let data = await req.json()
                let NFTaddress = await data.address;


                let NFTcontract = new web3.eth.Contract(nftABI, NFTaddress);
                
                // Toastify({
                //     text: "hi",
                //     backgroundColor: "green",
                //     position: "center",
                // }).showToast();
                this.nftOwner = NFTid
                try{
                  this.originalnftOwner = await NFTcontract.methods.originalOwnerOf(NFTid).call()
                  this.nftOwner = await NFTcontract.methods.ownerOf(NFTid).call()
                }catch(error){
                  Toastify({
                    text: error,
                    backgroundColor: "green",
                    position: "center",
                }).showToast();
                }
                
                
                //this.nftOwner =await NFTcontract.methods.originalOwnerOf(NFTid).call()
                //this.nftOwner = NFTid
                //getOriginalNFTOwner();

            }
            catch (error) {
                Toastify({
                    text: "The contract has not been deployed yet",
                    backgroundColor: "orange",
                    position: "center",
                });
            }
        },
    },
    components: { BalanceComponent }
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
  border-radius: 10px ;
  margin-left: 15px;
  margin-right: 15px;
  border-width: thin;
}

.text-white {
  color: white;
}

#header{
  font-family: 'Arimo';
  font-size: 10px;
  color: white;
}

.btn{
  margin-right: 10px;
  margin-bottom: 10px;
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
  border-radius: 10px;
}

.grid-container-element { 
    display: grid; 
    grid-template-columns: 1fr 1fr; 
    grid-gap: 5px; 
    /* border: 1px solid black;  */
    width: 50%; 
    left: 60px;
    padding-top: 10px;
    width: 1920/2;
} 
.grid-child-element { 
    padding: 10px;
    margin-left: 30px;
    margin-right: 30px;
    margin: 10px; 
    border: 1px solid rgb(255, 255, 255); 
    border-radius: 10px;
    width: 475px
}
.message{
 color: white;
}

.contractinfo{
 background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  padding: 10px;
  margin-top: -70px;
  
}

.address{
  color: rgb(255, 166, 0);
}

li {
  cursor: pointer;
}
.selected {
    background-color: rgb(255, 166, 0);
    color: white;
  }


  .overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  background: rgba(0,0,0,.95);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  padding: 10px;
  margin-top: -70px;
  padding: 20px;
}

.user-box {
  position: relative;
}

.user-box input {
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

.user-box label {
  position: absolute;
  top:0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.user-box input:focus ~ label,
.user-box input:valid ~ label {
  top: -24px;
  left: 0;
  color: #f68e44;
  font-size: 12px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-active{
  transition: opacity 0.5s;
}

.fade-enter, 
.fade-leave-to {
  opacity: 0;
}


.flip-enter-active,
.flip-leave-active {
  transition: transform 0.5s;
}

.flip-enter,
.flip-leave-to {
  transform: rotateY(90deg);
}


.confirmation {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;

}
</style>