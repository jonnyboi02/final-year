
   <template>
    <div style="color: white;">
    <!-- <div v-if="borrower">
      {{borrower.address}}
    </div> -->
    <h3>Request Loan</h3>
    <!-- <div id = 'header'> -->
      <div id='contents' style="border-style: solid; border-radius: 25px; border-width: thin;">
        <h4> Current Annual Interest rate is {{ form.rate }}%</h4>

      </div>

    <!-- </div> -->
    <div v-if="loanContractAddress " id="deploy" > Contract Deployed at : {{ loanContractAddress }} </div>
    <div style="padding-bottom: 10px; ">
      <!-- form:{
          amount: 100,
          rate: 10,
          duration: 3600,
          collateralAmount: 200,
          collateralHolder: null,
          collateralUrl: " ",
          price: 10,
        } -->
     
        Amount of Loan (in Ethers): <br> <input  v-model="form.amount"/>
        <br>
        <!-- Rate: <br><input  v-model="form.rate"/>
        <br> -->
        Duration: <br>
        <select v-model="currentDuration" @change="durationToSeconds" style="padding-left: 45px;padding-right: 45px;">
          <!--Need to set the form.duration stuff -->
          <option v-for="duration in options" :key="duration" :value= "duration">
            {{ duration }}
          </option>
        </select>

        <!-- Number of months:<br> <input v-model="form.duration"/> -->
        <br>
        Collateral value: <br><input v-model="form.collateralAmount"/>
        <br>
        <!-- Borrower Address: <br><input v-model="form.collateralHolder"/>
        <br> -->
        Desired Price of Contract (in Ethers):<br> <input v-model="form.price"/>
        <br>
        Upload Collateral:
        <br>
        <!-- <button> Upload </button> -->
        <input style="margin-left: 60px;" type="file" @change="handleFileUpload" />



    </div>
    <div style="padding-bottom: 10px; ">       
      <!-- <button class="button"  >Upload NFT</button> -->
      <!-- <button @click="changeOwner" class="button" style="float: right; ">Change Contract Owner</button>
      <button @click="getLoanDetails">Get Contract Details</button>  -->
    </div>

    <div style="padding-bottom: 10px; ">       
      <button @click="deployLoanContract" class="button"  >Deploy smart contract</button>
      <!-- <button @click="changeOwner" class="button" style="float: right; ">Change Contract Owner</button>
      <button @click="getLoanDetails">Get Contract Details</button>  -->
    </div>

    <!-- <button>Generate URL</button> -->
    {{ test }}
    <!-- <div style="padding-bottom: 10px; ">
      <button @click="changeOwner" class="button">Change Contract Owner</button>
    </div> -->
    <div style="padding-bottom: 10px; ">
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
    </div>
  </div>


  </template>
  
  <script>
  import Web3 from 'web3';
  import HelloWorld from './contracts/Test.json';
  import HelloWorldABI from './contracts/HelloWorldABI.json';
  import HelloWorldBytecode from './contracts/HelloWorldBytecode.txt';
  import Toastify from 'toastify-js';
  import 'toastify-js/src/toastify.css';
  

  import LoanABI from './contracts/LoanABI.json'
  import {Buffer } from 'buffer';
  export default {
    mounted(){
      this.getAccounts();
      this.getAddress();
      this.durationToSeconds();
    },
    data() {
      return {
        contractAddress: null,
        loanContractAddress: null,
        loanContractInstance: null,
        loanDetails: null,
        accounts: null,
        borrower: null,
        options: ['3 Months', '6 Months', '1 Year', '2 Years'],
        currentDuration: '3 Months',
        nftFile: null,
        form:{
          amount: 100,
          rate: 3,
          duration: 3600,
          collateralAmount: 200,
          collateralHolder: null,
          collateralUrl: " ",

          //0.5 Ether as default price
          price: 500,
        },
        value: "",
        test: "hi",
      };
    },
    methods: {
      handleFileUpload(event) {
      this.nftFile = event.target.files[0];
    },
      ethToWei(){
        const check = /^[0-9.]+$/;
          if (check.test(this.value)){
            try{
              const weiAmount = Web3.utils.toWei(this.form.amount.toString(), 'ether')/10**3;
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
      },

      durationToSeconds(){
        if (this.currentDuration === '3 Months'){
          this.form.duration = 3*30*24*60*60
        }
        else if (this.currentDuration === '6 Months'){
          this.form.duration = 6*30*24*60*60
        }
        else if (this.currentDuration === '1 Year'){
          this.form.duration = 12*30*24*60*60
        }
        else{
          this.form.duration = 24*30*24*60*60
        }
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
                    this.form.collateralHolder = data.key
                   
                }
            })
          },
      async getAccounts(){
        const web3 = new Web3('http://localhost:8547');
        const accounts = await web3.eth.getAccounts();
        this.accounts = accounts;
      },
      async getLoanDetails(){
        try{
          const web3 = new Web3('http://localhost:8547');
          const accounts = await web3.eth.getAccounts();
        // const web3 = new Web3('http://localhost:8545');
        const LoanContract = new web3.eth.Contract(
          LoanABI,
          this.loanContractAddress,
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

      //used to issue the transaction
      sendTransaction() {
          //checking the data to make sure it is good
          if (this.form.amount===""){
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
     
          if (check.test(this.form.amount)){
            try{
              const weiAmount = Web3.utils.toWei(this.form.amount.toString(), 'ether')/10**3;
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
                  // Toastify({
                  //     text: "Transaction sent successfully!",
                  //     duration: 3000,
                  //     close: true,
                  //     backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                  //     stopOnFocus: true
                  // }).showToast();
              }
            })
                .catch(error => {
                console.error(error);
            });
        },
      async changeOwner(){
          try {
            const web3 = new Web3('http://localhost:8547');
            const accounts = await web3.eth.getAccounts();
          // call changeOwner function
          await this.loanContractInstance.methods.changeOwner(accounts[2]).send({
            from: accounts[0],
            gas: 3000000,
          });
          Toastify({
            text: `Owner Changed to` + accounts[2],
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
        
      },
      async deployLoanContract(){
        
        if (this.form.collateralAmount/this.form.amount<0.75){
          Toastify({
            text: "Please contribute a higher value NFT",
            backgroundColor: 'red',
            position: 'center',
          }).showToast();
          return
        }
        this.sendTransaction();
        const web3 = new Web3('http://localhost:8547');
        const accounts = await web3.eth.getAccounts();
        const networkId = await web3.eth.net.getId();
        const LoanContract = new web3.eth.Contract(
          LoanABI,
          null, 
          { data: '60806040523480156200001157600080fd5b50604051620015df380380620015df833981810160405281019062000037919062000304565b826000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660038190555085600481905550846005819055508360088190555082600960006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600a90805190602001906200016e929190620001b4565b5080600b819055506005544262000186919062000431565b6006819055506000600760006101000a81548160ff02191690831515021790555050505050505050620005f9565b828054620001c29062000502565b90600052602060002090601f016020900481019282620001e6576000855562000232565b82601f106200020157805160ff191683800117855562000232565b8280016001018555821562000232579182015b828111156200023157825182559160200191906001019062000214565b5b50905062000241919062000245565b5090565b5b808211156200026057600081600090555060010162000246565b5090565b60006200027b6200027584620003fe565b620003ca565b9050828152602081018484840111156200029457600080fd5b620002a1848285620004cc565b509392505050565b600081519050620002ba81620005c5565b92915050565b600082601f830112620002d257600080fd5b8151620002e484826020860162000264565b91505092915050565b600081519050620002fe81620005df565b92915050565b600080600080600080600060e0888a0312156200032057600080fd5b6000620003308a828b01620002ed565b9750506020620003438a828b01620002ed565b9650506040620003568a828b01620002ed565b9550506060620003698a828b01620002ed565b94505060806200037c8a828b01620002a9565b93505060a088015167ffffffffffffffff8111156200039a57600080fd5b620003a88a828b01620002c0565b92505060c0620003bb8a828b01620002ed565b91505092959891949750929550565b6000604051905081810181811067ffffffffffffffff82111715620003f457620003f362000596565b5b8060405250919050565b600067ffffffffffffffff8211156200041c576200041b62000596565b5b601f19601f8301169050602081019050919050565b60006200043e82620004c2565b91506200044b83620004c2565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0382111562000483576200048262000538565b5b828201905092915050565b60006200049b82620004a2565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b83811015620004ec578082015181840152602081019050620004cf565b83811115620004fc576000848401525b50505050565b600060028204905060018216806200051b57607f821691505b6020821081141562000532576200053162000567565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620005d0816200048e565b8114620005dc57600080fd5b50565b620005ea81620004c2565b8114620005f657600080fd5b50565b610fd680620006096000396000f3fe6080604052600436106100fe5760003560e01c80638da5cb5b11610095578063a6f9dae111610064578063a6f9dae1146102ef578063aa8c217c14610318578063bcead63e14610343578063e27facdc1461036e578063f966ade714610399576100fe565b80638da5cb5b1461023857806392d09ceb14610263578063a035b1fe1461028e578063a3b9e39d146102b9576100fe565b806357f7d74f116100d157806357f7d74f1461018e5780636164051a146101b7578063786716fe146101e25780637df1f1b91461020d576100fe565b80630b168f21146101035780630fb5a6b41461012e5780632c4e722e14610159578063330aec3e14610184575b600080fd5b34801561010f57600080fd5b506101186103a3565b6040516101259190610ca4565b60405180910390f35b34801561013a57600080fd5b50610143610431565b6040516101509190610d26565b60405180910390f35b34801561016557600080fd5b5061016e610437565b60405161017b9190610d26565b60405180910390f35b61018c61043d565b005b34801561019a57600080fd5b506101b560048036038101906101b09190610a5e565b610583565b005b3480156101c357600080fd5b506101cc610608565b6040516101d99190610c89565b60405180910390f35b3480156101ee57600080fd5b506101f761061b565b6040516102049190610d26565b60405180910390f35b34801561021957600080fd5b50610222610621565b60405161022f9190610bad565b60405180910390f35b34801561024457600080fd5b5061024d610645565b60405161025a9190610bad565b60405180910390f35b34801561026f57600080fd5b5061027861066b565b6040516102859190610d26565b60405180910390f35b34801561029a57600080fd5b506102a3610671565b6040516102b09190610d26565b60405180910390f35b3480156102c557600080fd5b506102ce610677565b6040516102e69c9b9a99989796959493929190610bc8565b60405180910390f35b3480156102fb57600080fd5b5061031660048036038101906103119190610a5e565b6107eb565b005b34801561032457600080fd5b5061032d61082f565b60405161033a9190610d26565b60405180910390f35b34801561034f57600080fd5b50610358610835565b6040516103659190610bad565b60405180910390f35b34801561037a57600080fd5b5061038361085b565b6040516103909190610bad565b60405180910390f35b6103a1610881565b005b600a80546103b090610eb9565b80601f01602080910402602001604051908101604052809291908181526020018280546103dc90610eb9565b80156104295780601f106103fe57610100808354040283529160200191610429565b820191906000526020600020905b81548152906001019060200180831161040c57829003601f168201915b505050505081565b60055481565b60045481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146104cb576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104c290610d06565b60405180910390fd5b60646004546003546104dd9190610de4565b6104e79190610db3565b6003546104f49190610d5d565b3410610516576001600760006101000a81548160ff0219169083151502179055505b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc6008549081150290604051600060405180830381858888f19350505050158015610580573d6000803e3d6000fd5b50565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600760009054906101000a900460ff1681565b60065481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60085481565b600b5481565b600080600080600080600080600080606060008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600354600454600554600654600760009054906101000a900460ff16600854600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600a600b5481805461074590610eb9565b80601f016020809104026020016040519081016040528092919081815260200182805461077190610eb9565b80156107be5780601f10610793576101008083540402835291602001916107be565b820191906000526020600020905b8154815290600101906020018083116107a157829003601f168201915b505050505091509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60035481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600760009054906101000a900460ff16156108d1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108c890610cc6565b60405180910390fd5b60065442111561095657600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc600854476109259190610d5d565b9081150290604051600060405180830381858888f19350505050158015610950573d6000803e3d6000fd5b50610a47565b60646004546003546109689190610de4565b6109729190610db3565b60035461097f9190610d5d565b34146109c0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109b790610ce6565b60405180910390fd5b6001600760006101000a81548160ff021916908315150217905550600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc6008549081150290604051600060405180830381858888f19350505050158015610a45573d6000803e3d6000fd5b505b565b600081359050610a5881610f89565b92915050565b600060208284031215610a7057600080fd5b6000610a7e84828501610a49565b91505092915050565b610a9081610e3e565b82525050565b610a9f81610e50565b82525050565b6000610ab082610d41565b610aba8185610d4c565b9350610aca818560208601610e86565b610ad381610f78565b840191505092915050565b6000610aeb601683610d4c565b91507f4c6f616e20697320616c726561647920726570616964000000000000000000006000830152602082019050919050565b6000610b2b601a83610d4c565b91507f496e636f72726563742072657061796d656e7420616d6f756e740000000000006000830152602082019050919050565b6000610b6b602083610d4c565b91507f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e746000830152602082019050919050565b610ba781610e7c565b82525050565b6000602082019050610bc26000830184610a87565b92915050565b600061018082019050610bde600083018f610a87565b610beb602083018e610a87565b610bf8604083018d610a87565b610c05606083018c610b9e565b610c12608083018b610b9e565b610c1f60a083018a610b9e565b610c2c60c0830189610b9e565b610c3960e0830188610a96565b610c47610100830187610b9e565b610c55610120830186610a87565b818103610140830152610c688185610aa5565b9050610c78610160830184610b9e565b9d9c50505050505050505050505050565b6000602082019050610c9e6000830184610a96565b92915050565b60006020820190508181036000830152610cbe8184610aa5565b905092915050565b60006020820190508181036000830152610cdf81610ade565b9050919050565b60006020820190508181036000830152610cff81610b1e565b9050919050565b60006020820190508181036000830152610d1f81610b5e565b9050919050565b6000602082019050610d3b6000830184610b9e565b92915050565b600081519050919050565b600082825260208201905092915050565b6000610d6882610e7c565b9150610d7383610e7c565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115610da857610da7610eeb565b5b828201905092915050565b6000610dbe82610e7c565b9150610dc983610e7c565b925082610dd957610dd8610f1a565b5b828204905092915050565b6000610def82610e7c565b9150610dfa83610e7c565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0483118215151615610e3357610e32610eeb565b5b828202905092915050565b6000610e4982610e5c565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b83811015610ea4578082015181840152602081019050610e89565b83811115610eb3576000848401525b50505050565b60006002820490506001821680610ed157607f821691505b60208210811415610ee557610ee4610f49565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000601f19601f8301169050919050565b610f9281610e3e565b8114610f9d57600080fd5b5056fea2646970667358221220092a4520ee5d889387f2715b1f07f2c3a2780332b402ab50e8cb9ea45bb73aed64736f6c63430008000033'}
        );
        const gas = 3000000; // Set the gas limit to 3000000
        const options = {
          from: accounts[0],
          gas: gas, // Pass the gas limit to the send method
        };

        
        var account = null;
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
                    this.form.collateralHolder = data.key
                    for (let i = 0; i < accounts.length; i++) {

                      if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(data.key.toLowerCase())) {
                        this.form.collateralHolder = accounts[i];
                        break;
                      }
                    }
                    
                    //this.senderPassword = localStorage.getItem('password')
                }
            });
        
        for (let i = 0; i < accounts.length; i++) {
          if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(this.form.collateralHolder.toLowerCase())) {
            this.form.collateralHolder = accounts[i]
            account = accounts[i];
          //   Toastify({
          //   text: account ,
          //   backgroundColor: 'green',
          //   position: 'center',
          // }).showToast();
          await this.generateURL();
            const args = [
              this.form.amount, // amount
              this.form.rate, // rate
              this.form.duration, // duration
              this.form.collateralAmount, // collateralAmount
              this.form.collateralHolder, // collateralHolder
              this.form.collateralUrl, 
              this.form.price,
            ];

        try{

          //deploys the smart contract
          const contract = await LoanContract.deploy({
            arguments: args
          }).send(options);
          
          this.loanContractAddress = contract.options.address;
          this.loanContractInstance = new web3.eth.Contract(
            LoanABI, 
            this.loanContractAddress,
          ) 
          const response= fetch("http://127.0.0.1:8000/contracts/",{
            method: "PUT", 
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'address': this.loanContractAddress, 
                }),

          })

          // this.test=this.generateURL();
          // this.generateURL();
          //read in the collateral
          const fileReader = new FileReader();
          // const buffer = await new Promise((resolve) => {
          //   fileReader.onload = (event) => (Buffer.from(event.target.result));
          //   fileReader.readAsArrayBuffer(this.nftFile);
          // });

          // const result = await this.loanContractInstance.methods.mint(accounts[0], buffer).send({from: accounts[0]});

        
          // this.test = await JSON.Stringify(this.loanContractInstance.methods.ownerOf(0).call());

          //displays the message for a contract that has been deployed
          Toastify({
            text: `Deployed loan contract ` + this.loanContractAddress +" "+ this.form.collateralHolder ,
            backgroundColor: 'green',
            position: 'center',
          }).showToast();

        } catch(error){
          Toastify({
            text: `Error deploying contract: ${error}` + this.form.collateralHoldercollateralHolder,
            backgroundColor: 'red',
            position: 'center',
          }).showToast();

        }
            break;
          }
        }

      },
      async generateURL() {
        const formData = new FormData();
        formData.append("file", this.nftFile);
        const response = await fetch("http://localhost:8000/generate-url/", {
          method: "POST",
          body: formData
        });
        const data = await response.json();
        this.test = data.url;
        this.form.collateralUrl = data.url;
    }


     
    },
  };
  </script>

<style>
  #deploy{
    border-style: solid;
    border-radius: 25px;
    background: rgb(0,0,0);
background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(1,221,15,1) 100%, rgba(255,255,255,1) 100%);
    
  }

  #header #contents{
    border-style: solid,

  }

  .button{
    padding-right: 30px;
   
  }

</style>
  