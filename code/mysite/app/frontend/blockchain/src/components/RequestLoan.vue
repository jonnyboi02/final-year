
   <template>
    <!-- <NFTmint/> -->
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
  import Toastify from 'toastify-js';
  import 'toastify-js/src/toastify.css';
  import nftABI from './contracts/MyNFT.json'

  import LoanABI from './contracts/LoanABI.json'
  import {Buffer } from 'buffer';
import NFTmint from './NFTmint.vue';
  export default {
    mounted() {
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
            options: ["3 Months", "6 Months", "1 Year", "2 Years"],
            currentDuration: "3 Months",
            nftFile: null,
            form: {
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
            accountInstance: "",
            contract:{
              address: "",
              instance: "",
            },
            tokens:[],
        };
    },
    methods: {
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
                }
            });
        },
        async getAccounts() {
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            this.accounts = accounts;
        },
        async getLoanDetails() {
            try {
                const web3 = new Web3("http://localhost:8547");
                const accounts = await web3.eth.getAccounts();
                // const web3 = new Web3('http://localhost:8545');
                const LoanContract = new web3.eth.Contract(LoanABI, this.loanContractAddress);
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
                else {
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
        async deployLoanContract() {
            if (this.form.collateralAmount / this.form.amount < 0.75) {
                Toastify({
                    text: "Please contribute a higher value NFT",
                    backgroundColor: "red",
                    position: "center",
                }).showToast();
                return;
            }
            //sends the funds
            this.sendTransaction();

            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const networkId = await web3.eth.net.getId();
            const LoanContract = new web3.eth.Contract(LoanABI, null, { data: "60806040523480156200001157600080fd5b50604051620015df380380620015df833981810160405281019062000037919062000304565b826000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660038190555085600481905550846005819055508360088190555082600960006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600a90805190602001906200016e929190620001b4565b5080600b819055506005544262000186919062000431565b6006819055506000600760006101000a81548160ff02191690831515021790555050505050505050620005f9565b828054620001c29062000502565b90600052602060002090601f016020900481019282620001e6576000855562000232565b82601f106200020157805160ff191683800117855562000232565b8280016001018555821562000232579182015b828111156200023157825182559160200191906001019062000214565b5b50905062000241919062000245565b5090565b5b808211156200026057600081600090555060010162000246565b5090565b60006200027b6200027584620003fe565b620003ca565b9050828152602081018484840111156200029457600080fd5b620002a1848285620004cc565b509392505050565b600081519050620002ba81620005c5565b92915050565b600082601f830112620002d257600080fd5b8151620002e484826020860162000264565b91505092915050565b600081519050620002fe81620005df565b92915050565b600080600080600080600060e0888a0312156200032057600080fd5b6000620003308a828b01620002ed565b9750506020620003438a828b01620002ed565b9650506040620003568a828b01620002ed565b9550506060620003698a828b01620002ed565b94505060806200037c8a828b01620002a9565b93505060a088015167ffffffffffffffff8111156200039a57600080fd5b620003a88a828b01620002c0565b92505060c0620003bb8a828b01620002ed565b91505092959891949750929550565b6000604051905081810181811067ffffffffffffffff82111715620003f457620003f362000596565b5b8060405250919050565b600067ffffffffffffffff8211156200041c576200041b62000596565b5b601f19601f8301169050602081019050919050565b60006200043e82620004c2565b91506200044b83620004c2565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0382111562000483576200048262000538565b5b828201905092915050565b60006200049b82620004a2565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b83811015620004ec578082015181840152602081019050620004cf565b83811115620004fc576000848401525b50505050565b600060028204905060018216806200051b57607f821691505b6020821081141562000532576200053162000567565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620005d0816200048e565b8114620005dc57600080fd5b50565b620005ea81620004c2565b8114620005f657600080fd5b50565b610fd680620006096000396000f3fe6080604052600436106100fe5760003560e01c80638da5cb5b11610095578063a6f9dae111610064578063a6f9dae1146102ef578063aa8c217c14610318578063bcead63e14610343578063e27facdc1461036e578063f966ade714610399576100fe565b80638da5cb5b1461023857806392d09ceb14610263578063a035b1fe1461028e578063a3b9e39d146102b9576100fe565b806357f7d74f116100d157806357f7d74f1461018e5780636164051a146101b7578063786716fe146101e25780637df1f1b91461020d576100fe565b80630b168f21146101035780630fb5a6b41461012e5780632c4e722e14610159578063330aec3e14610184575b600080fd5b34801561010f57600080fd5b506101186103a3565b6040516101259190610ca4565b60405180910390f35b34801561013a57600080fd5b50610143610431565b6040516101509190610d26565b60405180910390f35b34801561016557600080fd5b5061016e610437565b60405161017b9190610d26565b60405180910390f35b61018c61043d565b005b34801561019a57600080fd5b506101b560048036038101906101b09190610a5e565b610583565b005b3480156101c357600080fd5b506101cc610608565b6040516101d99190610c89565b60405180910390f35b3480156101ee57600080fd5b506101f761061b565b6040516102049190610d26565b60405180910390f35b34801561021957600080fd5b50610222610621565b60405161022f9190610bad565b60405180910390f35b34801561024457600080fd5b5061024d610645565b60405161025a9190610bad565b60405180910390f35b34801561026f57600080fd5b5061027861066b565b6040516102859190610d26565b60405180910390f35b34801561029a57600080fd5b506102a3610671565b6040516102b09190610d26565b60405180910390f35b3480156102c557600080fd5b506102ce610677565b6040516102e69c9b9a99989796959493929190610bc8565b60405180910390f35b3480156102fb57600080fd5b5061031660048036038101906103119190610a5e565b6107eb565b005b34801561032457600080fd5b5061032d61082f565b60405161033a9190610d26565b60405180910390f35b34801561034f57600080fd5b50610358610835565b6040516103659190610bad565b60405180910390f35b34801561037a57600080fd5b5061038361085b565b6040516103909190610bad565b60405180910390f35b6103a1610881565b005b600a80546103b090610eb9565b80601f01602080910402602001604051908101604052809291908181526020018280546103dc90610eb9565b80156104295780601f106103fe57610100808354040283529160200191610429565b820191906000526020600020905b81548152906001019060200180831161040c57829003601f168201915b505050505081565b60055481565b60045481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146104cb576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104c290610d06565b60405180910390fd5b60646004546003546104dd9190610de4565b6104e79190610db3565b6003546104f49190610d5d565b3410610516576001600760006101000a81548160ff0219169083151502179055505b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc6008549081150290604051600060405180830381858888f19350505050158015610580573d6000803e3d6000fd5b50565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600760009054906101000a900460ff1681565b60065481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60085481565b600b5481565b600080600080600080600080600080606060008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600354600454600554600654600760009054906101000a900460ff16600854600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600a600b5481805461074590610eb9565b80601f016020809104026020016040519081016040528092919081815260200182805461077190610eb9565b80156107be5780601f10610793576101008083540402835291602001916107be565b820191906000526020600020905b8154815290600101906020018083116107a157829003601f168201915b505050505091509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60035481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600760009054906101000a900460ff16156108d1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108c890610cc6565b60405180910390fd5b60065442111561095657600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc600854476109259190610d5d565b9081150290604051600060405180830381858888f19350505050158015610950573d6000803e3d6000fd5b50610a47565b60646004546003546109689190610de4565b6109729190610db3565b60035461097f9190610d5d565b34146109c0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109b790610ce6565b60405180910390fd5b6001600760006101000a81548160ff021916908315150217905550600960009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc6008549081150290604051600060405180830381858888f19350505050158015610a45573d6000803e3d6000fd5b505b565b600081359050610a5881610f89565b92915050565b600060208284031215610a7057600080fd5b6000610a7e84828501610a49565b91505092915050565b610a9081610e3e565b82525050565b610a9f81610e50565b82525050565b6000610ab082610d41565b610aba8185610d4c565b9350610aca818560208601610e86565b610ad381610f78565b840191505092915050565b6000610aeb601683610d4c565b91507f4c6f616e20697320616c726561647920726570616964000000000000000000006000830152602082019050919050565b6000610b2b601a83610d4c565b91507f496e636f72726563742072657061796d656e7420616d6f756e740000000000006000830152602082019050919050565b6000610b6b602083610d4c565b91507f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e746000830152602082019050919050565b610ba781610e7c565b82525050565b6000602082019050610bc26000830184610a87565b92915050565b600061018082019050610bde600083018f610a87565b610beb602083018e610a87565b610bf8604083018d610a87565b610c05606083018c610b9e565b610c12608083018b610b9e565b610c1f60a083018a610b9e565b610c2c60c0830189610b9e565b610c3960e0830188610a96565b610c47610100830187610b9e565b610c55610120830186610a87565b818103610140830152610c688185610aa5565b9050610c78610160830184610b9e565b9d9c50505050505050505050505050565b6000602082019050610c9e6000830184610a96565b92915050565b60006020820190508181036000830152610cbe8184610aa5565b905092915050565b60006020820190508181036000830152610cdf81610ade565b9050919050565b60006020820190508181036000830152610cff81610b1e565b9050919050565b60006020820190508181036000830152610d1f81610b5e565b9050919050565b6000602082019050610d3b6000830184610b9e565b92915050565b600081519050919050565b600082825260208201905092915050565b6000610d6882610e7c565b9150610d7383610e7c565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115610da857610da7610eeb565b5b828201905092915050565b6000610dbe82610e7c565b9150610dc983610e7c565b925082610dd957610dd8610f1a565b5b828204905092915050565b6000610def82610e7c565b9150610dfa83610e7c565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0483118215151615610e3357610e32610eeb565b5b828202905092915050565b6000610e4982610e5c565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b60005b83811015610ea4578082015181840152602081019050610e89565b83811115610eb3576000848401525b50505050565b60006002820490506001821680610ed157607f821691505b60208210811415610ee557610ee4610f49565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000601f19601f8301169050919050565b610f9281610e3e565b8114610f9d57600080fd5b5056fea2646970667358221220092a4520ee5d889387f2715b1f07f2c3a2780332b402ab50e8cb9ea45bb73aed64736f6c63430008000033" });
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
            for (let i = 0; i < accounts.length; i++) {
                if (JSON.stringify(accounts[i].toLowerCase()) === JSON.stringify(this.form.collateralHolder.toLowerCase())) {
                    this.form.collateralHolder = accounts[i];
                    account = accounts[i];
                    this.accountInstance = accounts[i];

                    await this.generateURL();
                    
                    const args = [
                        this.form.amount,
                        this.form.rate,
                        this.form.duration,
                        this.form.collateralAmount,
                        this.form.collateralHolder,
                        this.form.collateralUrl,
                        this.form.price,
                    ];
                    try {
                        //deploys the smart contract
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

                        const fileReader = new FileReader();
  
                        Toastify({
                            text: `Deployed loan contract ` + this.loanContractAddress + " " + this.form.collateralHolder,
                            backgroundColor: "green",
                            position: "center",
                        }).showToast();
                    }
                    catch (error) {
                        Toastify({
                            text: `Error deploying contract: ${error}` + this.form.collateralHoldercollateralHolder,
                            backgroundColor: "red",
                            position: "center",
                        }).showToast();
                    }
                    break;
                }
            }
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

            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const NFTContract = await new web3.eth.Contract(nftABI, null, {data: "60806040523480156200001157600080fd5b506040516200342b3803806200342b8339818101604052810190620000379190620002e8565b818181600090816200004a9190620005b8565b5080600190816200005c9190620005b8565b5050506200007f620000736200008760201b60201c565b6200008f60201b60201c565b50506200069f565b600033905090565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b6000604051905090565b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620001be8262000173565b810181811067ffffffffffffffff82111715620001e057620001df62000184565b5b80604052505050565b6000620001f562000155565b9050620002038282620001b3565b919050565b600067ffffffffffffffff82111562000226576200022562000184565b5b620002318262000173565b9050602081019050919050565b60005b838110156200025e57808201518184015260208101905062000241565b60008484015250505050565b6000620002816200027b8462000208565b620001e9565b905082815260208101848484011115620002a0576200029f6200016e565b5b620002ad8482856200023e565b509392505050565b600082601f830112620002cd57620002cc62000169565b5b8151620002df8482602086016200026a565b91505092915050565b600080604083850312156200030257620003016200015f565b5b600083015167ffffffffffffffff81111562000323576200032262000164565b5b6200033185828601620002b5565b925050602083015167ffffffffffffffff81111562000355576200035462000164565b5b6200036385828601620002b5565b9150509250929050565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680620003c057607f821691505b602082108103620003d657620003d562000378565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b600060088302620004407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8262000401565b6200044c868362000401565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600062000499620004936200048d8462000464565b6200046e565b62000464565b9050919050565b6000819050919050565b620004b58362000478565b620004cd620004c482620004a0565b8484546200040e565b825550505050565b600090565b620004e4620004d5565b620004f1818484620004aa565b505050565b5b8181101562000519576200050d600082620004da565b600181019050620004f7565b5050565b601f82111562000568576200053281620003dc565b6200053d84620003f1565b810160208510156200054d578190505b620005656200055c85620003f1565b830182620004f6565b50505b505050565b600082821c905092915050565b60006200058d600019846008026200056d565b1980831691505092915050565b6000620005a883836200057a565b9150826002028217905092915050565b620005c3826200036d565b67ffffffffffffffff811115620005df57620005de62000184565b5b620005eb8254620003a7565b620005f88282856200051d565b600060209050601f8311600181146200063057600084156200061b578287015190505b6200062785826200059a565b86555062000697565b601f1984166200064086620003dc565b60005b828110156200066a5784890151825560018201915060208501945060208101905062000643565b868310156200068a578489015162000686601f8916826200057a565b8355505b6001600288020188555050505b505050505050565b612d7c80620006af6000396000f3fe608060405234801561001057600080fd5b50600436106101165760003560e01c80638462151c116100a2578063b88d4fde11610071578063b88d4fde146102df578063c87b56dd146102fb578063d0def5211461032b578063e985e9c51461035b578063f2fde38b1461038b57610116565b80638462151c146102575780638da5cb5b1461028757806395d89b41146102a5578063a22cb465146102c357610116565b806323b872dd116100e957806323b872dd146101b557806342842e0e146101d15780636352211e146101ed57806370a082311461021d578063715018a61461024d57610116565b806301ffc9a71461011b57806306fdde031461014b578063081812fc14610169578063095ea7b314610199575b600080fd5b61013560048036038101906101309190611a13565b6103a7565b6040516101429190611a5b565b60405180910390f35b610153610489565b6040516101609190611b06565b60405180910390f35b610183600480360381019061017e9190611b5e565b61051b565b6040516101909190611bcc565b60405180910390f35b6101b360048036038101906101ae9190611c13565b610561565b005b6101cf60048036038101906101ca9190611c53565b610678565b005b6101eb60048036038101906101e69190611c53565b6106d8565b005b61020760048036038101906102029190611b5e565b6106f8565b6040516102149190611bcc565b60405180910390f35b61023760048036038101906102329190611ca6565b61077e565b6040516102449190611ce2565b60405180910390f35b610255610835565b005b610271600480360381019061026c9190611ca6565b610849565b60405161027e9190611dbb565b60405180910390f35b61028f6108e0565b60405161029c9190611bcc565b60405180910390f35b6102ad61090a565b6040516102ba9190611b06565b60405180910390f35b6102dd60048036038101906102d89190611e09565b61099c565b005b6102f960048036038101906102f49190611f7e565b6109b2565b005b61031560048036038101906103109190611b5e565b610a14565b6040516103229190611b06565b60405180910390f35b610345600480360381019061034091906120a2565b610b01565b6040516103529190611ce2565b60405180910390f35b610375600480360381019061037091906120fe565b610bae565b6040516103829190611a5b565b60405180910390f35b6103a560048036038101906103a09190611ca6565b610c42565b005b60007f80ac58cd000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916148061047257507f5b5e139f000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916145b80610482575061048182610c56565b5b9050919050565b6060600080546104989061216d565b80601f01602080910402602001604051908101604052809291908181526020018280546104c49061216d565b80156105115780601f106104e657610100808354040283529160200191610511565b820191906000526020600020905b8154815290600101906020018083116104f457829003601f168201915b5050505050905090565b600061052682610cc0565b6004600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b600061056c826106f8565b90508073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff16036105dc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105d390612210565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff166105fb610d0b565b73ffffffffffffffffffffffffffffffffffffffff16148061062a575061062981610624610d0b565b610bae565b5b610669576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610660906122a2565b60405180910390fd5b6106738383610d13565b505050565b610689610683610d0b565b82610dcc565b6106c8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106bf90612334565b60405180910390fd5b6106d3838383610e61565b505050565b6106f3838383604051806020016040528060008152506109b2565b505050565b6000806107048361115a565b9050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff1603610775576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161076c906123a0565b60405180910390fd5b80915050919050565b60008073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16036107ee576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016107e590612432565b60405180910390fd5b600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b61083d611197565b6108476000611215565b565b6060600960008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054806020026020016040519081016040528092919081815260200182805480156108d457602002820191906000526020600020905b8154815260200190600101908083116108c0575b50505050509050919050565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b6060600180546109199061216d565b80601f01602080910402602001604051908101604052809291908181526020018280546109459061216d565b80156109925780601f1061096757610100808354040283529160200191610992565b820191906000526020600020905b81548152906001019060200180831161097557829003601f168201915b5050505050905090565b6109ae6109a7610d0b565b83836112db565b5050565b6109c36109bd610d0b565b83610dcc565b610a02576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109f990612334565b60405180910390fd5b610a0e84848484611447565b50505050565b6060610a1f826114a3565b610a5e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610a55906124c4565b60405180910390fd5b600860008381526020019081526020016000208054610a7c9061216d565b80601f0160208091040260200160405190810160405280929190818152602001828054610aa89061216d565b8015610af55780601f10610aca57610100808354040283529160200191610af5565b820191906000526020600020905b815481529060010190602001808311610ad857829003601f168201915b50505050509050919050565b6000610b0b611197565b60076000815480929190610b1e90612513565b919050555060006007549050610b3484826114e4565b610b3e8184611701565b600960008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190806001815401808255809150506001900390600052602060002001600090919091909150558091505092915050565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b610c4a611197565b610c538161176e565b50565b60007f01ffc9a7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916149050919050565b610cc9816114a3565b610d08576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610cff906123a0565b60405180910390fd5b50565b600033905090565b816004600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16610d86836106f8565b73ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45050565b600080610dd8836106f8565b90508073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff161480610e1a5750610e198185610bae565b5b80610e5857508373ffffffffffffffffffffffffffffffffffffffff16610e408461051b565b73ffffffffffffffffffffffffffffffffffffffff16145b91505092915050565b8273ffffffffffffffffffffffffffffffffffffffff16610e81826106f8565b73ffffffffffffffffffffffffffffffffffffffff1614610ed7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ece906125cd565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603610f46576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610f3d9061265f565b60405180910390fd5b610f5383838360016117f1565b8273ffffffffffffffffffffffffffffffffffffffff16610f73826106f8565b73ffffffffffffffffffffffffffffffffffffffff1614610fc9576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610fc0906125cd565b60405180910390fd5b6004600082815260200190815260200160002060006101000a81549073ffffffffffffffffffffffffffffffffffffffff02191690556001600360008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055506001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a461115583838360016117f7565b505050565b60006002600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b61119f610d0b565b73ffffffffffffffffffffffffffffffffffffffff166111bd6108e0565b73ffffffffffffffffffffffffffffffffffffffff1614611213576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161120a906126cb565b60405180910390fd5b565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b8173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1603611349576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161134090612737565b60405180910390fd5b80600560008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c318360405161143a9190611a5b565b60405180910390a3505050565b611452848484610e61565b61145e848484846117fd565b61149d576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611494906127c9565b60405180910390fd5b50505050565b60008073ffffffffffffffffffffffffffffffffffffffff166114c58361115a565b73ffffffffffffffffffffffffffffffffffffffff1614159050919050565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603611553576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161154a90612835565b60405180910390fd5b61155c816114a3565b1561159c576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611593906128a1565b60405180910390fd5b6115aa6000838360016117f1565b6115b3816114a3565b156115f3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016115ea906128a1565b60405180910390fd5b6001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a46116fd6000838360016117f7565b5050565b61170a826114a3565b611749576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161174090612933565b60405180910390fd5b806008600084815260200190815260200160002090816117699190612aff565b505050565b611776611197565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16036117e5576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016117dc90612c43565b60405180910390fd5b6117ee81611215565b50565b50505050565b50505050565b600061181e8473ffffffffffffffffffffffffffffffffffffffff16611984565b15611977578373ffffffffffffffffffffffffffffffffffffffff1663150b7a02611847610d0b565b8786866040518563ffffffff1660e01b81526004016118699493929190612cb8565b6020604051808303816000875af19250505080156118a557506040513d601f19601f820116820180604052508101906118a29190612d19565b60015b611927573d80600081146118d5576040519150601f19603f3d011682016040523d82523d6000602084013e6118da565b606091505b50600081510361191f576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611916906127c9565b60405180910390fd5b805181602001fd5b63150b7a0260e01b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916817bffffffffffffffffffffffffffffffffffffffffffffffffffffffff19161491505061197c565b600190505b949350505050565b6000808273ffffffffffffffffffffffffffffffffffffffff163b119050919050565b6000604051905090565b600080fd5b600080fd5b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b6119f0816119bb565b81146119fb57600080fd5b50565b600081359050611a0d816119e7565b92915050565b600060208284031215611a2957611a286119b1565b5b6000611a37848285016119fe565b91505092915050565b60008115159050919050565b611a5581611a40565b82525050565b6000602082019050611a706000830184611a4c565b92915050565b600081519050919050565b600082825260208201905092915050565b60005b83811015611ab0578082015181840152602081019050611a95565b60008484015250505050565b6000601f19601f8301169050919050565b6000611ad882611a76565b611ae28185611a81565b9350611af2818560208601611a92565b611afb81611abc565b840191505092915050565b60006020820190508181036000830152611b208184611acd565b905092915050565b6000819050919050565b611b3b81611b28565b8114611b4657600080fd5b50565b600081359050611b5881611b32565b92915050565b600060208284031215611b7457611b736119b1565b5b6000611b8284828501611b49565b91505092915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000611bb682611b8b565b9050919050565b611bc681611bab565b82525050565b6000602082019050611be16000830184611bbd565b92915050565b611bf081611bab565b8114611bfb57600080fd5b50565b600081359050611c0d81611be7565b92915050565b60008060408385031215611c2a57611c296119b1565b5b6000611c3885828601611bfe565b9250506020611c4985828601611b49565b9150509250929050565b600080600060608486031215611c6c57611c6b6119b1565b5b6000611c7a86828701611bfe565b9350506020611c8b86828701611bfe565b9250506040611c9c86828701611b49565b9150509250925092565b600060208284031215611cbc57611cbb6119b1565b5b6000611cca84828501611bfe565b91505092915050565b611cdc81611b28565b82525050565b6000602082019050611cf76000830184611cd3565b92915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b611d3281611b28565b82525050565b6000611d448383611d29565b60208301905092915050565b6000602082019050919050565b6000611d6882611cfd565b611d728185611d08565b9350611d7d83611d19565b8060005b83811015611dae578151611d958882611d38565b9750611da083611d50565b925050600181019050611d81565b5085935050505092915050565b60006020820190508181036000830152611dd58184611d5d565b905092915050565b611de681611a40565b8114611df157600080fd5b50565b600081359050611e0381611ddd565b92915050565b60008060408385031215611e2057611e1f6119b1565b5b6000611e2e85828601611bfe565b9250506020611e3f85828601611df4565b9150509250929050565b600080fd5b600080fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b611e8b82611abc565b810181811067ffffffffffffffff82111715611eaa57611ea9611e53565b5b80604052505050565b6000611ebd6119a7565b9050611ec98282611e82565b919050565b600067ffffffffffffffff821115611ee957611ee8611e53565b5b611ef282611abc565b9050602081019050919050565b82818337600083830152505050565b6000611f21611f1c84611ece565b611eb3565b905082815260208101848484011115611f3d57611f3c611e4e565b5b611f48848285611eff565b509392505050565b600082601f830112611f6557611f64611e49565b5b8135611f75848260208601611f0e565b91505092915050565b60008060008060808587031215611f9857611f976119b1565b5b6000611fa687828801611bfe565b9450506020611fb787828801611bfe565b9350506040611fc887828801611b49565b925050606085013567ffffffffffffffff811115611fe957611fe86119b6565b5b611ff587828801611f50565b91505092959194509250565b600067ffffffffffffffff82111561201c5761201b611e53565b5b61202582611abc565b9050602081019050919050565b600061204561204084612001565b611eb3565b90508281526020810184848401111561206157612060611e4e565b5b61206c848285611eff565b509392505050565b600082601f83011261208957612088611e49565b5b8135612099848260208601612032565b91505092915050565b600080604083850312156120b9576120b86119b1565b5b60006120c785828601611bfe565b925050602083013567ffffffffffffffff8111156120e8576120e76119b6565b5b6120f485828601612074565b9150509250929050565b60008060408385031215612115576121146119b1565b5b600061212385828601611bfe565b925050602061213485828601611bfe565b9150509250929050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000600282049050600182168061218557607f821691505b6020821081036121985761219761213e565b5b50919050565b7f4552433732313a20617070726f76616c20746f2063757272656e74206f776e6560008201527f7200000000000000000000000000000000000000000000000000000000000000602082015250565b60006121fa602183611a81565b91506122058261219e565b604082019050919050565b60006020820190508181036000830152612229816121ed565b9050919050565b7f4552433732313a20617070726f76652063616c6c6572206973206e6f7420746f60008201527f6b656e206f776e6572206f7220617070726f76656420666f7220616c6c000000602082015250565b600061228c603d83611a81565b915061229782612230565b604082019050919050565b600060208201905081810360008301526122bb8161227f565b9050919050565b7f4552433732313a2063616c6c6572206973206e6f7420746f6b656e206f776e6560008201527f72206f7220617070726f76656400000000000000000000000000000000000000602082015250565b600061231e602d83611a81565b9150612329826122c2565b604082019050919050565b6000602082019050818103600083015261234d81612311565b9050919050565b7f4552433732313a20696e76616c696420746f6b656e2049440000000000000000600082015250565b600061238a601883611a81565b915061239582612354565b602082019050919050565b600060208201905081810360008301526123b98161237d565b9050919050565b7f4552433732313a2061646472657373207a65726f206973206e6f74206120766160008201527f6c6964206f776e65720000000000000000000000000000000000000000000000602082015250565b600061241c602983611a81565b9150612427826123c0565b604082019050919050565b6000602082019050818103600083015261244b8161240f565b9050919050565b7f4552433732314d657461646174613a2055524920717565727920666f72206e6f60008201527f6e6578697374656e7420746f6b656e0000000000000000000000000000000000602082015250565b60006124ae602f83611a81565b91506124b982612452565b604082019050919050565b600060208201905081810360008301526124dd816124a1565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061251e82611b28565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82036125505761254f6124e4565b5b600182019050919050565b7f4552433732313a207472616e736665722066726f6d20696e636f72726563742060008201527f6f776e6572000000000000000000000000000000000000000000000000000000602082015250565b60006125b7602583611a81565b91506125c28261255b565b604082019050919050565b600060208201905081810360008301526125e6816125aa565b9050919050565b7f4552433732313a207472616e7366657220746f20746865207a65726f2061646460008201527f7265737300000000000000000000000000000000000000000000000000000000602082015250565b6000612649602483611a81565b9150612654826125ed565b604082019050919050565b600060208201905081810360008301526126788161263c565b9050919050565b7f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572600082015250565b60006126b5602083611a81565b91506126c08261267f565b602082019050919050565b600060208201905081810360008301526126e4816126a8565b9050919050565b7f4552433732313a20617070726f766520746f2063616c6c657200000000000000600082015250565b6000612721601983611a81565b915061272c826126eb565b602082019050919050565b6000602082019050818103600083015261275081612714565b9050919050565b7f4552433732313a207472616e7366657220746f206e6f6e20455243373231526560008201527f63656976657220696d706c656d656e7465720000000000000000000000000000602082015250565b60006127b3603283611a81565b91506127be82612757565b604082019050919050565b600060208201905081810360008301526127e2816127a6565b9050919050565b7f4552433732313a206d696e7420746f20746865207a65726f2061646472657373600082015250565b600061281f602083611a81565b915061282a826127e9565b602082019050919050565b6000602082019050818103600083015261284e81612812565b9050919050565b7f4552433732313a20746f6b656e20616c7265616479206d696e74656400000000600082015250565b600061288b601c83611a81565b915061289682612855565b602082019050919050565b600060208201905081810360008301526128ba8161287e565b9050919050565b7f4552433732314d657461646174613a2055524920736574206f66206e6f6e657860008201527f697374656e7420746f6b656e0000000000000000000000000000000000000000602082015250565b600061291d602c83611a81565b9150612928826128c1565b604082019050919050565b6000602082019050818103600083015261294c81612910565b9050919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026129b57fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82612978565b6129bf8683612978565b95508019841693508086168417925050509392505050565b6000819050919050565b60006129fc6129f76129f284611b28565b6129d7565b611b28565b9050919050565b6000819050919050565b612a16836129e1565b612a2a612a2282612a03565b848454612985565b825550505050565b600090565b612a3f612a32565b612a4a818484612a0d565b505050565b5b81811015612a6e57612a63600082612a37565b600181019050612a50565b5050565b601f821115612ab357612a8481612953565b612a8d84612968565b81016020851015612a9c578190505b612ab0612aa885612968565b830182612a4f565b50505b505050565b600082821c905092915050565b6000612ad660001984600802612ab8565b1980831691505092915050565b6000612aef8383612ac5565b9150826002028217905092915050565b612b0882611a76565b67ffffffffffffffff811115612b2157612b20611e53565b5b612b2b825461216d565b612b36828285612a72565b600060209050601f831160018114612b695760008415612b57578287015190505b612b618582612ae3565b865550612bc9565b601f198416612b7786612953565b60005b82811015612b9f57848901518255600182019150602085019450602081019050612b7a565b86831015612bbc5784890151612bb8601f891682612ac5565b8355505b6001600288020188555050505b505050505050565b7f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160008201527f6464726573730000000000000000000000000000000000000000000000000000602082015250565b6000612c2d602683611a81565b9150612c3882612bd1565b604082019050919050565b60006020820190508181036000830152612c5c81612c20565b9050919050565b600081519050919050565b600082825260208201905092915050565b6000612c8a82612c63565b612c948185612c6e565b9350612ca4818560208601611a92565b612cad81611abc565b840191505092915050565b6000608082019050612ccd6000830187611bbd565b612cda6020830186611bbd565b612ce76040830185611cd3565b8181036060830152612cf98184612c7f565b905095945050505050565b600081519050612d13816119e7565b92915050565b600060208284031215612d2f57612d2e6119b1565b5b6000612d3d84828501612d04565b9150509291505056fea264697066735822122024b854a4a0b42fe9384463bf63e28d8f916807b9c4f63a60dbe7c7bdb3c0a33064736f6c63430008120033"})
            const gas = 3000000; // Set the gas limit to 3000000
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
            this.contract.instance = new web3.eth.Contract(nftABI, this.contract.address);

            //mints a users nft to thier account
            await contract.methods.mint(this.accountInstance, url).send({from: accounts[0]})
            const tokenIds = await contract.methods.tokensOfOwner(this.accountInstance).call()
            this.tokens = tokenIds;
            const uri = await contract.methods.tokenURI(tokenIds[0]).call()
            Toastify({
               text: "NFT uploaded "+this.contract.address + "with uri "+uri,
               position: "center",
            }).showToast();
        },

    },
    components: { NFTmint }
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
  