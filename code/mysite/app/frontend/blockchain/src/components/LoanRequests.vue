<template>
    <div id='details'>
      <h2 style="color: white;">Loan Requests</h2>
      <div class="requests">
        <div class="request-list">
          <h2>Waiting Loans</h2>
          <nav id="lists" style=" padding-top: 10px;">
            <ul v-if="waitingLoans && waitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in waitingLoans" :key="lender" :value="lender" @click="selectWaitItem(index)" style="padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;  ">
                    {{  lender.collateralHolder }} Loan {{ lender.id }}
                </li>
              </div>
            </ul>
           
          </nav>

        </div>
        <div class="request-list">
          <h2>Non-waiting Loans</h2>
          <nav id="lists" style=" padding-top: 10px;">
            <ul v-if="nonWaitingLoans && nonWaitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in nonWaitingLoans" :key="lender" :value="lender" @click="selectNonWaitItem(index)" style="padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; ">
                  {{  lender.collateralHolder }} Loan {{ lender.id }}
                </li>
              </div>
            </ul>
           
          </nav>
        </div>
      </div>
      <div v-if="loanRequest" id="loanDetails">
        <h2>Loan Request Details</h2>
        <div>ID: {{ loanRequest.id }}</div>
        <div>Loan Requested: {{ loanRequest.amount }} ETH</div>
        <div>Loan Duration: {{ loanRequest.duration / 86400 }} Days</div>
        <div>APR Rate: {{ loanRequest.rate }}%</div>
        <div v-if="loanRequest.collateralValue">Collateral Value: {{ loanRequest.collateralValue }} ETH</div>
        <div v-if="loanRequest.collateralHolder">Collateral Holder: {{ loanRequest.collateralHolder }}</div>
        <div v-if="loanRequest.collateralURL">Collateral URL: {{ loanRequest.collateralURL }}</div>
        <div>Loan Approved: {{ loanRequest.loanApproved ? "Yes" : "No" }}</div>
        <div>Loan Waiting: {{ loanRequest.loanWaiting ? "Yes": "No" }}</div>
        <div>Sale Price: {{ loanRequest.price }}  ETH</div>
        <div>Request Time: {{ loanRequest.request_time ?  `${new Date(loanRequest.request_time).toLocaleDateString('en-US')} ${new Date(loanRequest.request_time).toLocaleTimeString('en-US', {hour12: false})}`: `${loanRequest.request_time.toLocaleDateString('en-US')} ${loanRequest.request_time.toLocaleTimeString('en-US', {hour12: false})}`}}</div>
        <div>
            <button v-if="loanRequest.loanWaiting" class = 'buttons' @click="acceptLoan">Approve Loan</button>
            <button v-if='loanRequest.loanWaiting' class = 'buttons'  @click="rejectLoan">Reject Loan</button>
            <button class = 'buttons' @click="viewNFT">View NFT</button>
        </div>

        {{ tokens }}
        {{ uri }}
      </div>
      <div v-else id="loanDetails">
        <h2>Select on a loan to view the details of.</h2>
      </div>

      <div id="">
        <h2>NFT requests</h2>
        <div class="requests">
        <div class="request-list">
          <h2>Asset Evaluations</h2>
          <nav id="lists" style=" padding-top: 10px;">
            <ul v-if="negotiations && negotiations.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(negotiation, index) in negotiations" :key="lender" :value="lender" @click="selectNFTrequest(index)" style="padding: 2px; border-style: solid; border-radius: 10px; padding-left: 10px; padding-right: 15px;  ">
                    ID: {{  negotiation.id }} NFT request {{ negotiation.user }}
                </li>
              </div>
            </ul>
           
          </nav>

        </div>
        <div class="request-list">
          <h2>Details</h2>
          
          <div v-if="currentNegotiation">
            <p>Request ID: {{ currentNegotiation.id }}</p>
            <p> Requester: {{ currentNegotiation.user }}</p>   
            <p>Picture:  </p>
            <img v-if="currentNegotiation.photo" :src="'http://localhost:8000/media/' + currentNegotiation.photo" :alt="currentNegotiation.description" style="width:200px; height: 200px ">
            <p> NFTs requested: {{ currentNegotiation.amount }}</p>
            <p> Description: {{ currentNegotiation.description }}</p>
            <p>Agreed? {{ currentNegotiation.accepted ? "Yes" : "No" }}</p>
            <button v-if="!currentNegotiation.accepted" style="margin-right: 10px;" @click="acceptAsset">Accept Asset</button>
            <button  v-if="!currentNegotiation.accepted" style="margin-right: 10px; margin-bottom: 10px;">Reject Asset</button>
            
            <button v-if="currentNegotiation.accepted" @click="viewConditions" >View Conditions</button>
          </div>
          <div v-else>
            Select an Asset Evaluation.
          </div>
          <!-- <nav id="lists" style=" padding-top: 10px;">
            <ul v-if="nonWaitingLoans && nonWaitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in nonWaitingLoans" :key="lender" :value="lender" @click="selectNonWaitItem(index)" style="padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; ">
                  {{  lender.collateralHolder }} Loan {{ lender.id }}
                </li>
              </div>
            </ul>
           
          </nav> -->
        </div>
      </div>

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
  export default {
    data() {
      return {
        waitingLoans: [],
        nonWaitingLoans: [],
        loanRequest: null,
        index: 0,
        loanRequest: null,
        form:{
            amount: null,
            rate: null,
            duration: null,
            collateralAmount: null,
            collateralHolder: null,
            collateralUrl: null,
            price: null,
        },
        contract:{
            instance: null,
            address: null,
        },
        tokens: null,
        uri: null,
        loanContractAddress: null,
        loanContractInstance: null,
        negotiations: [],
        currentNegotiation: null,
        negotiationIndex: 0,
      };
    },
    async mounted() {
      await this.getLoans();
      await this.getNegotiations();
    },
    methods: {
      viewConditions(){
      window.location.href = "http://localhost:8000/media/" + this.currentNegotiation.conditions;
    },
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
        let NFTurl = await NFTcontract.methods.tokenURI(this.loanRequest.collateralURL).call()
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
      async acceptAsset(){
                const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
                let data = await req.json()
                this.contract.address = data.address
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                var contract = new web3.eth.Contract(nftABI, this.contract.address);
                var currentConditions = this.currentNegotiation;
                await web3.eth.personal.unlockAccount(currentConditions.user, currentConditions.password, 600);
                
                var negotiationId = currentConditions.id
                try{

                  //creates the contract
                  let response = await fetch("http://127.0.0.1:8000/create_conditions/",{
                    method: "POST",
                    body: new URLSearchParams({
                      negotiation_id: negotiationId,
                     })
                  })

                  let data = await response.json()
                  let url = data.file_url
                  for (let i = 0; i<currentConditions.amount; i++){
                    await contract.methods.mint(currentConditions.user, url).send({from: accounts[0]});
                  }

                  
                  //refreshes the negotititaions
                 await this.getNegotiations();
                 //updates selected one
                 this.currentNegotiation = this.negotiations[negotiationId-1]
                  Toastify({
                        text: "This user has NFTs: "+ await contract.methods.tokensOfOwner(currentConditions.user).call(),
                        duration: 3000,
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        stopOnFocus: true
                    }).showToast();
                 // await this.getNegotiations();

                  


                }catch(error){
                  console.log(error)
                }
      },

        selectNFTrequest(index){
          this.currentNegotiation = this.negotiations[index];
          this.negotiationIndex = index;
        },
        async getNegotiations(){
          fetch('http://127.0.0.1:8000/get_negotiations/')
            .then(response => response.json())
            .then(data => {
              this.negotiations = data;
            })
            .catch(error => console.log(error));

            console.log(this.negotiations.length)
        },

        async rejectLoan(){
                var account = this.loanRequest.collateralHolder
                //gets the address of the nft contract
                const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
                let data = await req.json()
                this.contract.address = data.address
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();

                //links to the deployed nft contract
                var contract = new web3.eth.Contract(nftABI, this.contract.address);
                this.contract.instance = contract;

                //let curToken = parseInt(this.loanRequest.collateralUrl)
                let tokens = await contract.methods.tokensOfOwner(this.loanRequest.collateralHolder).call()
                //console.log(await contract.methods.ownerOf(curToken).call())
                for (let i =0;i< tokens.length; i++){
                  let token = tokens[i];
                  console.log(token)
                  if (JSON.stringify(token) === JSON.stringify(this.loanRequest.collateralURL)){
                    console.log("transferred back!")
                    await web3.eth.personal.unlockAccount(accounts[0], "123456789", 600);

                    await contract.methods.transferFrom(accounts[0],account, token).send({from: accounts[0]})
                    try{
                      console.log( await contract.methods.ownerOf(token));
                    }catch(error){
                      console.log(error)
                    }
                    // console.log( await contract.methods.ownerOf(token));
                    console.log("hi")
                    break;
                  }
                }
                let  tokenIds = await contract.methods.tokensOfOwner(accounts[0]).call()
                // tokenIds = await contract.methods.tokensOfOwner(accounts[0]).call()
                // console.log(tokens);
                // //console.log(tokenIds);
                // console.log(data.address);
                // console.log(contract.options.address);

            try{
                // let response = await fetch("http://127.0.0.1:8000/reject_loan/", {
                //     method: 'POST',
                //     body: JSON.stringify({
                //         'id':this.loanRequest.id
                //     })
                // })
                // let data = await response.json()
                //this.$router.go(0)

                // console.log("hey")
            }catch(error){
                console.log(error)
            }

        },

        async sendTransaction(){
          const check = /^[0-9.]+$/;
          var value = null;
          const web3 = new Web3("http://localhost:8547");
          const accounts = await web3.eth.getAccounts();
            if (check.test(this.form.amount)) {
                try {
                    const weiAmount = Web3.utils.toWei(this.form.amount.toString(), "ether") / (Math.pow(10, 3));
                    const weiAmountWithPrefix = "0x" + weiAmount;
                    value = weiAmountWithPrefix;
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
                sender_address: accounts[0],
                sender_password: "123456789",
                recipient_address: this.form.collateralHolder,
                value: value,
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
                        text: "Insuffient funds"+value,
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
        async uploadNFT(){
            try{
                let url = this.loanRequest.collateralURL
                var account = this.loanRequest.collateralHolder
                //gets the address of the nft contract
                const req = await fetch("http://127.0.0.1:8000/get_nft_address/");
                let data = await req.json()
                this.contract.address = data.address
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();

                var contract = new web3.eth.Contract(nftABI, this.contract.address);
                this.contract.instance = contract;
                // await contract.methods.mint(account, url).send({from: accounts[0]})
                const tokenIds = await contract.methods.tokensOfOwner(account).call()
                this.tokens = tokenIds;

                const uri = await contract.methods.tokenURI(url).call()
                this.uri = uri

            
                // Toastify({
                // text:await contract.methods.ownerOf(url).call(),
                // position: "center",
                // }).showToast();
                //await web3.eth.personal.unlockAccount(account, localStorage.getItem('password'), 600);
               

                //let d = await contract.methods.transferFrom(account,contract.options.address ,tokenIds[tokenIds.length-1]) .send({from: account})

                Toastify({
                text: "NFT uploaded "+this.contract.address + "with uri "+uri,
                position: "center",
                backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)",
                }).showToast();
            }catch(error){
                console.log(error)
                Toastify({
                text: error + contract.options.address,
                position: "center",
                }).showToast();
            }
        },
        async acceptLoan(){
            const check = await fetch("http://127.0.0.1:8000/get_nft_length/")
            const checkData = await check.json()
            if (checkData.length === '1'){ 
                await this.uploadNFT();
                //return;
            }


            // const check = await fetch("http://127.0.0.1:8000/get_nft_length/")
            // const checkData = await check.json()

            //gets the url of the propsed collateral
               



            
            //sets the parameters to what should be sent to the contract
            this.form.amount = this.loanRequest.amount
            this.form.rate= this.loanRequest.rate
            this.form.duration= this.loanRequest.duration
            this.form.collateralHolder= this.loanRequest.collateralHolder
            this.form.collateralAmount = this.loanRequest.collateralValue
            this.form.collateralUrl= this.loanRequest.collateralURL
            this.form.price= this.loanRequest.price

            
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const networkId = await web3.eth.net.getId();
            
            this.sendTransaction();

            const LoanContract = new web3.eth.Contract(LoanABI, null, { data: "60806040523480156200001157600080fd5b5060405162001656380380620016568339818101604052810190620000379190620003e8565b826000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660038190555085600481905550846005819055508360088190555082600960006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600a9081620001679190620006fb565b5080600b81905550600554426200017f919062000811565b6006819055506000600760006101000a81548160ff0219169083151502179055506000600c81905550505050505050506200084c565b6000604051905090565b600080fd5b600080fd5b6000819050919050565b620001de81620001c9565b8114620001ea57600080fd5b50565b600081519050620001fe81620001d3565b92915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000620002318262000204565b9050919050565b620002438162000224565b81146200024f57600080fd5b50565b600081519050620002638162000238565b92915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620002be8262000273565b810181811067ffffffffffffffff82111715620002e057620002df62000284565b5b80604052505050565b6000620002f5620001b5565b9050620003038282620002b3565b919050565b600067ffffffffffffffff82111562000326576200032562000284565b5b620003318262000273565b9050602081019050919050565b60005b838110156200035e57808201518184015260208101905062000341565b60008484015250505050565b6000620003816200037b8462000308565b620002e9565b905082815260208101848484011115620003a0576200039f6200026e565b5b620003ad8482856200033e565b509392505050565b600082601f830112620003cd57620003cc62000269565b5b8151620003df8482602086016200036a565b91505092915050565b600080600080600080600060e0888a0312156200040a5762000409620001bf565b5b60006200041a8a828b01620001ed565b97505060206200042d8a828b01620001ed565b9650506040620004408a828b01620001ed565b9550506060620004538a828b01620001ed565b9450506080620004668a828b0162000252565b93505060a088015167ffffffffffffffff8111156200048a5762000489620001c4565b5b620004988a828b01620003b5565b92505060c0620004ab8a828b01620001ed565b91505092959891949750929550565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b600060028204905060018216806200050d57607f821691505b602082108103620005235762000522620004c5565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026200058d7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff826200054e565b6200059986836200054e565b95508019841693508086168417925050509392505050565b6000819050919050565b6000620005dc620005d6620005d084620001c9565b620005b1565b620001c9565b9050919050565b6000819050919050565b620005f883620005bb565b620006106200060782620005e3565b8484546200055b565b825550505050565b600090565b6200062762000618565b62000634818484620005ed565b505050565b5b818110156200065c57620006506000826200061d565b6001810190506200063a565b5050565b601f821115620006ab57620006758162000529565b62000680846200053e565b8101602085101562000690578190505b620006a86200069f856200053e565b83018262000639565b50505b505050565b600082821c905092915050565b6000620006d060001984600802620006b0565b1980831691505092915050565b6000620006eb8383620006bd565b9150826002028217905092915050565b6200070682620004ba565b67ffffffffffffffff81111562000722576200072162000284565b5b6200072e8254620004f4565b6200073b82828562000660565b600060209050601f8311600181146200077357600084156200075e578287015190505b6200076a8582620006dd565b865550620007da565b601f198416620007838662000529565b60005b82811015620007ad5784890151825560018201915060208501945060208101905062000786565b86831015620007cd5784890151620007c9601f891682620006bd565b8355505b6001600288020188555050505b505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006200081e82620001c9565b91506200082b83620001c9565b9250828201905080821115620008465762000845620007e2565b5b92915050565b610dfa806200085c6000396000f3fe6080604052600436106101025760003560e01c80638da5cb5b11610095578063a6f9dae111610064578063a6f9dae1146103f0578063aa8c217c14610419578063bcead63e14610444578063d524b0ff1461046f578063e27facdc1461049a576101ff565b80638da5cb5b1461033957806392d09ceb14610364578063a035b1fe1461038f578063a3b9e39d146103ba576101ff565b806357f7d74f116100d157806357f7d74f1461028f5780636164051a146102b8578063786716fe146102e35780637df1f1b91461030e576101ff565b80630b168f21146102045780630fb5a6b41461022f5780632c4e722e1461025a578063330aec3e14610285576101ff565b366101ff57600760009054906101000a900460ff1615610157576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161014e90610983565b60405180910390fd5b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146101e5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101dc906109ef565b60405180910390fd5b34600c60008282546101f79190610a48565b925050819055005b600080fd5b34801561021057600080fd5b506102196104c5565b6040516102269190610afb565b60405180910390f35b34801561023b57600080fd5b50610244610553565b6040516102519190610b2c565b60405180910390f35b34801561026657600080fd5b5061026f610559565b60405161027c9190610b2c565b60405180910390f35b61028d61055f565b005b34801561029b57600080fd5b506102b660048036038101906102b19190610baa565b610641565b005b3480156102c457600080fd5b506102cd6106c6565b6040516102da9190610bf2565b60405180910390f35b3480156102ef57600080fd5b506102f86106d9565b6040516103059190610b2c565b60405180910390f35b34801561031a57600080fd5b506103236106df565b6040516103309190610c1c565b60405180910390f35b34801561034557600080fd5b5061034e610703565b60405161035b9190610c1c565b60405180910390f35b34801561037057600080fd5b50610379610729565b6040516103869190610b2c565b60405180910390f35b34801561039b57600080fd5b506103a461072f565b6040516103b19190610b2c565b60405180910390f35b3480156103c657600080fd5b506103cf610735565b6040516103e79c9b9a99989796959493929190610c37565b60405180910390f35b3480156103fc57600080fd5b5061041760048036038101906104129190610baa565b61088a565b005b34801561042557600080fd5b5061042e6108ce565b60405161043b9190610b2c565b60405180910390f35b34801561045057600080fd5b506104596108d4565b6040516104669190610c1c565b60405180910390f35b34801561047b57600080fd5b506104846108fa565b6040516104919190610b2c565b60405180910390f35b3480156104a657600080fd5b506104af610900565b6040516104bc9190610c1c565b60405180910390f35b600a80546104d290610d27565b80601f01602080910402602001604051908101604052809291908181526020018280546104fe90610d27565b801561054b5780601f106105205761010080835404028352916020019161054b565b820191906000526020600020905b81548152906001019060200180831161052e57829003601f168201915b505050505081565b60055481565b60045481565b600034116105a2576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161059990610da4565b60405180910390fd5b34600c60008282546105b49190610a48565b92505081905550600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc479081150290604051600060405180830381858888f19350505050158015610623573d6000803e3d6000fd5b506001600760006101000a81548160ff021916908315150217905550565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600760009054906101000a900460ff1681565b60065481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60085481565b600b5481565b60008060008060008060008060006060600080600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600354600454600554600654600760009054906101000a900460ff16600854600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600a600b54600c548280546107e490610d27565b80601f016020809104026020016040519081016040528092919081815260200182805461081090610d27565b801561085d5780601f106108325761010080835404028352916020019161085d565b820191906000526020600020905b81548152906001019060200180831161084057829003601f168201915b505050505092509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60035481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600c5481565b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600082825260208201905092915050565b7f4c6f616e20697320616c72656164792072657061696400000000000000000000600082015250565b600061096d601683610926565b915061097882610937565b602082019050919050565b6000602082019050818103600083015261099c81610960565b9050919050565b7f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e74600082015250565b60006109d9602083610926565b91506109e4826109a3565b602082019050919050565b60006020820190508181036000830152610a08816109cc565b9050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000610a5382610a0f565b9150610a5e83610a0f565b9250828201905080821115610a7657610a75610a19565b5b92915050565b600081519050919050565b60005b83811015610aa5578082015181840152602081019050610a8a565b60008484015250505050565b6000601f19601f8301169050919050565b6000610acd82610a7c565b610ad78185610926565b9350610ae7818560208601610a87565b610af081610ab1565b840191505092915050565b60006020820190508181036000830152610b158184610ac2565b905092915050565b610b2681610a0f565b82525050565b6000602082019050610b416000830184610b1d565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610b7782610b4c565b9050919050565b610b8781610b6c565b8114610b9257600080fd5b50565b600081359050610ba481610b7e565b92915050565b600060208284031215610bc057610bbf610b47565b5b6000610bce84828501610b95565b91505092915050565b60008115159050919050565b610bec81610bd7565b82525050565b6000602082019050610c076000830184610be3565b92915050565b610c1681610b6c565b82525050565b6000602082019050610c316000830184610c0d565b92915050565b600061018082019050610c4d600083018f610c0d565b610c5a602083018e610c0d565b610c67604083018d610b1d565b610c74606083018c610b1d565b610c81608083018b610b1d565b610c8e60a083018a610b1d565b610c9b60c0830189610be3565b610ca860e0830188610b1d565b610cb6610100830187610c0d565b818103610120830152610cc98186610ac2565b9050610cd9610140830185610b1d565b610ce7610160830184610b1d565b9d9c50505050505050505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680610d3f57607f821691505b602082108103610d5257610d51610cf8565b5b50919050565b7f56616c7565206d7573742062652067726561746572207468616e203000000000600082015250565b6000610d8e601c83610926565b9150610d9982610d58565b602082019050919050565b60006020820190508181036000830152610dbd81610d81565b905091905056fea26469706673582212204128b9814fe8d1a7140210d55c2b745348d3aba4021ac860e96517f276c2cfca64736f6c63430008120033" });

            const gas = 3000000; // Set the gas limit to 3000000
            // const options = {
            //     from: accounts[0],
            //     gas: gas, // Pass the gas limit to the send method
            // };

            const args = [
                this.form.amount,
                Math.trunc(this.form.rate*100),
                this.form.duration,
                this.form.collateralAmount,
                this.form.collateralHolder,
                this.form.collateralUrl,
                this.form.price
            ]

            const options = {
                from: accounts[0],
                gas: gas, // Pass the gas limit to the send method
            };

            try { 
                //deploys the smart contract
                // Toastify({
                //             text: 'Deploying for '+this.form.collateralHolder,
                //             backgroundColor: "green",
                //             position: "center",
                //         }).showToast();
                        const contract = await LoanContract.deploy({
                            arguments: args
                        }).send(options);
                        
                        
                        this.loanContractAddress = contract.options.address;
                        this.loanContractInstance = new web3.eth.Contract(LoanABI, this.loanContractAddress);
                        const response = fetch("http://127.0.0.1:8000/contracts/", {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                "address": this.loanContractAddress,
                            }),
                        });

                        //const fileReader = new FileReader();
  
                        Toastify({
                            text: `Deployed loan contract address: ` + this.loanContractAddress + " for " + this.form.collateralHolder,
                            backgroundColor:  "linear-gradient(to right, #00b09b, #96c93d)",
                            position: "center",
                        }).showToast();
                    }
                    catch (error) {
                        Toastify({
                            text: `Error deploying contract: ${error}` + this.form.collateralHolder,
                            backgroundColor: "red",
                            position: "center",
                        }).showToast();
                    }
            
            // return;
                    
            let response = await fetch("http://127.0.0.1:8000/accept_loan/", {
                    method: 'POST',
                    body: JSON.stringify({
                        'id':this.loanRequest.id
                    })
            })

            let data = await response.json()
        

        },
        selectWaitItem(index){
            this.index = index;
            this.loanRequest =  this.waitingLoans[index]
        },
        selectNonWaitItem(index){
            this.index = index;
            this.loanRequest =  this.nonWaitingLoans[index]

        },
      async getLoans() {
        try {
          const response = await fetch("http://127.0.0.1:8000/request_loan/");
          const data = await response.json();
          this.waitingLoans = data.filter((loan) => loan.loanWaiting);
          this.nonWaitingLoans = data.filter((loan) => !loan.loanWaiting);
        } catch (error) {
          console.error(error);
        }
      },
      //sets the loan to be approved
      async approveLoan(){
        let id = this.loanRequest.id

      },
    },
  };
  </script>
  
  <style>
  .requests {
    display: flex;
    justify-content: space-between;
  }
  
  .request-list {
    width: 370px;
    border: 1px solid white;
    padding: 10px;
    border-radius: 10px;

  }

  #lists{
    height:200px;
    width:101%;
    overflow:hidden; 
    overflow-y:scroll;
    color: white;
}
#details{
    color: white;
   background: rgba(0,0,0,.6);
    box-sizing: border-box;
    box-shadow: 0 15px 10px rgba(0,0,0,.6);
    border-radius: 10px;
    padding: 10px;
    margin-top: -70px;
  
}

#loanDetails{
    border-style: solid;
    border-color: white;
    margin-top: 15px;
    border-radius: 10px;
    border-width: thin;
}

.buttons{
    margin-right: 10px;
    padding: 10px;
}
  </style>
  