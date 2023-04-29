<template>
    
<div class="containers">
        <!-- <h3 style="color: white">Loans You've requested</h3> -->
        <!-- {{ account }} -->
    <div class="box" >
        <h4>Waiting Requests</h4>
        <div style="padding-bottom: 50px;">
        <nav id="lists2" style=" padding-top: 10px;">
            <ul v-if="waitingLoans && waitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in waitingLoans" :key="lender" :value="lender" @click="selectWaitLoan(index)" style="text-align: centre; padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px; width: 255px; margin-left: 5px; ">
                    Loan {{ lender.id }}
                </li>
              </div>
            </ul>
            <ul v-else>
                <li  style="margin-left: 10px; padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;  ">
                No Waiting Loans yet.
                </li>
            </ul>
           
          </nav>
        </div>
    </div>
    <div class="box">
        <h4>Approved Requests </h4>
        <nav id="lists2" style=" padding-top: 10px;">
            <ul v-if="approvedLoans && approvedLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in approvedLoans" :key="lender" :value="lender" @click="selectApproveLoan(index)" style="padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;width: 255px;  ">
                    Loan {{ lender.id }}
                </li>
              </div>
            </ul>
            <ul v-else>
                <li  style="margin-left: 10px; padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;  ">
                No Approved Loans yet.
                </li>
            </ul>
           
          </nav>
    </div>
    <div class="box">
        <h4>Rejected Requests</h4>
        <nav id="lists2" style=" padding-top: 10px;">
            <ul v-if="rejectedLoans && rejectedLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in rejectedLoans" :key="lender" :value="lender" @click="selectRejectLoan(index)" style="padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px; width: 255px; ">
                    Loan {{ lender.id }}
                </li>
              </div>
            </ul>
            <ul v-else>
                <li  style="margin-left: 10px; padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;  ">
                No Rejected Loans yet.
                </li>
            </ul>
           
          </nav>
    </div>
</div>
</template>

<script>

import Web3 from 'web3';
  import Toastify from 'toastify-js';
  import 'toastify-js/src/toastify.css';
  import nftABI from './contracts/MyNFT.json'

  import LoanABI from './contracts/LoanABI.json'
  import {Buffer } from 'buffer';
import NFTmint from './NFTmint.vue';
// import { ClientRequest } from 'http';
export default{
    data(){
        return {
            loans: [],
            waitingLoans: [],
            approvedLoans: [],
            rejectedLoans: [],
            account: null,
            selectedLoan: null,
        }
    },
    async mounted(){
        await this.getAddress();
        await this.getLoans();
    },
    methods:{
        async selectRejectLoan(index){
            this.selectedLoan = this.rejectedLoans[index]
            let loanRequest = this.selectedLoan;
            let loanDetails = "Loan Details \n"
            loanDetails += `ID: ${loanRequest.id}\nLoan Requested: ${loanRequest.amount} ETH\nLoan Duration: ${loanRequest.duration / 86400} Days\nAPR Rate: ${loanRequest.rate}%\n`;

            if (loanRequest.collateralValue) {
            loanDetails += `Collateral Value: ${loanRequest.collateralValue} ETH\n`;
            }
            if (loanRequest.collateralHolder) {
            loanDetails += `Collateral Holder: ${loanRequest.collateralHolder}\n`;
            }
            if (loanRequest.collateralURL) {
            loanDetails += `Collateral URL: ${loanRequest.collateralURL}\n`;
            }

            loanDetails += `Loan Approved: ${loanRequest.loanApproved ? "Yes" : "No"}\nLoan Waiting: ${loanRequest.loanWaiting ? "Yes": "No"}\nSale Price: ${loanRequest.price} ETH\nRequest Time: ${loanRequest.request_time ?  `${new Date(loanRequest.request_time).toLocaleDateString('en-US')} ${new Date(loanRequest.request_time).toLocaleTimeString('en-US', {hour12: false})}`: `${loanRequest.request_time.toLocaleDateString('en-US')} ${loanRequest.request_time.toLocaleTimeString('en-US', {hour12: false})}`}`;

            Toastify({
                        text: loanDetails,
                        duration: 20000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true,
            }).showToast();
        },
        async selectApproveLoan(index){
            this.selectedLoan = this.approvedLoans[index]
            let loanRequest = this.selectedLoan;
            let loanDetails = "Loan Details \n"
            loanDetails += `ID: ${loanRequest.id}\nLoan Requested: ${loanRequest.amount} ETH\nLoan Duration: ${loanRequest.duration / 86400} Days\nAPR Rate: ${loanRequest.rate}%\n`;

            if (loanRequest.collateralValue) {
            loanDetails += `Collateral Value: ${loanRequest.collateralValue} ETH\n`;
            }
            if (loanRequest.collateralHolder) {
            loanDetails += `Collateral Holder: ${loanRequest.collateralHolder}\n`;
            }
            if (loanRequest.collateralURL) {
            loanDetails += `Collateral URL: ${loanRequest.collateralURL}\n`;
            }

            loanDetails += `Loan Approved: ${loanRequest.loanApproved ? "Yes" : "No"}\nLoan Waiting: ${loanRequest.loanWaiting ? "Yes": "No"}\nSale Price: ${loanRequest.price} ETH\nRequest Time: ${loanRequest.request_time ?  `${new Date(loanRequest.request_time).toLocaleDateString('en-US')} ${new Date(loanRequest.request_time).toLocaleTimeString('en-US', {hour12: false})}`: `${loanRequest.request_time.toLocaleDateString('en-US')} ${loanRequest.request_time.toLocaleTimeString('en-US', {hour12: false})}`}`;

            Toastify({
                        text: loanDetails,
                        duration: 20000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true,
            }).showToast();
        },
        async selectWaitLoan(index){
            this.selectedLoan = this.waitingLoans[index]
            let loanRequest = this.selectedLoan
            let loanDetails = "Loan Details \n"
            loanDetails += `ID: ${loanRequest.id}\nLoan Requested: ${loanRequest.amount} ETH\nLoan Duration: ${loanRequest.duration / 86400} Days\nAPR Rate: ${loanRequest.rate}%\n`;

            if (loanRequest.collateralValue) {
            loanDetails += `Collateral Value: ${loanRequest.collateralValue} ETH\n`;
            }
            if (loanRequest.collateralHolder) {
            loanDetails += `Collateral Holder: ${loanRequest.collateralHolder}\n`;
            }
            if (loanRequest.collateralURL) {
            loanDetails += `Collateral URL: ${loanRequest.collateralURL}\n`;
            }

            loanDetails += `Loan Approved: ${loanRequest.loanApproved ? "Yes" : "No"}\nLoan Waiting: ${loanRequest.loanWaiting ? "Yes": "No"}\nRequest Time: ${loanRequest.request_time ?  `${new Date(loanRequest.request_time).toLocaleDateString('en-US')} ${new Date(loanRequest.request_time).toLocaleTimeString('en-US', {hour12: false})}`: `${loanRequest.request_time.toLocaleDateString('en-US')} ${loanRequest.request_time.toLocaleTimeString('en-US', {hour12: false})}`}`;

            Toastify({
                        text: loanDetails,
                        duration: 20000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true,
            }).showToast();
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
                    //this.form.collateralHolder = data.key;
                    //this.curAccount = data.key;
                    this.account = data.key;
                }
            });
        },

        //gets a list of loans 
        async getLoans() {
            try {
                const response = await fetch("http://127.0.0.1:8000/request_loan/");
                const data = await response.json();
                this.loans = await data;
                let userLoans = data.filter((loan)=>JSON.stringify(loan.collateralHolder.toLowerCase()) === JSON.stringify(this.account.toLowerCase()));
                this.waitingLoans = data.filter((loan) => loan.loanWaiting == true && JSON.stringify(loan.collateralHolder.toLowerCase()) === JSON.stringify(this.account.toLowerCase()) )
                this.approvedLoans =  userLoans.filter((loan) => loan.loanWaiting == false && loan.loanApproved) 
                this.rejectedLoans = userLoans.filter((loan) => loan.loanWaiting == false && !loan.loanApproved)

                
                //this.waitingLoans = data;
            } catch (error) {
                console.error(error);
            }

            
      }
    }
}

</script>


<style>

.containers {
padding-top: 10px;
  width: 60%;
  right: 14.45%;
  margin: 0 auto;
  position: absolute;
}

.box {


  width: 26.5%;
  height: 400px;
  margin-right: 10px;
  margin-bottom: 10px;
  text-align: center;
  color: white;
  font-size: 24px;
  padding-top: 80px;
  box-sizing: border-box;
  float: left;
  border-color: white;
  border-radius: 10px;
  border-width: thin;
  border-style: solid;


}

#lists2{
    height:150px;
    width:100%;
    overflow:hidden; 
    overflow-y:scroll;
    color: white;
    font-size: 13px;
}
</style>