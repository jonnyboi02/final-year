
   <template>
    <!-- <NFTmint/> -->
    <div style="color: white;">
    <!-- <div v-if="borrower">
      {{borrower.address}}
    </div> -->


    <h3>Request Loan</h3>
    <!-- <div id = 'header'> -->
      <div id='contents' style="border-style: solid; border-radius: 25px; border-width: thin;">
        <h4> Current Annual Interest rate is {{ baseInterestRate }}%</h4>

      </div>

    <!-- </div> -->
    <div v-if="loanContractAddress " id="deploy" > Contract Deployed at : {{ loanContractAddress }} </div>
    <div style="padding-bottom: 10px; " @change="aprCalculation">
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
        <!-- Desired Price of Contract (in Ethers):<br> <input v-model="form.price"/>
        <br> -->
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
      <button @click="deployLoanContract" class="button"  >Request Loan</button>
      <!-- <button @click="changeOwner" class="button" style="float: right; ">Change Contract Owner</button>
      <button @click="getLoanDetails">Get Contract Details</button>  -->
    </div>

    <div style="border-style: solid; border-radius: 25px; border-width: thin; margin-left: 75px; margin-right: 75px;">
        <h4>Calculated APR: {{ this.apr }}%</h4>
    

    </div>

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
    async mounted() {
        this.getAccounts();
        await this.getAddress();
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
                amount: "",
                rate: 3,
                duration: 3600,
                collateralAmount: 200,
                collateralHolder: null,
                collateralUrl: " ",
                //0.5 Ether as default price
                price: 5,
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
        };
    },
    methods: {
        aprCalculation(){
            try{
                const rate = this.baseInterestRate
                const amount = this.form.amount
                const days = this.form.duration/3600
                const collateralValue = this.form.collateralAmount
                
                let interestRate = rate+ (1-(rate/100))*(1-(collateralValue/amount))
                let interestAmount = (amount * (interestRate/100) *(days/365))

                //formula used to calculate the apr for stuff
                let apr = ((interestAmount/amount)/(days/365))*100;
                this.apr = apr.toFixed(2);

                
                if (apr<0){
                    this.form.rate = 3
                }
                else{
                    this.form.rate = 3;
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
                        text: "Hey",
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
            const formData = new FormData();
            formData.append("file", this.nftFile);
            const response1 = await fetch("http://localhost:8000/generate-url/", {
                method: "POST",
                body: formData
            });
            const data = await response1.json();
            //this.test = data.url;
            //his.form.collateralUrl = data.url;
            let url = data.url

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
           

            await contract.methods.mint(account, url).send({from: accounts[0]})
           
 


            const tokenIds = await contract.methods.tokensOfOwner(account).call()
            this.tokens = tokenIds;
            const uri = await contract.methods.tokenURI(tokenIds[tokenIds.length-1]).call()
            this.uri = uri


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
                        'collateralURL' : this.tokens[this.tokens.length-1],
                        'price': this.form.price,

                    })
                })
                let datas = await response.json()
                Toastify({
                    text: `Loan Request Made! `+account,
                    backgroundColor: "green",
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
            this.sendTransaction();

            this.requestLoan();

            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const networkId = await web3.eth.net.getId();
            const LoanContract = new web3.eth.Contract(LoanABI, null, { data: "60806040523480156200001157600080fd5b5060405162001623380380620016238339818101604052810190620000379190620003a7565b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660028190555085600381905550846004819055508360078190555082600860006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508160099081620001269190620006ba565b5080600a81905550600454426200013e9190620007d0565b6005819055506000600660006101000a81548160ff0219169083151502179055506000600b81905550505050505050506200080b565b6000604051905090565b600080fd5b600080fd5b6000819050919050565b6200019d8162000188565b8114620001a957600080fd5b50565b600081519050620001bd8162000192565b92915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000620001f082620001c3565b9050919050565b6200020281620001e3565b81146200020e57600080fd5b50565b6000815190506200022281620001f7565b92915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6200027d8262000232565b810181811067ffffffffffffffff821117156200029f576200029e62000243565b5b80604052505050565b6000620002b462000174565b9050620002c2828262000272565b919050565b600067ffffffffffffffff821115620002e557620002e462000243565b5b620002f08262000232565b9050602081019050919050565b60005b838110156200031d57808201518184015260208101905062000300565b60008484015250505050565b6000620003406200033a84620002c7565b620002a8565b9050828152602081018484840111156200035f576200035e6200022d565b5b6200036c848285620002fd565b509392505050565b600082601f8301126200038c576200038b62000228565b5b81516200039e84826020860162000329565b91505092915050565b600080600080600080600060e0888a031215620003c957620003c86200017e565b5b6000620003d98a828b01620001ac565b9750506020620003ec8a828b01620001ac565b9650506040620003ff8a828b01620001ac565b9550506060620004128a828b01620001ac565b9450506080620004258a828b0162000211565b93505060a088015167ffffffffffffffff81111562000449576200044862000183565b5b620004578a828b0162000374565b92505060c06200046a8a828b01620001ac565b91505092959891949750929550565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680620004cc57607f821691505b602082108103620004e257620004e162000484565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026200054c7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff826200050d565b6200055886836200050d565b95508019841693508086168417925050509392505050565b6000819050919050565b60006200059b620005956200058f8462000188565b62000570565b62000188565b9050919050565b6000819050919050565b620005b7836200057a565b620005cf620005c682620005a2565b8484546200051a565b825550505050565b600090565b620005e6620005d7565b620005f3818484620005ac565b505050565b5b818110156200061b576200060f600082620005dc565b600181019050620005f9565b5050565b601f8211156200066a576200063481620004e8565b6200063f84620004fd565b810160208510156200064f578190505b620006676200065e85620004fd565b830182620005f8565b50505b505050565b600082821c905092915050565b60006200068f600019846008026200066f565b1980831691505092915050565b6000620006aa83836200067c565b9150826002028217905092915050565b620006c58262000479565b67ffffffffffffffff811115620006e157620006e062000243565b5b620006ed8254620004b3565b620006fa8282856200061f565b600060209050601f8311600181146200073257600084156200071d578287015190505b6200072985826200069c565b86555062000799565b601f1984166200074286620004e8565b60005b828110156200076c5784890151825560018201915060208501945060208101905062000745565b868310156200078c578489015162000788601f8916826200067c565b8355505b6001600288020188555050505b505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000620007dd8262000188565b9150620007ea8362000188565b9250828201905080821115620008055762000804620007a1565b5b92915050565b610e08806200081b6000396000f3fe6080604052600436106100f75760003560e01c806392d09ceb1161008a578063aa8c217c11610059578063aa8c217c146103e5578063bcead63e14610410578063d524b0ff1461043b578063e27facdc14610466576101f6565b806392d09ceb14610330578063a035b1fe1461035b578063a3b9e39d14610386578063a6f9dae1146103bc576101f6565b806357f7d74f116100c657806357f7d74f146102865780636164051a146102af578063786716fe146102da5780638da5cb5b14610305576101f6565b80630b168f21146101fb5780630fb5a6b4146102265780632c4e722e14610251578063330aec3e1461027c576101f6565b366101f657600660009054906101000a900460ff161561014c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101439061094f565b60405180910390fd5b600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146101dc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101d3906109bb565b60405180910390fd5b34600b60008282546101ee9190610a14565b925050819055005b600080fd5b34801561020757600080fd5b50610210610491565b60405161021d9190610ac7565b60405180910390f35b34801561023257600080fd5b5061023b61051f565b6040516102489190610af8565b60405180910390f35b34801561025d57600080fd5b50610266610525565b6040516102739190610af8565b60405180910390f35b61028461052b565b005b34801561029257600080fd5b506102ad60048036038101906102a89190610b76565b610636565b005b3480156102bb57600080fd5b506102c46106ba565b6040516102d19190610bbe565b60405180910390f35b3480156102e657600080fd5b506102ef6106cd565b6040516102fc9190610af8565b60405180910390f35b34801561031157600080fd5b5061031a6106d3565b6040516103279190610be8565b60405180910390f35b34801561033c57600080fd5b506103456106f9565b6040516103529190610af8565b60405180910390f35b34801561036757600080fd5b506103706106ff565b60405161037d9190610af8565b60405180910390f35b34801561039257600080fd5b5061039b610705565b6040516103b39c9b9a99989796959493929190610c03565b60405180910390f35b3480156103c857600080fd5b506103e360048036038101906103de9190610b76565b610858565b005b3480156103f157600080fd5b506103fa61089c565b6040516104079190610af8565b60405180910390f35b34801561041c57600080fd5b506104256108a2565b6040516104329190610be8565b60405180910390f35b34801561044757600080fd5b506104506108c6565b60405161045d9190610af8565b60405180910390f35b34801561047257600080fd5b5061047b6108cc565b6040516104889190610be8565b60405180910390f35b6009805461049e90610cf3565b80601f01602080910402602001604051908101604052809291908181526020018280546104ca90610cf3565b80156105175780601f106104ec57610100808354040283529160200191610517565b820191906000526020600020905b8154815290600101906020018083116104fa57829003601f168201915b505050505081565b60045481565b60035481565b670de0b6b3a76400006002546105419190610d24565b600354670de0b6b3a764000060025461055a9190610d24565b6105649190610d24565b61056e9190610a14565b4710156105b0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105a790610db2565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc479081150290604051600060405180830381858888f19350505050158015610618573d6000803e3d6000fd5b506001600660006101000a81548160ff021916908315150217905550565b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600660009054906101000a900460ff1681565b60055481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60075481565b600a5481565b6000806000806000806000806000606060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600254600354600454600554600660009054906101000a900460ff16600754600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166009600a54600b548280546107b290610cf3565b80601f01602080910402602001604051908101604052809291908181526020018280546107de90610cf3565b801561082b5780601f106108005761010080835404028352916020019161082b565b820191906000526020600020905b81548152906001019060200180831161080e57829003601f168201915b505050505092509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60025481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600b5481565b600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600082825260208201905092915050565b7f4c6f616e20697320616c72656164792072657061696400000000000000000000600082015250565b60006109396016836108f2565b915061094482610903565b602082019050919050565b600060208201905081810360008301526109688161092c565b9050919050565b7f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e74600082015250565b60006109a56020836108f2565b91506109b08261096f565b602082019050919050565b600060208201905081810360008301526109d481610998565b9050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000610a1f826109db565b9150610a2a836109db565b9250828201905080821115610a4257610a416109e5565b5b92915050565b600081519050919050565b60005b83811015610a71578082015181840152602081019050610a56565b60008484015250505050565b6000601f19601f8301169050919050565b6000610a9982610a48565b610aa381856108f2565b9350610ab3818560208601610a53565b610abc81610a7d565b840191505092915050565b60006020820190508181036000830152610ae18184610a8e565b905092915050565b610af2816109db565b82525050565b6000602082019050610b0d6000830184610ae9565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610b4382610b18565b9050919050565b610b5381610b38565b8114610b5e57600080fd5b50565b600081359050610b7081610b4a565b92915050565b600060208284031215610b8c57610b8b610b13565b5b6000610b9a84828501610b61565b91505092915050565b60008115159050919050565b610bb881610ba3565b82525050565b6000602082019050610bd36000830184610baf565b92915050565b610be281610b38565b82525050565b6000602082019050610bfd6000830184610bd9565b92915050565b600061018082019050610c19600083018f610bd9565b610c26602083018e610bd9565b610c33604083018d610ae9565b610c40606083018c610ae9565b610c4d608083018b610ae9565b610c5a60a083018a610ae9565b610c6760c0830189610baf565b610c7460e0830188610ae9565b610c82610100830187610bd9565b818103610120830152610c958186610a8e565b9050610ca5610140830185610ae9565b610cb3610160830184610ae9565b9d9c50505050505050505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680610d0b57607f821691505b602082108103610d1e57610d1d610cc4565b5b50919050565b6000610d2f826109db565b9150610d3a836109db565b9250828202610d48816109db565b91508282048414831517610d5f57610d5e6109e5565b5b5092915050565b7f42616c616e6365206e6f742073756666696369656e7400000000000000000000600082015250565b6000610d9c6016836108f2565b9150610da782610d66565b602082019050919050565b60006020820190508181036000830152610dcb81610d8f565b905091905056fea2646970667358221220ad1c2b9f4db2f84bf5c1544617fa7eb572a3478d5a19c520df02c5b692fda0cf64736f6c63430008120033" });
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
            const NFTContract = await new web3.eth.Contract(nftABI, null, {data: "60806040523480156200001157600080fd5b50604051620037bb380380620037bb8339818101604052810190620000379190620002e8565b818181600090816200004a9190620005b8565b5080600190816200005c9190620005b8565b5050506200007f620000736200008760201b60201c565b6200008f60201b60201c565b50506200069f565b600033905090565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b6000604051905090565b600080fd5b600080fd5b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b620001be8262000173565b810181811067ffffffffffffffff82111715620001e057620001df62000184565b5b80604052505050565b6000620001f562000155565b9050620002038282620001b3565b919050565b600067ffffffffffffffff82111562000226576200022562000184565b5b620002318262000173565b9050602081019050919050565b60005b838110156200025e57808201518184015260208101905062000241565b60008484015250505050565b6000620002816200027b8462000208565b620001e9565b905082815260208101848484011115620002a0576200029f6200016e565b5b620002ad8482856200023e565b509392505050565b600082601f830112620002cd57620002cc62000169565b5b8151620002df8482602086016200026a565b91505092915050565b600080604083850312156200030257620003016200015f565b5b600083015167ffffffffffffffff81111562000323576200032262000164565b5b6200033185828601620002b5565b925050602083015167ffffffffffffffff81111562000355576200035462000164565b5b6200036385828601620002b5565b9150509250929050565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680620003c057607f821691505b602082108103620003d657620003d562000378565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b600060088302620004407fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8262000401565b6200044c868362000401565b95508019841693508086168417925050509392505050565b6000819050919050565b6000819050919050565b600062000499620004936200048d8462000464565b6200046e565b62000464565b9050919050565b6000819050919050565b620004b58362000478565b620004cd620004c482620004a0565b8484546200040e565b825550505050565b600090565b620004e4620004d5565b620004f1818484620004aa565b505050565b5b8181101562000519576200050d600082620004da565b600181019050620004f7565b5050565b601f82111562000568576200053281620003dc565b6200053d84620003f1565b810160208510156200054d578190505b620005656200055c85620003f1565b830182620004f6565b50505b505050565b600082821c905092915050565b60006200058d600019846008026200056d565b1980831691505092915050565b6000620005a883836200057a565b9150826002028217905092915050565b620005c3826200036d565b67ffffffffffffffff811115620005df57620005de62000184565b5b620005eb8254620003a7565b620005f88282856200051d565b600060209050601f8311600181146200063057600084156200061b578287015190505b6200062785826200059a565b86555062000697565b601f1984166200064086620003dc565b60005b828110156200066a5784890151825560018201915060208501945060208101905062000643565b868310156200068a578489015162000686601f8916826200057a565b8355505b6001600288020188555050505b505050505050565b61310c80620006af6000396000f3fe608060405234801561001057600080fd5b506004361061012c5760003560e01c806373b64ac5116100ad578063b88d4fde11610071578063b88d4fde14610341578063c87b56dd1461035d578063d0def5211461038d578063e985e9c5146103bd578063f2fde38b146103ed5761012c565b806373b64ac5146102895780638462151c146102b95780638da5cb5b146102e957806395d89b4114610307578063a22cb465146103255761012c565b806342842e0e116100f457806342842e0e146101e75780636352211e1461020357806369e9cae11461023357806370a082311461024f578063715018a61461027f5761012c565b806301ffc9a71461013157806306fdde0314610161578063081812fc1461017f578063095ea7b3146101af57806323b872dd146101cb575b600080fd5b61014b60048036038101906101469190611bed565b610409565b6040516101589190611c35565b60405180910390f35b6101696104eb565b6040516101769190611ce0565b60405180910390f35b61019960048036038101906101949190611d38565b61057d565b6040516101a69190611da6565b60405180910390f35b6101c960048036038101906101c49190611ded565b6105c3565b005b6101e560048036038101906101e09190611e2d565b6106da565b005b61020160048036038101906101fc9190611e2d565b61073a565b005b61021d60048036038101906102189190611d38565b61075a565b60405161022a9190611da6565b60405180910390f35b61024d60048036038101906102489190611e2d565b6107e0565b005b61026960048036038101906102649190611e80565b610881565b6040516102769190611ebc565b60405180910390f35b610287610938565b005b6102a3600480360381019061029e9190611d38565b61094c565b6040516102b09190611da6565b60405180910390f35b6102d360048036038101906102ce9190611e80565b6109d1565b6040516102e09190611f95565b60405180910390f35b6102f1610a68565b6040516102fe9190611da6565b60405180910390f35b61030f610a92565b60405161031c9190611ce0565b60405180910390f35b61033f600480360381019061033a9190611fe3565b610b24565b005b61035b60048036038101906103569190612158565b610b3a565b005b61037760048036038101906103729190611d38565b610b9c565b6040516103849190611ce0565b60405180910390f35b6103a760048036038101906103a2919061227c565b610c89565b6040516103b49190611ebc565b60405180910390f35b6103d760048036038101906103d291906122d8565b610d88565b6040516103e49190611c35565b60405180910390f35b61040760048036038101906104029190611e80565b610e1c565b005b60007f80ac58cd000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614806104d457507f5b5e139f000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916145b806104e457506104e382610e30565b5b9050919050565b6060600080546104fa90612347565b80601f016020809104026020016040519081016040528092919081815260200182805461052690612347565b80156105735780601f1061054857610100808354040283529160200191610573565b820191906000526020600020905b81548152906001019060200180831161055657829003601f168201915b5050505050905090565b600061058882610e9a565b6004600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b60006105ce8261075a565b90508073ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff160361063e576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610635906123ea565b60405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff1661065d610ee5565b73ffffffffffffffffffffffffffffffffffffffff16148061068c575061068b81610686610ee5565b610d88565b5b6106cb576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106c29061247c565b60405180910390fd5b6106d58383610eed565b505050565b6106eb6106e5610ee5565b82610fa6565b61072a576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016107219061250e565b60405180910390fd5b61073583838361103b565b505050565b61075583838360405180602001604052806000815250610b3a565b505050565b60008061076683611334565b9050600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16036107d7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016107ce9061257a565b60405180910390fd5b80915050919050565b6107ea3382610fa6565b610829576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108209061260c565b60405180910390fd5b61083281611371565b610871576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108689061269e565b60405180910390fd5b61087c83838361103b565b505050565b60008073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff16036108f1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108e890612730565b60405180910390fd5b600360008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b6109406113b2565b61094a6000611430565b565b600061095782611371565b610996576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161098d906127c2565b60405180910390fd5b6009600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b6060600a60008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020805480602002602001604051908101604052809291908181526020018280548015610a5c57602002820191906000526020600020905b815481526020019060010190808311610a48575b50505050509050919050565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b606060018054610aa190612347565b80601f0160208091040260200160405190810160405280929190818152602001828054610acd90612347565b8015610b1a5780601f10610aef57610100808354040283529160200191610b1a565b820191906000526020600020905b815481529060010190602001808311610afd57829003601f168201915b5050505050905090565b610b36610b2f610ee5565b83836114f6565b5050565b610b4b610b45610ee5565b83610fa6565b610b8a576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610b819061250e565b60405180910390fd5b610b9684848484611662565b50505050565b6060610ba782611371565b610be6576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610bdd90612854565b60405180910390fd5b600860008381526020019081526020016000208054610c0490612347565b80601f0160208091040260200160405190810160405280929190818152602001828054610c3090612347565b8015610c7d5780601f10610c5257610100808354040283529160200191610c7d565b820191906000526020600020905b815481529060010190602001808311610c6057829003601f168201915b50505050509050919050565b6000610c936113b2565b60076000815480929190610ca6906128a3565b919050555060006007549050610cbc84826116be565b610cc681846118db565b836009600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600a60008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190806001815401808255809150506001900390600052602060002001600090919091909150558091505092915050565b6000600560008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16905092915050565b610e246113b2565b610e2d81611948565b50565b60007f01ffc9a7000000000000000000000000000000000000000000000000000000007bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916827bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916149050919050565b610ea381611371565b610ee2576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ed99061257a565b60405180910390fd5b50565b600033905090565b816004600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16610f608361075a565b73ffffffffffffffffffffffffffffffffffffffff167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45050565b600080610fb28361075a565b90508073ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff161480610ff45750610ff38185610d88565b5b8061103257508373ffffffffffffffffffffffffffffffffffffffff1661101a8461057d565b73ffffffffffffffffffffffffffffffffffffffff16145b91505092915050565b8273ffffffffffffffffffffffffffffffffffffffff1661105b8261075a565b73ffffffffffffffffffffffffffffffffffffffff16146110b1576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016110a89061295d565b60405180910390fd5b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff1603611120576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611117906129ef565b60405180910390fd5b61112d83838360016119cb565b8273ffffffffffffffffffffffffffffffffffffffff1661114d8261075a565b73ffffffffffffffffffffffffffffffffffffffff16146111a3576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161119a9061295d565b60405180910390fd5b6004600082815260200190815260200160002060006101000a81549073ffffffffffffffffffffffffffffffffffffffff02191690556001600360008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020600082825403925050819055506001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff168473ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a461132f83838360016119d1565b505050565b60006002600083815260200190815260200160002060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff169050919050565b60008073ffffffffffffffffffffffffffffffffffffffff1661139383611334565b73ffffffffffffffffffffffffffffffffffffffff1614159050919050565b6113ba610ee5565b73ffffffffffffffffffffffffffffffffffffffff166113d8610a68565b73ffffffffffffffffffffffffffffffffffffffff161461142e576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161142590612a5b565b60405180910390fd5b565b6000600660009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905081600660006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508173ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff167f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e060405160405180910390a35050565b8173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff1603611564576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161155b90612ac7565b60405180910390fd5b80600560008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508173ffffffffffffffffffffffffffffffffffffffff168373ffffffffffffffffffffffffffffffffffffffff167f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31836040516116559190611c35565b60405180910390a3505050565b61166d84848461103b565b611679848484846119d7565b6116b8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016116af90612b59565b60405180910390fd5b50505050565b600073ffffffffffffffffffffffffffffffffffffffff168273ffffffffffffffffffffffffffffffffffffffff160361172d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161172490612bc5565b60405180910390fd5b61173681611371565b15611776576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161176d90612c31565b60405180910390fd5b6117846000838360016119cb565b61178d81611371565b156117cd576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016117c490612c31565b60405180910390fd5b6001600360008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282540192505081905550816002600083815260200190815260200160002060006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550808273ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef60405160405180910390a46118d76000838360016119d1565b5050565b6118e482611371565b611923576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161191a90612cc3565b60405180910390fd5b806008600084815260200190815260200160002090816119439190612e8f565b505050565b6119506113b2565b600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16036119bf576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016119b690612fd3565b60405180910390fd5b6119c881611430565b50565b50505050565b50505050565b60006119f88473ffffffffffffffffffffffffffffffffffffffff16611b5e565b15611b51578373ffffffffffffffffffffffffffffffffffffffff1663150b7a02611a21610ee5565b8786866040518563ffffffff1660e01b8152600401611a439493929190613048565b6020604051808303816000875af1925050508015611a7f57506040513d601f19601f82011682018060405250810190611a7c91906130a9565b60015b611b01573d8060008114611aaf576040519150601f19603f3d011682016040523d82523d6000602084013e611ab4565b606091505b506000815103611af9576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401611af090612b59565b60405180910390fd5b805181602001fd5b63150b7a0260e01b7bffffffffffffffffffffffffffffffffffffffffffffffffffffffff1916817bffffffffffffffffffffffffffffffffffffffffffffffffffffffff191614915050611b56565b600190505b949350505050565b6000808273ffffffffffffffffffffffffffffffffffffffff163b119050919050565b6000604051905090565b600080fd5b600080fd5b60007fffffffff0000000000000000000000000000000000000000000000000000000082169050919050565b611bca81611b95565b8114611bd557600080fd5b50565b600081359050611be781611bc1565b92915050565b600060208284031215611c0357611c02611b8b565b5b6000611c1184828501611bd8565b91505092915050565b60008115159050919050565b611c2f81611c1a565b82525050565b6000602082019050611c4a6000830184611c26565b92915050565b600081519050919050565b600082825260208201905092915050565b60005b83811015611c8a578082015181840152602081019050611c6f565b60008484015250505050565b6000601f19601f8301169050919050565b6000611cb282611c50565b611cbc8185611c5b565b9350611ccc818560208601611c6c565b611cd581611c96565b840191505092915050565b60006020820190508181036000830152611cfa8184611ca7565b905092915050565b6000819050919050565b611d1581611d02565b8114611d2057600080fd5b50565b600081359050611d3281611d0c565b92915050565b600060208284031215611d4e57611d4d611b8b565b5b6000611d5c84828501611d23565b91505092915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000611d9082611d65565b9050919050565b611da081611d85565b82525050565b6000602082019050611dbb6000830184611d97565b92915050565b611dca81611d85565b8114611dd557600080fd5b50565b600081359050611de781611dc1565b92915050565b60008060408385031215611e0457611e03611b8b565b5b6000611e1285828601611dd8565b9250506020611e2385828601611d23565b9150509250929050565b600080600060608486031215611e4657611e45611b8b565b5b6000611e5486828701611dd8565b9350506020611e6586828701611dd8565b9250506040611e7686828701611d23565b9150509250925092565b600060208284031215611e9657611e95611b8b565b5b6000611ea484828501611dd8565b91505092915050565b611eb681611d02565b82525050565b6000602082019050611ed16000830184611ead565b92915050565b600081519050919050565b600082825260208201905092915050565b6000819050602082019050919050565b611f0c81611d02565b82525050565b6000611f1e8383611f03565b60208301905092915050565b6000602082019050919050565b6000611f4282611ed7565b611f4c8185611ee2565b9350611f5783611ef3565b8060005b83811015611f88578151611f6f8882611f12565b9750611f7a83611f2a565b925050600181019050611f5b565b5085935050505092915050565b60006020820190508181036000830152611faf8184611f37565b905092915050565b611fc081611c1a565b8114611fcb57600080fd5b50565b600081359050611fdd81611fb7565b92915050565b60008060408385031215611ffa57611ff9611b8b565b5b600061200885828601611dd8565b925050602061201985828601611fce565b9150509250929050565b600080fd5b600080fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b61206582611c96565b810181811067ffffffffffffffff821117156120845761208361202d565b5b80604052505050565b6000612097611b81565b90506120a3828261205c565b919050565b600067ffffffffffffffff8211156120c3576120c261202d565b5b6120cc82611c96565b9050602081019050919050565b82818337600083830152505050565b60006120fb6120f6846120a8565b61208d565b90508281526020810184848401111561211757612116612028565b5b6121228482856120d9565b509392505050565b600082601f83011261213f5761213e612023565b5b813561214f8482602086016120e8565b91505092915050565b6000806000806080858703121561217257612171611b8b565b5b600061218087828801611dd8565b945050602061219187828801611dd8565b93505060406121a287828801611d23565b925050606085013567ffffffffffffffff8111156121c3576121c2611b90565b5b6121cf8782880161212a565b91505092959194509250565b600067ffffffffffffffff8211156121f6576121f561202d565b5b6121ff82611c96565b9050602081019050919050565b600061221f61221a846121db565b61208d565b90508281526020810184848401111561223b5761223a612028565b5b6122468482856120d9565b509392505050565b600082601f83011261226357612262612023565b5b813561227384826020860161220c565b91505092915050565b6000806040838503121561229357612292611b8b565b5b60006122a185828601611dd8565b925050602083013567ffffffffffffffff8111156122c2576122c1611b90565b5b6122ce8582860161224e565b9150509250929050565b600080604083850312156122ef576122ee611b8b565b5b60006122fd85828601611dd8565b925050602061230e85828601611dd8565b9150509250929050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b6000600282049050600182168061235f57607f821691505b60208210810361237257612371612318565b5b50919050565b7f4552433732313a20617070726f76616c20746f2063757272656e74206f776e6560008201527f7200000000000000000000000000000000000000000000000000000000000000602082015250565b60006123d4602183611c5b565b91506123df82612378565b604082019050919050565b60006020820190508181036000830152612403816123c7565b9050919050565b7f4552433732313a20617070726f76652063616c6c6572206973206e6f7420746f60008201527f6b656e206f776e6572206f7220617070726f76656420666f7220616c6c000000602082015250565b6000612466603d83611c5b565b91506124718261240a565b604082019050919050565b6000602082019050818103600083015261249581612459565b9050919050565b7f4552433732313a2063616c6c6572206973206e6f7420746f6b656e206f776e6560008201527f72206f7220617070726f76656400000000000000000000000000000000000000602082015250565b60006124f8602d83611c5b565b91506125038261249c565b604082019050919050565b60006020820190508181036000830152612527816124eb565b9050919050565b7f4552433732313a20696e76616c696420746f6b656e2049440000000000000000600082015250565b6000612564601883611c5b565b915061256f8261252e565b602082019050919050565b6000602082019050818103600083015261259381612557565b9050919050565b7f4552433732313a207472616e736665722063616c6c6572206973206e6f74206f60008201527f776e6572206e6f7220617070726f766564000000000000000000000000000000602082015250565b60006125f6603183611c5b565b91506126018261259a565b604082019050919050565b60006020820190508181036000830152612625816125e9565b9050919050565b7f4552433732313a207472616e73666572206e6f6e6578697374656e7420746f6b60008201527f656e000000000000000000000000000000000000000000000000000000000000602082015250565b6000612688602283611c5b565b91506126938261262c565b604082019050919050565b600060208201905081810360008301526126b78161267b565b9050919050565b7f4552433732313a2061646472657373207a65726f206973206e6f74206120766160008201527f6c6964206f776e65720000000000000000000000000000000000000000000000602082015250565b600061271a602983611c5b565b9150612725826126be565b604082019050919050565b600060208201905081810360008301526127498161270d565b9050919050565b7f4552433732313a206f776e657220717565727920666f72206e6f6e657869737460008201527f656e7420746f6b656e0000000000000000000000000000000000000000000000602082015250565b60006127ac602983611c5b565b91506127b782612750565b604082019050919050565b600060208201905081810360008301526127db8161279f565b9050919050565b7f4552433732314d657461646174613a2055524920717565727920666f72206e6f60008201527f6e6578697374656e7420746f6b656e0000000000000000000000000000000000602082015250565b600061283e602f83611c5b565b9150612849826127e2565b604082019050919050565b6000602082019050818103600083015261286d81612831565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b60006128ae82611d02565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82036128e0576128df612874565b5b600182019050919050565b7f4552433732313a207472616e736665722066726f6d20696e636f72726563742060008201527f6f776e6572000000000000000000000000000000000000000000000000000000602082015250565b6000612947602583611c5b565b9150612952826128eb565b604082019050919050565b600060208201905081810360008301526129768161293a565b9050919050565b7f4552433732313a207472616e7366657220746f20746865207a65726f2061646460008201527f7265737300000000000000000000000000000000000000000000000000000000602082015250565b60006129d9602483611c5b565b91506129e48261297d565b604082019050919050565b60006020820190508181036000830152612a08816129cc565b9050919050565b7f4f776e61626c653a2063616c6c6572206973206e6f7420746865206f776e6572600082015250565b6000612a45602083611c5b565b9150612a5082612a0f565b602082019050919050565b60006020820190508181036000830152612a7481612a38565b9050919050565b7f4552433732313a20617070726f766520746f2063616c6c657200000000000000600082015250565b6000612ab1601983611c5b565b9150612abc82612a7b565b602082019050919050565b60006020820190508181036000830152612ae081612aa4565b9050919050565b7f4552433732313a207472616e7366657220746f206e6f6e20455243373231526560008201527f63656976657220696d706c656d656e7465720000000000000000000000000000602082015250565b6000612b43603283611c5b565b9150612b4e82612ae7565b604082019050919050565b60006020820190508181036000830152612b7281612b36565b9050919050565b7f4552433732313a206d696e7420746f20746865207a65726f2061646472657373600082015250565b6000612baf602083611c5b565b9150612bba82612b79565b602082019050919050565b60006020820190508181036000830152612bde81612ba2565b9050919050565b7f4552433732313a20746f6b656e20616c7265616479206d696e74656400000000600082015250565b6000612c1b601c83611c5b565b9150612c2682612be5565b602082019050919050565b60006020820190508181036000830152612c4a81612c0e565b9050919050565b7f4552433732314d657461646174613a2055524920736574206f66206e6f6e657860008201527f697374656e7420746f6b656e0000000000000000000000000000000000000000602082015250565b6000612cad602c83611c5b565b9150612cb882612c51565b604082019050919050565b60006020820190508181036000830152612cdc81612ca0565b9050919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b600060088302612d457fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82612d08565b612d4f8683612d08565b95508019841693508086168417925050509392505050565b6000819050919050565b6000612d8c612d87612d8284611d02565b612d67565b611d02565b9050919050565b6000819050919050565b612da683612d71565b612dba612db282612d93565b848454612d15565b825550505050565b600090565b612dcf612dc2565b612dda818484612d9d565b505050565b5b81811015612dfe57612df3600082612dc7565b600181019050612de0565b5050565b601f821115612e4357612e1481612ce3565b612e1d84612cf8565b81016020851015612e2c578190505b612e40612e3885612cf8565b830182612ddf565b50505b505050565b600082821c905092915050565b6000612e6660001984600802612e48565b1980831691505092915050565b6000612e7f8383612e55565b9150826002028217905092915050565b612e9882611c50565b67ffffffffffffffff811115612eb157612eb061202d565b5b612ebb8254612347565b612ec6828285612e02565b600060209050601f831160018114612ef95760008415612ee7578287015190505b612ef18582612e73565b865550612f59565b601f198416612f0786612ce3565b60005b82811015612f2f57848901518255600182019150602085019450602081019050612f0a565b86831015612f4c5784890151612f48601f891682612e55565b8355505b6001600288020188555050505b505050505050565b7f4f776e61626c653a206e6577206f776e657220697320746865207a65726f206160008201527f6464726573730000000000000000000000000000000000000000000000000000602082015250565b6000612fbd602683611c5b565b9150612fc882612f61565b604082019050919050565b60006020820190508181036000830152612fec81612fb0565b9050919050565b600081519050919050565b600082825260208201905092915050565b600061301a82612ff3565b6130248185612ffe565b9350613034818560208601611c6c565b61303d81611c96565b840191505092915050565b600060808201905061305d6000830187611d97565b61306a6020830186611d97565b6130776040830185611ead565b8181036060830152613089818461300f565b905095945050505050565b6000815190506130a381611bc1565b92915050565b6000602082840312156130bf576130be611b8b565b5b60006130cd84828501613094565b9150509291505056fea26469706673582212204d47aa8603e2624f238276722244be42a4f355a604ad7842b811374887c41f9164736f6c63430008120033"})
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
  