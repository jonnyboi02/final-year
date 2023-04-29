
   <template>
    <!-- <NFTmint/> -->
    <div class='information' style="color: white;  ">
    <!-- <div v-if="borrower">
      {{borrower.address}}
    </div> -->


    <h2>Request Loan</h2>
    <!-- <div id = 'header'> -->
      <div id='contents' style="align-items: center; margin: auto; margin-left: 230px;width: 500px;border-style: solid; border-radius: 10px; border-width: thin;">
       
      
        <h5> Current Annual Interest rate is {{ baseInterestRate }}%  </h5>
        <h4>Calculated APR: {{ this.apr }}%</h4>
      </div>

    <div class="forms">
    <!-- </div> -->
    <!-- <form> -->
    <div v-if="loanContractAddress " id="deploy" > Contract Deployed at : {{ loanContractAddress }} </div>
    <div style="padding-bottom: 10px; " @change="aprCalculation">
    <h2>Enter the details</h2>
      <!-- form:{
          amount: 100,
          rate: 10,
          duration: 3600,
          collateralAmount: 200,
          collateralHolder: null,
          collateralUrl: " ",
          price: 10,
        } -->
        
        <label>Amount of Loan (in Ethers):</label>
        <br>
        <input  v-model="form.amount" style=" width: 250px; " required/>
        
        <br>
        <!-- Rate: <br><input  v-model="form.rate"/>
        <br> -->
        <label>Duration:</label><br>
        <select v-model="currentDuration" @change="durationToSeconds" style=" width: 250px; padding-left: 85px;padding-right: 45px;">
          <!--Need to set the form.duration stuff -->
          <option v-for="duration in options" :key="duration" :value= "duration">
            {{ duration }}
          </option>
        </select>
       
        <!-- Number of months:<br> <input v-model="form.duration"/> -->
        <br>
        Collateral value (in Ether): <br><input style = " width: 250px" v-model="form.collateralAmount" required/>
        <br>
        <!-- Borrower Address: <br><input v-model="form.collateralHolder"/>
        <br> -->
        <!-- Desired Price of Contract (in Ethers):<br> <input v-model="form.price"/>
        <br> -->
        Select Collateral: <br>
        <select v-model="nftFile"  style="padding-left: 45px;padding-right: 45px; width: 250px" required>
          <!--Need to set the form.duration stuff -->
          <option v-for="token in tokens" :key="token" :value= "token">
            {{ token }}
          </option>
        </select>
        <br>
        <button @click="viewNFT">View Current Collateral</button>
        <br>
        <!-- <button> Upload </button> -->
        <!-- <input style="margin-left: 60px;" type="file" @change="handleFileUpload" required/>
        <br> -->
        <br>
        <span v-if="!nftFile" style="color: red;">Please choose a collateral</span>

        <div style="padding-bottom: 10px; ">       
            <br>
      <button @click="deployLoanContract" class="button"  >Request Loan</button>
      <!-- <button @click="changeOwner" class="button" style="float: right; ">Change Contract Owner</button>
      <button @click="getLoanDetails">Get Contract Details</button>  -->
    </div>
    
        <UserLoanRequests style="position: absolute; margin-top: 15px; width: 1150px; transform: translate(0.9%, 5%); " />
    </div>
<!-- </form> -->

</div>
    <div style="padding-bottom: 10px; ">       
      <!-- <button class="button"  >Upload NFT</button> -->
      <!-- <button @click="changeOwner" class="button" style="float: right; ">Change Contract Owner</button>
      <button @click="getLoanDetails">Get Contract Details</button>  -->
    </div>

  

    <!-- <div style="border-style: solid; border-radius: 10px; border-width: thin; margin-left: 75px; margin-right: 75px;">
        <h4>Calculated APR: {{ this.apr }}%</h4>
    

    </div> -->
    <!-- <div>
        <UserLoanRequests/>
    </div> -->


    <!-- <button>Generate URL</button> -->
   
    <!-- <div style="padding-bottom: 10px; ">
      <button @click="changeOwner" class="button">Change Contract Owner</button>
    </div> -->
    <!-- <div style="padding-bottom: 10px; ">
      <button >Get Contract Details</button> 
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
    </div> -->
    
  </div>
  <!-- <div style="width: 70%;">
        <UserLoanRequests />
    </div> -->


  </template>
  
  <script>
  import Web3 from 'web3';
  import Toastify from 'toastify-js';
  import 'toastify-js/src/toastify.css';
  import nftABI from './contracts/MyNFT.json'

  import LoanABI from './contracts/LoanABI.json'
  import {Buffer } from 'buffer';
import NFTmint from './NFTmint.vue';
import UserLoanRequests from './UserLoanRequests.vue';
  export default {
    async mounted() {
        
        this.getAccounts();
        await this.getAddress();
        await this.getUsed();
        this.durationToSeconds();
        this.getTokens();
    },
    data() {
        return {
            contractAddresses: [],
            contractAddress: null,
            loanContractAddress: null,
            loanContractInstance: null,
            loanDetails: null,
            accounts: null,
            borrower: null,
            options: ["3 Months", "6 Months", "1 Year", "2 Years"],
            currentDuration: "3 Months",
            nftFile: null,
            form: {
                amount: "",
                rate: 3,
                duration: 3600,
                collateralAmount: "",
                collateralHolder: null,
                collateralUrl: " ",
                //0.5 Ether as default price
                price: 0,
            },
            value: "",
            test: "hi",
            accountInstance: "",
            contract:{
              address: "",
              instance: "",
            },
            tokens:[],
            baseInterestRate: 3,
            curAccount: null,
            apr: 3,
            token: null,
            currentToken: null,
        };
    },
    methods: {
        async viewNFT(){
      const web3 = new Web3("http://localhost:8547");
        //const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
       // const result = await LoanContract.methods.getLoanDetails().call();
       // const NFTid = result[9]
        const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
        let data = await req.json()
        let NFTaddress = data.address;

        let NFTcontract = new web3.eth.Contract(nftABI, NFTaddress);
        // Toastify({
        //     text: "hi",
        //     backgroundColor: "green",
        //     position: "center",
        // }).showToast();
        console.log(this.nftFile)
        let NFTurl = await NFTcontract.methods.tokenURI(this.nftFile).call()
        let msg = document.createElement("div");
        //msg.innerHTML = "The NFT is available: <a href='" + NFTurl + "' target='_blank'>" + NFTurl + "</a> under id: " + NFTid;

        Toastify({
          text: "Click here to view the NFT",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
          position: "center",
          duration: 3000,
          gravity: "bottom",
          offset: { y: 100 },
          onClick: function() {
            window.open(NFTurl, "_blank");
          }
        }).showToast();

    },
        async getTokens(){
            const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
            let data1 = await req.json()
            this.contract.address = data1.address

            
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();

            var account = null;

          
            for (let i =0; i< accounts.length; i++){
                if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(this.form.collateralHolder.toLowerCase())){
                    account = accounts[i]
                    break;
                }
            }

            var contract = new web3.eth.Contract(nftABI, this.contract.address);
            let nfts = []
            for (let i = 0;i< this.contractAddresses.length; i++){
                try{
                let address = this.contractAddresses[i]
                let LoanContract = new web3.eth.Contract(LoanABI, address);
                let result = await LoanContract.methods.getLoanDetails().call();
                if (!result[6]){
                    nfts.push(result[9])
                }
                
                }catch(error){
                    continue;
                }

            }
            let nftset = new Set(nfts);

            console.log(nftset)
            this.contract.instance = contract;
           
            //console.log(await contract.methods.tokensOfOwner(account).call())

            //gets all token
            let temp = await contract.methods.tokensOfOwner(account).call() 
            let result=[];
            for (let i = 0; i< temp.length; i++){
               let token = temp[i];
                    // let owner = await contract.methods.ownerOf(token).call();
                    // console.log(owner)
                    // let regex = new RegExp(`^${this.form.collateralHolder}$`, 'i');
                    // if(owner.match(regex)){
                       
                    //     // this.tokens.push(token)
                    //     //console.log(owner+" "+this.form.collateralHolder)
                    //     same.push(token)
                    // }
                    // else{
                        
                    // }
                    // const LoanContract = new web3.eth.Contract(LoanABI, this.selectedAddress);
                    if (nftset.has(token)){
                        continue
                    }
                    else{
                        result.push(token)
                    }



            } 
            this.tokens = result; 
            console.log(result)
            //console.log(account)
        },
        aprCalculation(){
            try{
                const rate = this.baseInterestRate
                const amount = this.form.amount
                const days = this.form.duration/86400
                const collateralValue = this.form.collateralAmount
                
                let interestRate = rate + (1 - (rate / 100)) * (1 - (collateralValue / amount)) * (365 / days);
                let interestAmount = (amount * (interestRate/100) *(days/365))

                //formula used to calculate the apr for stuff
                let apr = ((interestAmount/amount)/(days/365))*100;
                this.apr = apr.toFixed(2);
                if (isNaN(amount) || isNaN(collateralValue)){
                    Toastify({
                        text: "Enter Decimals",
                        duration: 3000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true
                    }).showToast();
                }

                console.log(days)
                if (apr<0){
                    this.form.rate = 3;
                    this.apr = 3;
                }
                else{
                    this.form.rate = this.apr;
                }
                // this.form.rate = apr;
                // Toastify({
                //         text: apr+ "Hi" + interestAmount,
                //         duration: 3000,
                //         close: true,
                //         backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                //         stopOnFocus: true
                //     }).showToast();
            }catch(error){
                Toastify({
                        text: "Error",
                        duration: 3000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true
                    }).showToast();
            }

        },
        handleFileUpload(event) {
            this.nftFile = event.target.files[0];
        },
        ethToWei() {
            const check = /^[0-9.]+$/;
            if (check.test(this.value)) {
                try {
                    const weiAmount = Web3.utils.toWei(this.form.amount.toString(), "ether") / 10 ** 3;
                    const weiAmountWithPrefix = "0x" + weiAmount;
                    this.value = weiAmountWithPrefix;
                }
                catch {
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
        },
        durationToSeconds() {
            if (this.currentDuration === "3 Months") {
                this.form.duration = 3 * 30 * 24 * 60 * 60;
            }
            else if (this.currentDuration === "6 Months") {
                this.form.duration = 6 * 30 * 24 * 60 * 60;
            }
            else if (this.currentDuration === "1 Year") {
                this.form.duration = 12 * 30 * 24 * 60 * 60;
            }
            else {
                this.form.duration = 24 * 30 * 24 * 60 * 60;
            }
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
                    this.form.collateralHolder = data.key;
                    this.curAccount = data.key;
                }
            });
        },
        async getAccounts() {
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            this.accounts = accounts;
            
        },
        async getUsed() {
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
                // let final = []
                // const web3 = new Web3("http://localhost:8547");

                // for (let i = 0 ;i< this.contractAddresses.length; i++){
                //     const LoanContract = new web3.eth.Contract(LoanABI, this.contractAddresses[i]);
                //     const result = await LoanContract.methods.getLoanDetails().call();

                //     if (result[9].normalize().toLowerCase() === this.accountInstance.normalize().toLowerCase()){
                //         final.push(result[9])
                //     }
                // }
                // this.

                
            }
            catch (error) {
                console.error(error); // Log any errors to the console
            }
        },
        async getLoanDetails() {
            try {
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                // const web3 = new Web3('http://localhost:8545');
                const LoanContract = new web3.eth.Contract(LoanABI, this.loanContractAddress);
                const result = await LoanContract.methods.getLoanDetails().call();
                // this.loanDetails = {
                //     borrower: result[0],
                //     lender: result[1],
                //     owner: result[2],
                //     amount: result[3],
                //     rate: result[4],
                //     duration: result[5],
                //     dueDate: result[6],
                //     isRepaid: result[7],
                //     collateralAmount: result[8],
                //     collateralHolder: result[9],
                //     collateralUrl: result[10],
                //     price: result[11],
                // };
                this.loanDetails = {
                    lender: result[0],
                    owner: result[1],
                    amount: result[2],
                    rate: result[3],
                    duration: result[4],
                    dueDate: result[5],
                    isRepaid: result[6],
                    collateralAmount: result[7],
                    collateralHolder: result[8],
                    collateralUrl: result[9],
                    price: result[10],
                    amountreceived: result[11]

                }
            }
            catch (error) {
                Toastify({
                    text: "The contract has not been deployed yet",
                    backgroundColor: "orange",
                    position: "center",
                });
            }
        },
        //used to issue the transaction
        sendTransaction() {
            //checking the data to make sure it is good
            if (this.form.amount === "") {
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
            if (check.test(this.form.amount)) {
                try {
                    const weiAmount = Web3.utils.toWei(this.form.amount.toString(), "ether") / (Math.pow(10, 3));
                    const weiAmountWithPrefix = "0x" + weiAmount;
                    this.value = weiAmountWithPrefix;
                }
                catch {
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
            // this.output=this.value
            const data = {
                sender_address: this.accounts[0],
                sender_password: "123456789",
                recipient_address: this.form.collateralHolder,
                value: this.value,
            };
            fetch("http://127.0.0.1:8000/send_transaction/", {
                method: "POST",
                body: new URLSearchParams(data)
            })
                .then(response => response.json())
                .then(data => {
                console.log(data);
                this.output = data;
                if (data.transaction == null) {
                    Toastify({
                        text: "Insuffient funds",
                        duration: 3000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true
                    }).showToast();
                }
                return;
                // else {
                //     Toastify({
                //         text: "Transaction sent successfully!",
                //         duration: 3000,
                //         close: true,
                //         backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                //         stopOnFocus: true
                //     }).showToast();
                // }
            })
                .catch(error => {
                console.error(error);
            });
        },
        async changeOwner() {
            try {
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                // call changeOwner function
                await this.loanContractInstance.methods.changeOwner(accounts[2]).send({
                    from: accounts[0],
                    gas: 3000000,
                });
                Toastify({
                    text: `Owner Changed to` + accounts[2],
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
        },
        async requestLoan(){
            //const formData = new FormData();
           //formData.append("file", this.nftFile);

            // const response1 = await fetch("http://localhost:8000/generate-url/", {
            //     method: "POST",
            //     body: formData
            // });
            // const data = await response1.json();
            //this.test = data.url;
            
            // let url = data.url

            //this.accountInstance = form.collateralHolder;

            var account = this.accountInstance;
            const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
            let data1 = await req.json()
            this.contract.address = data1.address

            
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();

            for (let i =0; i< accounts.length; i++){
                if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(this.form.collateralHolder.toLowerCase())){
                    account = accounts[i]
                    break;
                }
            }

            var contract = new web3.eth.Contract(nftABI, this.contract.address);

            

            this.contract.instance = contract;
           
            console.log(await contract.methods.tokensOfOwner(account).call())

           // await contract.methods.mint(account, url).send({from: accounts[0]})
           const tokenIds = await contract.methods.tokensOfOwner(account).call()
            this.tokens = tokenIds;
            const uri = await contract.methods.tokenURI(this.nftFile).call()
            this.uri = uri



            await web3.eth.personal.unlockAccount(account, localStorage.getItem('password'), 600);

            //function that send the token to the contract
            try {
                await contract.methods.transferFrom(account, accounts[0], this.nftFile).send({from: account})
                // Toastify({
                //     text: "Current Owner is" + await contract.methods.ownerOf(this.nftFile).call(),
                //     position: "center",
                //     back
                // }).showToast();
                
                console.log("Transfer successful")

  
            } catch (error) {
                Toastify({
                    text: "You have already made request with this NFT, it is now owned by: " + await contract.methods.ownerOf(this.nftFile).call(),
                    position: "center",
                    backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)"
                }).showToast();
                return;
            }

            //console.log(tokenIds[tokenIds.length-1])

            const tokenId = tokenIds[tokenIds.length-1];
            const from = account;
            const to = accounts[0];

            contract.events.Transfer()
            .on('data', function(event){
                console.log(event); // log the event object
            })
            .on('error', console.error);

            let curUser = await contract.methods.ownerOf(this.nftFile).call();
            console.log("Current User:", curUser);

            let bank = await contract.methods.tokensOfOwner(accounts[0]).call();
            console.log("Bank Tokens:", bank);

            // Toastify({
            //         text: await contract.methods.ownerOf(tokenIds[tokenIds.length-1]).call(),
            //         backgroundColor: "red",
            //         position: "center",
            //     }).showToast();

            // Toastify({
            //         text: "Error Occurred when changing owner"  + await contract.methods.tokensOfOwner(account).call(),
            //         backgroundColor: "red",
            //         position: "center",
            //     }).showToast();

            if (isNaN(this.form.rate) ||isNaN(this.form.amount) || isNaN(this.form.collateralAmount) ){
                Toastify({
                    text: `Enter valid input `,
                    backgroundColor: "red",
                    position: "center",
                }).showToast();
                return;
            }
            console.log("hi")
            console.log(this.nftFile)
            if (this.nftFile === null){
                Toastify({
                    text: `Please Upload a file `,
                    backgroundColor: "red",
                    position: "center",
                }).showToast();
                return;
            }

            // if (await contract.methods.ownerOf(this.nftFile))


            try{
                const response = await fetch("http://127.0.0.1:8000/request_loan/", {
                    method: 'POST',
                    body: JSON.stringify({
                        'account' : this.accountInstance,
                        'amount' : this.form.amount,
                        'duration' : this.form.duration,
                        'rate': this.form.rate,
                        'collateralValue': this.form.collateralAmount,
                        'collateralHolder': this.form.collateralHolder,
                        'collateralURL' : this.nftFile,
                        'price': this.form.price,

                    })
                })
                let datas = await response.json()
                Toastify({
                    text: `Loan Request Made! `+account,
                    backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)",
                    position: "center",
                }).showToast();

        }catch(error){
                            Toastify({
                            text: `Error deploying contract: `+error ,
                            backgroundColor: "red",
                            position: "center",
                        }).showToast();
        }
            // if (data.amount){
            //     Toastify({
            //                 text: `Error deploying contract: }` + this.form.collateralHoldercollateralHolder,
            //                 backgroundColor: "red",
            //                 position: "center",
            //             }).showToast();
            // }
            


        },
        async deployLoanContract() {
            // if (this.form.collateralAmount / this.form.amount < 0.75) {
            //     Toastify({
            //         text: "Please contribute a higher value NFT",
            //         backgroundColor: "red",
            //         position: "center",
            //     }).showToast();
            //     return;
            // }

            //this.requestLoan();
            //sends the funds
            //this.sendTransaction();

            this.requestLoan();

            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const networkId = await web3.eth.net.getId();
            const LoanContract = new web3.eth.Contract(LoanABI, null, { data: "60806040523480156200001157600080fd5b5060405162001656380380620016568339818101604052810190620000379190620003e8565b826000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660038190555085600481905550846005819055508360088190555082600960006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600a9081620001679190620006fb565b5080600b81905550600554426200017f919062000811565b6006819055506000600760006101000a81548160ff0219169083151502179055506000600c81905550505050505050506200084c565b6000604051905090565b600080fd5b600080fd5b6000819050919050565b620001de81620001c9565b8114620001ea57600080fd5b50565b600081519050620001fe81620001d3565b92915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000620002318262000204565b9050919050565b620002438162000224565b81146200024f57600080fd5b50565b600081519050620002638162000238565b92915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620002be8262000273565b810181811067ffffffffffffffff82111715620002e057620002df62000284565b5b80604052505050565b6000620002f5620001b5565b9050620003038282620002b3565b919050565b600067ffffffffffffffff82111562000326576200032562000284565b5b620003318262000273565b9050602081019050919050565b60005b838110156200035e57808201518184015260208101905062000341565b60008484015250505050565b6000620003816200037b8462000308565b620002e9565b905082815260208101848484011115620003a0576200039f6200026e565b5b620003ad8482856200033e565b509392505050565b600082601f830112620003cd57620003cc62000269565b5b8151620003df8482602086016200036a565b91505092915050565b600080600080600080600060e0888a0312156200040a5762000409620001bf565b5b60006200041a8a828b01620001ed565b97505060206200042d8a828b01620001ed565b9650506040620004408a828b01620001ed565b9550506060620004538a828b01620001ed565b9450506080620004668a828b0162000252565b93505060a088015167ffffffffffffffff8111156200048a5762000489620001c4565b5b620004988a828b01620003b5565b92505060c0620004ab8a828b01620001ed565b91505092959891949750929550565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806200050d57607f821691505b602082108103620005235762000522620004c5565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026200058d7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff826200054e565b6200059986836200054e565b95508019841693508086168417925050509392505050565b6000819050919050565b6000620005dc620005d6620005d084620001c9565b620005b1565b620001c9565b9050919050565b6000819050919050565b620005f883620005bb565b620006106200060782620005e3565b8484546200055b565b825550505050565b600090565b6200062762000618565b62000634818484620005ed565b505050565b5b818110156200065c57620006506000826200061d565b6001810190506200063a565b5050565b601f821115620006ab57620006758162000529565b62000680846200053e565b8101602085101562000690578190505b620006a86200069f856200053e565b83018262000639565b50505b505050565b600082821c905092915050565b6000620006d060001984600802620006b0565b1980831691505092915050565b6000620006eb8383620006bd565b9150826002028217905092915050565b6200070682620004ba565b67ffffffffffffffff81111562000722576200072162000284565b5b6200072e8254620004f4565b6200073b82828562000660565b600060209050601f8311600181146200077357600084156200075e578287015190505b6200076a8582620006dd565b865550620007da565b601f198416620007838662000529565b60005b82811015620007ad5784890151825560018201915060208501945060208101905062000786565b86831015620007cd5784890151620007c9601f891682620006bd565b8355505b6001600288020188555050505b505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006200081e82620001c9565b91506200082b83620001c9565b9250828201905080821115620008465762000845620007e2565b5b92915050565b610dfa806200085c6000396000f3fe6080604052600436106101025760003560e01c80638da5cb5b11610095578063a6f9dae111610064578063a6f9dae1146103f0578063aa8c217c14610419578063bcead63e14610444578063d524b0ff1461046f578063e27facdc1461049a576101ff565b80638da5cb5b1461033957806392d09ceb14610364578063a035b1fe1461038f578063a3b9e39d146103ba576101ff565b806357f7d74f116100d157806357f7d74f1461028f5780636164051a146102b8578063786716fe146102e35780637df1f1b91461030e576101ff565b80630b168f21146102045780630fb5a6b41461022f5780632c4e722e1461025a578063330aec3e14610285576101ff565b366101ff57600760009054906101000a900460ff1615610157576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161014e90610983565b60405180910390fd5b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146101e5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101dc906109ef565b60405180910390fd5b34600c60008282546101f79190610a48565b925050819055005b600080fd5b34801561021057600080fd5b506102196104c5565b6040516102269190610afb565b60405180910390f35b34801561023b57600080fd5b50610244610553565b6040516102519190610b2c565b60405180910390f35b34801561026657600080fd5b5061026f610559565b60405161027c9190610b2c565b60405180910390f35b61028d61055f565b005b34801561029b57600080fd5b506102b660048036038101906102b19190610baa565b610641565b005b3480156102c457600080fd5b506102cd6106c6565b6040516102da9190610bf2565b60405180910390f35b3480156102ef57600080fd5b506102f86106d9565b6040516103059190610b2c565b60405180910390f35b34801561031a57600080fd5b506103236106df565b6040516103309190610c1c565b60405180910390f35b34801561034557600080fd5b5061034e610703565b60405161035b9190610c1c565b60405180910390f35b34801561037057600080fd5b50610379610729565b6040516103869190610b2c565b60405180910390f35b34801561039b57600080fd5b506103a461072f565b6040516103b19190610b2c565b60405180910390f35b3480156103c657600080fd5b506103cf610735565b6040516103e79c9b9a99989796959493929190610c37565b60405180910390f35b3480156103fc57600080fd5b5061041760048036038101906104129190610baa565b61088a565b005b34801561042557600080fd5b5061042e6108ce565b60405161043b9190610b2c565b60405180910390f35b34801561045057600080fd5b506104596108d4565b6040516104669190610c1c565b60405180910390f35b34801561047b57600080fd5b506104846108fa565b6040516104919190610b2c565b60405180910390f35b3480156104a657600080fd5b506104af610900565b6040516104bc9190610c1c565b60405180910390f35b600a80546104d290610d27565b80601f01602080910402602001604051908101604052809291908181526020018280546104fe90610d27565b801561054b5780601f106105205761010080835404028352916020019161054b565b820191906000526020600020905b81548152906001019060200180831161052e57829003601f168201915b505050505081565b60055481565b60045481565b600034116105a2576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161059990610da4565b60405180910390fd5b34600c60008282546105b49190610a48565b92505081905550600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc479081150290604051600060405180830381858888f19350505050158015610623573d6000803e3d6000fd5b506001600760006101000a81548160ff021916908315150217905550565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600760009054906101000a900460ff1681565b60065481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60085481565b600b5481565b60008060008060008060008060006060600080600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600354600454600554600654600760009054906101000a900460ff16600854600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600a600b54600c548280546107e490610d27565b80601f016020809104026020016040519081016040528092919081815260200182805461081090610d27565b801561085d5780601f106108325761010080835404028352916020019161085d565b820191906000526020600020905b81548152906001019060200180831161084057829003601f168201915b505050505092509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60035481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600c5481565b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600082825260208201905092915050565b7f4c6f616e20697320616c72656164792072657061696400000000000000000000600082015250565b600061096d601683610926565b915061097882610937565b602082019050919050565b6000602082019050818103600083015261099c81610960565b9050919050565b7f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e74600082015250565b60006109d9602083610926565b91506109e4826109a3565b602082019050919050565b60006020820190508181036000830152610a08816109cc565b9050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000610a5382610a0f565b9150610a5e83610a0f565b9250828201905080821115610a7657610a75610a19565b5b92915050565b600081519050919050565b60005b83811015610aa5578082015181840152602081019050610a8a565b60008484015250505050565b6000601f19601f8301169050919050565b6000610acd82610a7c565b610ad78185610926565b9350610ae7818560208601610a87565b610af081610ab1565b840191505092915050565b60006020820190508181036000830152610b158184610ac2565b905092915050565b610b2681610a0f565b82525050565b6000602082019050610b416000830184610b1d565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610b7782610b4c565b9050919050565b610b8781610b6c565b8114610b9257600080fd5b50565b600081359050610ba481610b7e565b92915050565b600060208284031215610bc057610bbf610b47565b5b6000610bce84828501610b95565b91505092915050565b60008115159050919050565b610bec81610bd7565b82525050565b6000602082019050610c076000830184610be3565b92915050565b610c1681610b6c565b82525050565b6000602082019050610c316000830184610c0d565b92915050565b600061018082019050610c4d600083018f610c0d565b610c5a602083018e610c0d565b610c67604083018d610b1d565b610c74606083018c610b1d565b610c81608083018b610b1d565b610c8e60a083018a610b1d565b610c9b60c0830189610be3565b610ca860e0830188610b1d565b610cb6610100830187610c0d565b818103610120830152610cc98186610ac2565b9050610cd9610140830185610b1d565b610ce7610160830184610b1d565b9d9c50505050505050505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680610d3f57607f821691505b602082108103610d5257610d51610cf8565b5b50919050565b7f56616c7565206d7573742062652067726561746572207468616e203000000000600082015250565b6000610d8e601c83610926565b9150610d9982610d58565b602082019050919050565b60006020820190508181036000830152610dbd81610d81565b905091905056fea26469706673582212204128b9814fe8d1a7140210d55c2b745348d3aba4021ac860e96517f276c2cfca64736f6c63430008120033" });
            const gas = 3000000; // Set the gas limit to 3000000
            const options = {
                from: accounts[0],
                gas: gas, // Pass the gas limit to the send method
            };
            var account = null;
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
                    this.form.collateralHolder = data.key;
                    for (let i = 0; i < accounts.length; i++) {
                        if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(data.key.toLowerCase())) {
                            this.form.collateralHolder = accounts[i];
                            break;
                        }
                    }
                    //this.senderPassword = localStorage.getItem('password')
                }
            });
            // for (let i = 0; i < accounts.length; i++) {
            //     if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(this.form.collateralHolder.toLowerCase())) {
            //         this.form.collateralHolder = accounts[i];
            //         account = accounts[i];
            //         this.accountInstance = accounts[i];

            //         //generate the URL and transfer ownership of this
            //         await this.generateURL();
                    
            //         this.form.collateralUrl = this.tokens[this.tokens.length-1]

            //         const args = [
            //             this.form.amount,
            //             this.form.rate,
            //             this.form.duration,
            //             this.form.collateralAmount,
            //             this.form.collateralHolder,
            //             this.tokens[this.tokens.length-1],
            //             this.form.price,
            //         ];
            //         try {
            //             //deploys the smart contract
            //             const contract = await LoanContract.deploy({
            //                 arguments: args
            //             }).send(options);
            //             this.loanContractAddress = contract.options.address;
            //             this.loanContractInstance = new web3.eth.Contract(LoanABI, this.loanContractAddress);
            //             const response = fetch("http://127.0.0.1:8000/contracts/", {
            //                 method: "PUT",
            //                 headers: {
            //                     "Content-Type": "application/json"
            //                 },
            //                 body: JSON.stringify({
            //                     "address": this.loanContractAddress,
            //                 }),
            //             });

            //             const fileReader = new FileReader();
  
            //             Toastify({
            //                 text: `Deployed loan contract ` + this.loanContractAddress + " " + this.form.collateralHolder,
            //                 backgroundColor: "green",
            //                 position: "center",
            //             }).showToast();
            //         }
            //         catch (error) {
            //             Toastify({
            //                 text: `Error deploying contract: ${error}` + this.form.collateralHoldercollateralHolder,
            //                 backgroundColor: "red",
            //                 position: "center",
            //             }).showToast();
            //         }
            //         break;
            //     }
            // }
        },
        async generateURL() {

            //generates the url for the uploaded nft
            const formData = new FormData();
            formData.append("file", this.nftFile);
            const response = await fetch("http://localhost:8000/generate-url/", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            this.test = data.url;
            this.form.collateralUrl = data.url;
            let url = data.url

            const check = await fetch("http://127.0.0.1:8000/get_nft_length/")
            
            // {
            //     method: "POST",
            //     body: new URLSearchParams(data)
            // })
            //check if there is an instance of this item
            const checkData = await check.json()

            if (checkData.length === '1'){
                const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
                let data = await req.json()
                this.contract.address = data.address

                // Toastify({
                // text: "NFT uploaded "+this.contract.address + "with uri "+url,
                // position: "center",
                // }).showToast();

                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                
                let contract = new web3.eth.Contract(nftABI, this.contract.address);

                this.contract.instance = contract;
                // Toastify({
                // text: "NFT uploaded "+this.contract.address + "with uri "+url,
                // position: "center",
                // }).showToast();

            //mints a users nft to thier account
                await contract.methods.mint(this.accountInstance, url).send({from: accounts[0]})
                const tokenIds = await contract.methods.tokensOfOwner(this.accountInstance).call()
                this.tokens = tokenIds;
                const uri = await contract.methods.tokenURI(tokenIds[tokenIds.length-1]).call()
                //transfers nft to contract
                try{

                    await web3.eth.personal.unlockAccount(this.accountInstance, localStorage.getItem('password'), 600);

                    let d = await contract.methods.transferFrom(this.accountInstance,contract.options.address ,tokenIds[tokenIds.length-1]) .send({from: this.accountInstance})

                    Toastify({
                    text: "NFT uploaded "+this.contract.address + "with uri "+uri+d,
                    position: "center",
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                    }).showToast();

                    // const id = await contract.methods.tokensOfOwner(contract.options.address).call()
                    //     Toastify({
                    // text: id,
                    // position: "center",
                    // }).showToast();
                }catch(error){
                    Toastify({
                    text: "" + error + localStorage.getItem('password'),
                    position: "center",
                    }).showToast();
                }

            }
            else{

            this.test = checkData.length



            //deploys the smart contract
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const NFTContract = await new web3.eth.Contract(nftABI, null, {data: "60806040523480156200001157600080fd5b50604051620035cf380380620035cf8339818101604052810190620000379190620002e8565b818181600090816200004a9190620005b8565b5080600190816200005c9190620005b8565b5050506200007f620000736200008760201b60201c565b6200008f60201b60201c565b50506200069f565b600033905090565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b6000604051905090565b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620001be8262000173565b810181811067ffffffffffffffff82111715620001e057620001df62000184565b5b80604052505050565b6000620001f562000155565b9050620002038282620001b3565b919050565b600067ffffffffffffffff82111562000226576200022562000184565b5b620002318262000173565b9050602081019050919050565b60005b838110156200025e57808201518184015260208101905062000241565b60008484015250505050565b6000620002816200027b8462000208565b620001e9565b905082815260208101848484011115620002a0576200029f6200016e565b5b620002ad8482856200023e565b509392505050565b600082601f830112620002cd57620002cc62000169565b5b8151620002df8482602086016200026a565b91505092915050565b600080604083850312156200030257620003016200015f565b5b600083015167ffffffffffffffff81111562000323576200032262000164565b5b6200033185828601620002b5565b925050602083015167ffffffffffffffff81111562000355576200035462000164565b5b6200036385828601620002b5565b9150509250929050565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680620003c057607f821691505b602082108103620003d657620003d562000378565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b600060088302620004407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8262000401565b6200044c868362000401565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600062000499620004936200048d8462000464565b6200046e565b62000464565b9050919050565b6000819050919050565b620004b58362000478565b620004cd620004c482620004a0565b8484546200040e565b825550505050565b600090565b620004e4620004d5565b620004f1818484620004aa565b505050565b5b8181101562000519576200050d600082620004da565b600181019050620004f7565b5050565b601f82111562000568576200053281620003dc565b6200053d84620003f1565b810160208510156200054d578190505b620005656200055c85620003f1565b830182620004f6565b50505b505050565b600082821c905092915050565b60006200058d600019846008026200056d565b1980831691505092915050565b6000620005a883836200057a565b9150826002028217905092915050565b620005c3826200036d565b67ffffffffffffffff811115620005df57620005de62000184565b5b620005eb8254620003a7565b620005f88282856200051d565b600060209050601f8311600181146200063057600084156200061b578287015190505b6200062785826200059a565b86555062000697565b601f1984166200064086620003dc565b60005b828110156200066a5784890151825560018201915060208501945060208101905062000643565b868310156200068a578489015162000686601f8916826200057a565b8355505b6001600288020188555050505b505050505050565b612f2080620006af6000396000f3fe608060405234801561001057600080fd5b50600436106101215760003560e01c806373b64ac5116100ad578063b88d4fde11610071578063b88d4fde1461031a578063c87b56dd14610336578063d0def52114610366578063e985e9c514610396578063f2fde38b146103c657610121565b806373b64ac5146102625780638462151c146102925780638da5cb5b146102c257806395d89b41146102e0578063a22cb465146102fe57610121565b806323b872dd116100f457806323b872dd146101c057806342842e0e146101dc5780636352211e146101f857806370a0823114610228578063715018a61461025857610121565b806301ffc9a71461012657806306fdde0314610156578063081812fc14610174578063095ea7b3146101a4575b600080fd5b610140600480360381019061013b9190611b25565b6103e2565b60405161014d9190611b6d565b60405180910390f35b61015e6104c4565b60405161016b9190611c18565b60405180910390f35b61018e60048036038101906101899190611c70565b610556565b60405161019b9190611cde565b60405180910390f35b6101be60048036038101906101b99190611d25565b61059c565b005b6101da60048036038101906101d59190611d65565b6106b3565b005b6101f660048036038101906101f19190611d65565b610713565b005b610212600480360381019061020d9190611c70565b610733565b60405161021f9190611cde565b60405180910390f35b610242600480360381019061023d9190611db8565b6107b9565b60405161024f9190611df4565b60405180910390f35b610260610870565b005b61027c60048036038101906102779190611c70565b610884565b6040516102899190611cde565b60405180910390f35b6102ac60048036038101906102a79190611db8565b610909565b6040516102b99190611ecd565b60405180910390f35b6102ca6109a0565b6040516102d79190611cde565b60405180910390f35b6102e86109ca565b6040516102f59190611c18565b60405180910390f35b61031860048036038101906103139190611f1b565b610a5c565b005b610334600480360381019061032f9190612090565b610a72565b005b610350600480360381019061034b9190611c70565b610ad4565b60405161035d9190611c18565b60405180910390f35b610380600480360381019061037b91906121b4565b610bc1565b60405161038d9190611df4565b60405180910390f35b6103b060048036038101906103ab9190612210565b610cc0565b6040516103bd9190611b6d565b60405180910390f35b6103e060048036038101906103db9190611db8565b610d54565b005b60007f80ac58cd000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614806104ad57507f5b5e139f000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916145b806104bd57506104bc82610d68565b5b9050919050565b6060600080546104d39061227f565b80601f01602080910402602001604051908101604052809291908181526020018280546104ff9061227f565b801561054c5780601f106105215761010080835404028352916020019161054c565b820191906000526020600020905b81548152906001019060200180831161052f57829003601f168201915b5050505050905090565b600061056182610dd2565b6004600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b60006105a782610733565b90508073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1603610617576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161060e90612322565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff16610636610e1d565b73ffffffffffffffffffffffffffffffffffffffff16148061066557506106648161065f610e1d565b610cc0565b5b6106a4576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161069b906123b4565b60405180910390fd5b6106ae8383610e25565b505050565b6106c46106be610e1d565b82610ede565b610703576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106fa90612446565b60405180910390fd5b61070e838383610f73565b505050565b61072e83838360405180602001604052806000815250610a72565b505050565b60008061073f8361126c565b9050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16036107b0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016107a7906124b2565b60405180910390fd5b80915050919050565b60008073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603610829576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161082090612544565b60405180910390fd5b600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b6108786112a9565b6108826000611327565b565b600061088f826113ed565b6108ce576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108c5906125d6565b60405180910390fd5b6009600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b6060600a60008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002080548060200260200160405190810160405280929190818152602001828054801561099457602002820191906000526020600020905b815481526020019060010190808311610980575b50505050509050919050565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b6060600180546109d99061227f565b80601f0160208091040260200160405190810160405280929190818152602001828054610a059061227f565b8015610a525780601f10610a2757610100808354040283529160200191610a52565b820191906000526020600020905b815481529060010190602001808311610a3557829003601f168201915b5050505050905090565b610a6e610a67610e1d565b838361142e565b5050565b610a83610a7d610e1d565b83610ede565b610ac2576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ab990612446565b60405180910390fd5b610ace8484848461159a565b50505050565b6060610adf826113ed565b610b1e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b1590612668565b60405180910390fd5b600860008381526020019081526020016000208054610b3c9061227f565b80601f0160208091040260200160405190810160405280929190818152602001828054610b689061227f565b8015610bb55780601f10610b8a57610100808354040283529160200191610bb5565b820191906000526020600020905b815481529060010190602001808311610b9857829003601f168201915b50505050509050919050565b6000610bcb6112a9565b60076000815480929190610bde906126b7565b919050555060006007549050610bf484826115f6565b610bfe8184611813565b836009600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600a60008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190806001815401808255809150506001900390600052602060002001600090919091909150558091505092915050565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b610d5c6112a9565b610d6581611880565b50565b60007f01ffc9a7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916149050919050565b610ddb816113ed565b610e1a576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610e11906124b2565b60405180910390fd5b50565b600033905090565b816004600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16610e9883610733565b73ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45050565b600080610eea83610733565b90508073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff161480610f2c5750610f2b8185610cc0565b5b80610f6a57508373ffffffffffffffffffffffffffffffffffffffff16610f5284610556565b73ffffffffffffffffffffffffffffffffffffffff16145b91505092915050565b8273ffffffffffffffffffffffffffffffffffffffff16610f9382610733565b73ffffffffffffffffffffffffffffffffffffffff1614610fe9576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610fe090612771565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603611058576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161104f90612803565b60405180910390fd5b6110658383836001611903565b8273ffffffffffffffffffffffffffffffffffffffff1661108582610733565b73ffffffffffffffffffffffffffffffffffffffff16146110db576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110d290612771565b60405180910390fd5b6004600082815260200190815260200160002060006101000a81549073ffffffffffffffffffffffffffffffffffffffff02191690556001600360008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055506001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a46112678383836001611909565b505050565b60006002600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b6112b1610e1d565b73ffffffffffffffffffffffffffffffffffffffff166112cf6109a0565b73ffffffffffffffffffffffffffffffffffffffff1614611325576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161131c9061286f565b60405180910390fd5b565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b60008073ffffffffffffffffffffffffffffffffffffffff1661140f8361126c565b73ffffffffffffffffffffffffffffffffffffffff1614159050919050565b8173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff160361149c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611493906128db565b60405180910390fd5b80600560008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c318360405161158d9190611b6d565b60405180910390a3505050565b6115a5848484610f73565b6115b18484848461190f565b6115f0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016115e79061296d565b60405180910390fd5b50505050565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603611665576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161165c906129d9565b60405180910390fd5b61166e816113ed565b156116ae576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016116a590612a45565b60405180910390fd5b6116bc600083836001611903565b6116c5816113ed565b15611705576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016116fc90612a45565b60405180910390fd5b6001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a461180f600083836001611909565b5050565b61181c826113ed565b61185b576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161185290612ad7565b60405180910390fd5b8060086000848152602001908152602001600020908161187b9190612ca3565b505050565b6118886112a9565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16036118f7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016118ee90612de7565b60405180910390fd5b61190081611327565b50565b50505050565b50505050565b60006119308473ffffffffffffffffffffffffffffffffffffffff16611a96565b15611a89578373ffffffffffffffffffffffffffffffffffffffff1663150b7a02611959610e1d565b8786866040518563ffffffff1660e01b815260040161197b9493929190612e5c565b6020604051808303816000875af19250505080156119b757506040513d601f19601f820116820180604052508101906119b49190612ebd565b60015b611a39573d80600081146119e7576040519150601f19603f3d011682016040523d82523d6000602084013e6119ec565b606091505b506000815103611a31576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611a289061296d565b60405180910390fd5b805181602001fd5b63150b7a0260e01b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916817bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614915050611a8e565b600190505b949350505050565b6000808273ffffffffffffffffffffffffffffffffffffffff163b119050919050565b6000604051905090565b600080fd5b600080fd5b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b611b0281611acd565b8114611b0d57600080fd5b50565b600081359050611b1f81611af9565b92915050565b600060208284031215611b3b57611b3a611ac3565b5b6000611b4984828501611b10565b91505092915050565b60008115159050919050565b611b6781611b52565b82525050565b6000602082019050611b826000830184611b5e565b92915050565b600081519050919050565b600082825260208201905092915050565b60005b83811015611bc2578082015181840152602081019050611ba7565b60008484015250505050565b6000601f19601f8301169050919050565b6000611bea82611b88565b611bf48185611b93565b9350611c04818560208601611ba4565b611c0d81611bce565b840191505092915050565b60006020820190508181036000830152611c328184611bdf565b905092915050565b6000819050919050565b611c4d81611c3a565b8114611c5857600080fd5b50565b600081359050611c6a81611c44565b92915050565b600060208284031215611c8657611c85611ac3565b5b6000611c9484828501611c5b565b91505092915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000611cc882611c9d565b9050919050565b611cd881611cbd565b82525050565b6000602082019050611cf36000830184611ccf565b92915050565b611d0281611cbd565b8114611d0d57600080fd5b50565b600081359050611d1f81611cf9565b92915050565b60008060408385031215611d3c57611d3b611ac3565b5b6000611d4a85828601611d10565b9250506020611d5b85828601611c5b565b9150509250929050565b600080600060608486031215611d7e57611d7d611ac3565b5b6000611d8c86828701611d10565b9350506020611d9d86828701611d10565b9250506040611dae86828701611c5b565b9150509250925092565b600060208284031215611dce57611dcd611ac3565b5b6000611ddc84828501611d10565b91505092915050565b611dee81611c3a565b82525050565b6000602082019050611e096000830184611de5565b92915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b611e4481611c3a565b82525050565b6000611e568383611e3b565b60208301905092915050565b6000602082019050919050565b6000611e7a82611e0f565b611e848185611e1a565b9350611e8f83611e2b565b8060005b83811015611ec0578151611ea78882611e4a565b9750611eb283611e62565b925050600181019050611e93565b5085935050505092915050565b60006020820190508181036000830152611ee78184611e6f565b905092915050565b611ef881611b52565b8114611f0357600080fd5b50565b600081359050611f1581611eef565b92915050565b60008060408385031215611f3257611f31611ac3565b5b6000611f4085828601611d10565b9250506020611f5185828601611f06565b9150509250929050565b600080fd5b600080fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b611f9d82611bce565b810181811067ffffffffffffffff82111715611fbc57611fbb611f65565b5b80604052505050565b6000611fcf611ab9565b9050611fdb8282611f94565b919050565b600067ffffffffffffffff821115611ffb57611ffa611f65565b5b61200482611bce565b9050602081019050919050565b82818337600083830152505050565b600061203361202e84611fe0565b611fc5565b90508281526020810184848401111561204f5761204e611f60565b5b61205a848285612011565b509392505050565b600082601f83011261207757612076611f5b565b5b8135612087848260208601612020565b91505092915050565b600080600080608085870312156120aa576120a9611ac3565b5b60006120b887828801611d10565b94505060206120c987828801611d10565b93505060406120da87828801611c5b565b925050606085013567ffffffffffffffff8111156120fb576120fa611ac8565b5b61210787828801612062565b91505092959194509250565b600067ffffffffffffffff82111561212e5761212d611f65565b5b61213782611bce565b9050602081019050919050565b600061215761215284612113565b611fc5565b90508281526020810184848401111561217357612172611f60565b5b61217e848285612011565b509392505050565b600082601f83011261219b5761219a611f5b565b5b81356121ab848260208601612144565b91505092915050565b600080604083850312156121cb576121ca611ac3565b5b60006121d985828601611d10565b925050602083013567ffffffffffffffff8111156121fa576121f9611ac8565b5b61220685828601612186565b9150509250929050565b6000806040838503121561222757612226611ac3565b5b600061223585828601611d10565b925050602061224685828601611d10565b9150509250929050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000600282049050600182168061229757607f821691505b6020821081036122aa576122a9612250565b5b50919050565b7f4552433732313a20617070726f76616c20746f2063757272656e74206f776e6560008201527f7200000000000000000000000000000000000000000000000000000000000000602082015250565b600061230c602183611b93565b9150612317826122b0565b604082019050919050565b6000602082019050818103600083015261233b816122ff565b9050919050565b7f4552433732313a20617070726f76652063616c6c6572206973206e6f7420746f60008201527f6b656e206f776e6572206f7220617070726f76656420666f7220616c6c000000602082015250565b600061239e603d83611b93565b91506123a982612342565b604082019050919050565b600060208201905081810360008301526123cd81612391565b9050919050565b7f4552433732313a2063616c6c6572206973206e6f7420746f6b656e206f776e6560008201527f72206f7220617070726f76656400000000000000000000000000000000000000602082015250565b6000612430602d83611b93565b915061243b826123d4565b604082019050919050565b6000602082019050818103600083015261245f81612423565b9050919050565b7f4552433732313a20696e76616c696420746f6b656e2049440000000000000000600082015250565b600061249c601883611b93565b91506124a782612466565b602082019050919050565b600060208201905081810360008301526124cb8161248f565b9050919050565b7f4552433732313a2061646472657373207a65726f206973206e6f74206120766160008201527f6c6964206f776e65720000000000000000000000000000000000000000000000602082015250565b600061252e602983611b93565b9150612539826124d2565b604082019050919050565b6000602082019050818103600083015261255d81612521565b9050919050565b7f4552433732313a206f776e657220717565727920666f72206e6f6e657869737460008201527f656e7420746f6b656e0000000000000000000000000000000000000000000000602082015250565b60006125c0602983611b93565b91506125cb82612564565b604082019050919050565b600060208201905081810360008301526125ef816125b3565b9050919050565b7f4552433732314d657461646174613a2055524920717565727920666f72206e6f60008201527f6e6578697374656e7420746f6b656e0000000000000000000000000000000000602082015250565b6000612652602f83611b93565b915061265d826125f6565b604082019050919050565b6000602082019050818103600083015261268181612645565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006126c282611c3a565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82036126f4576126f3612688565b5b600182019050919050565b7f4552433732313a207472616e736665722066726f6d20696e636f72726563742060008201527f6f776e6572000000000000000000000000000000000000000000000000000000602082015250565b600061275b602583611b93565b9150612766826126ff565b604082019050919050565b6000602082019050818103600083015261278a8161274e565b9050919050565b7f4552433732313a207472616e7366657220746f20746865207a65726f2061646460008201527f7265737300000000000000000000000000000000000000000000000000000000602082015250565b60006127ed602483611b93565b91506127f882612791565b604082019050919050565b6000602082019050818103600083015261281c816127e0565b9050919050565b7f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572600082015250565b6000612859602083611b93565b915061286482612823565b602082019050919050565b600060208201905081810360008301526128888161284c565b9050919050565b7f4552433732313a20617070726f766520746f2063616c6c657200000000000000600082015250565b60006128c5601983611b93565b91506128d08261288f565b602082019050919050565b600060208201905081810360008301526128f4816128b8565b9050919050565b7f4552433732313a207472616e7366657220746f206e6f6e20455243373231526560008201527f63656976657220696d706c656d656e7465720000000000000000000000000000602082015250565b6000612957603283611b93565b9150612962826128fb565b604082019050919050565b600060208201905081810360008301526129868161294a565b9050919050565b7f4552433732313a206d696e7420746f20746865207a65726f2061646472657373600082015250565b60006129c3602083611b93565b91506129ce8261298d565b602082019050919050565b600060208201905081810360008301526129f2816129b6565b9050919050565b7f4552433732313a20746f6b656e20616c7265616479206d696e74656400000000600082015250565b6000612a2f601c83611b93565b9150612a3a826129f9565b602082019050919050565b60006020820190508181036000830152612a5e81612a22565b9050919050565b7f4552433732314d657461646174613a2055524920736574206f66206e6f6e657860008201527f697374656e7420746f6b656e0000000000000000000000000000000000000000602082015250565b6000612ac1602c83611b93565b9150612acc82612a65565b604082019050919050565b60006020820190508181036000830152612af081612ab4565b9050919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b600060088302612b597fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82612b1c565b612b638683612b1c565b95508019841693508086168417925050509392505050565b6000819050919050565b6000612ba0612b9b612b9684611c3a565b612b7b565b611c3a565b9050919050565b6000819050919050565b612bba83612b85565b612bce612bc682612ba7565b848454612b29565b825550505050565b600090565b612be3612bd6565b612bee818484612bb1565b505050565b5b81811015612c1257612c07600082612bdb565b600181019050612bf4565b5050565b601f821115612c5757612c2881612af7565b612c3184612b0c565b81016020851015612c40578190505b612c54612c4c85612b0c565b830182612bf3565b50505b505050565b600082821c905092915050565b6000612c7a60001984600802612c5c565b1980831691505092915050565b6000612c938383612c69565b9150826002028217905092915050565b612cac82611b88565b67ffffffffffffffff811115612cc557612cc4611f65565b5b612ccf825461227f565b612cda828285612c16565b600060209050601f831160018114612d0d5760008415612cfb578287015190505b612d058582612c87565b865550612d6d565b601f198416612d1b86612af7565b60005b82811015612d4357848901518255600182019150602085019450602081019050612d1e565b86831015612d605784890151612d5c601f891682612c69565b8355505b6001600288020188555050505b505050505050565b7f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160008201527f6464726573730000000000000000000000000000000000000000000000000000602082015250565b6000612dd1602683611b93565b9150612ddc82612d75565b604082019050919050565b60006020820190508181036000830152612e0081612dc4565b9050919050565b600081519050919050565b600082825260208201905092915050565b6000612e2e82612e07565b612e388185612e12565b9350612e48818560208601611ba4565b612e5181611bce565b840191505092915050565b6000608082019050612e716000830187611ccf565b612e7e6020830186611ccf565b612e8b6040830185611de5565b8181036060830152612e9d8184612e23565b905095945050505050565b600081519050612eb781611af9565b92915050565b600060208284031215612ed357612ed2611ac3565b5b6000612ee184828501612ea8565b9150509291505056fea26469706673582212205aa3a3145d125b2319b93c6bfcee1131d7e9b6145de5eac2afdfb8b082597d8864736f6c63430008120033"})
            const gas = 30000000; // Set the gas limit to 3000000
            const options = {
              from: accounts[0],
              gas: gas, // Pass the gas limit to the send method
            };

            //arguments to the constructor
            const args = [
              "test",
              "test",
            ]
            const contract = await NFTContract.deploy({
                            arguments: args
                    }).send(options);

            this.contract.address = contract.options.address;

                    
            //store contract address
            await fetch("http://127.0.0.1:8000/get_nft_address/",{
                method: "POST",
                body: JSON.stringify({
                    'address': this.contract.address
                })
            })


            this.contract.instance = new web3.eth.Contract(nftABI, this.contract.address);

            web3.eth.personal.unlockAccount(this.accountInstance, localStorage.getItem('password'), 600);
            //mints a users nft to thier account
            await contract.methods.mint(this.accountInstance, url).send({from: accounts[0]})
            const tokenIds = await contract.methods.tokensOfOwner(this.accountInstance).call()
            this.tokens = tokenIds;
            const uri = await contract.methods.tokenURI(tokenIds[tokenIds.length-1]).call()

            const uploadToken = tokenIds[tokenIds.length-1];
            try{
         

                await contract.methods.transferNFT(this.accountInstance,contract.options.address ,uploadToken)

                const id = contract.methods.ownerOf(tokenIds[tokenIds.length-1]).call()
                Toastify({
               text: id,
               position: "center",
            }).showToast();
            // Toastify({
            //    text: "NFT uploaded "+this.contract.address + "with uri "+uri,
            //    position: "center",
            // }).showToast();
            }
            catch(error){
                Toastify({
               text: " "+this.contract.address + "with uri "+uri,
               position: "center",
            }).showToast();
            }
           
       }


        },

    },
    components: { NFTmint, UserLoanRequests }
};
  </script>

<style>
  #deploy{
    border-style: solid;
    border-radius: 10px;
    background: rgb(0,0,0);
background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(1,221,15,1) 100%, rgba(255,255,255,1) 100%);
    
  }

  #header #contents{
    border-style: solid,

  }

  .button{
    padding-right: 30px;
   
  }

  .forms{
    border-style: solid;
    margin-top: 10px;
    border-radius: 10px;
    border-width: thin;
    width: 500px;
    align-items: center;
    margin-left: 230px;
    

  }
  .information{
    padding: 10px;
    /* position: absolute; */
    margin-top: -70px;
   background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  height: 1000px;

  }

</style>
  