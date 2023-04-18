<template>
    <div id='details'>
      <h2>Loan Requests</h2>
      <div class="requests">
        <div class="request-list">
          <h2>Waiting Loans</h2>
          <nav id="lists" style=" padding-top: 20px;">
            <ul v-if="waitingLoans && waitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in waitingLoans" :key="lender" :value="lender" @click="selectWaitItem(index)" style="padding: 2px; border-style: solid; border-radius: 20px; padding-left: 20px; padding-right: 15px;  ">
                    {{  lender.collateralHolder }} Loan {{ lender.id }}
                </li>
              </div>
            </ul>
           
          </nav>

        </div>
        <div class="request-list">
          <h2>Non-waiting Loans</h2>
          <nav id="lists" style=" padding-top: 20px;">
            <ul v-if="nonWaitingLoans && nonWaitingLoans.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(lender, index) in nonWaitingLoans" :key="lender" :value="lender" @click="selectNonWaitItem(index)" style="padding: 2px; border-style: solid; border-radius: 20px; align: center; padding-left: 20px; padding-right: 15px; ">
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
            <button class = 'buttons'>View NFT</button>
        </div>

        {{ tokens }}
        {{ uri }}
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
      };
    },
    async mounted() {
      await this.getLoans();
    },
    methods: {
        async rejectLoan(){
            try{
                let response = await fetch("http://127.0.0.1:8000/reject_loan/", {
                    method: 'POST',
                    body: JSON.stringify({
                        'id':this.loanRequest.id
                    })
                })
                let data = await response.json()
                this.$router.go(0)
            }catch(error){
                console.log(error)
            }

        },

        async sendTransaction(){

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
                const uri = await contract.methods.tokenURI(tokenIds[tokenIds.length-1]).call()
                this.uri = uri

                //await web3.eth.personal.unlockAccount(account, localStorage.getItem('password'), 600);
               

                //let d = await contract.methods.transferFrom(account,contract.options.address ,tokenIds[tokenIds.length-1]) .send({from: account})

                Toastify({
                text: "NFT uploaded "+this.contract.address + "with uri "+uri,
                position: "center",
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
            this.form.collateralUrl= this.tokens[this.tokens.length-1]
            this.form.price= this.loanRequest.price

            
            const web3 = new Web3("http://localhost:8547");
            const accounts = await web3.eth.getAccounts();
            const networkId = await web3.eth.net.getId();
            
            
            const LoanContract = new web3.eth.Contract(LoanABI, null, { data: "60806040523480156200001157600080fd5b5060405162001623380380620016238339818101604052810190620000379190620003a7565b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508660028190555085600381905550846004819055508360078190555082600860006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508160099081620001269190620006ba565b5080600a81905550600454426200013e9190620007d0565b6005819055506000600660006101000a81548160ff0219169083151502179055506000600b81905550505050505050506200080b565b6000604051905090565b600080fd5b600080fd5b6000819050919050565b6200019d8162000188565b8114620001a957600080fd5b50565b600081519050620001bd8162000192565b92915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000620001f082620001c3565b9050919050565b6200020281620001e3565b81146200020e57600080fd5b50565b6000815190506200022281620001f7565b92915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6200027d8262000232565b810181811067ffffffffffffffff821117156200029f576200029e62000243565b5b80604052505050565b6000620002b462000174565b9050620002c2828262000272565b919050565b600067ffffffffffffffff821115620002e557620002e462000243565b5b620002f08262000232565b9050602081019050919050565b60005b838110156200031d57808201518184015260208101905062000300565b60008484015250505050565b6000620003406200033a84620002c7565b620002a8565b9050828152602081018484840111156200035f576200035e6200022d565b5b6200036c848285620002fd565b509392505050565b600082601f8301126200038c576200038b62000228565b5b81516200039e84826020860162000329565b91505092915050565b600080600080600080600060e0888a031215620003c957620003c86200017e565b5b6000620003d98a828b01620001ac565b9750506020620003ec8a828b01620001ac565b9650506040620003ff8a828b01620001ac565b9550506060620004128a828b01620001ac565b9450506080620004258a828b0162000211565b93505060a088015167ffffffffffffffff81111562000449576200044862000183565b5b620004578a828b0162000374565b92505060c06200046a8a828b01620001ac565b91505092959891949750929550565b600081519050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680620004cc57607f821691505b602082108103620004e257620004e162000484565b5b50919050565b60008190508160005260206000209050919050565b60006020601f8301049050919050565b600082821b905092915050565b6000600883026200054c7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff826200050d565b6200055886836200050d565b95508019841693508086168417925050509392505050565b6000819050919050565b60006200059b620005956200058f8462000188565b62000570565b62000188565b9050919050565b6000819050919050565b620005b7836200057a565b620005cf620005c682620005a2565b8484546200051a565b825550505050565b600090565b620005e6620005d7565b620005f3818484620005ac565b505050565b5b818110156200061b576200060f600082620005dc565b600181019050620005f9565b5050565b601f8211156200066a576200063481620004e8565b6200063f84620004fd565b810160208510156200064f578190505b620006676200065e85620004fd565b830182620005f8565b50505b505050565b600082821c905092915050565b60006200068f600019846008026200066f565b1980831691505092915050565b6000620006aa83836200067c565b9150826002028217905092915050565b620006c58262000479565b67ffffffffffffffff811115620006e157620006e062000243565b5b620006ed8254620004b3565b620006fa8282856200061f565b600060209050601f8311600181146200073257600084156200071d578287015190505b6200072985826200069c565b86555062000799565b601f1984166200074286620004e8565b60005b828110156200076c5784890151825560018201915060208501945060208101905062000745565b868310156200078c578489015162000788601f8916826200067c565b8355505b6001600288020188555050505b505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000620007dd8262000188565b9150620007ea8362000188565b9250828201905080821115620008055762000804620007a1565b5b92915050565b610e08806200081b6000396000f3fe6080604052600436106100f75760003560e01c806392d09ceb1161008a578063aa8c217c11610059578063aa8c217c146103e5578063bcead63e14610410578063d524b0ff1461043b578063e27facdc14610466576101f6565b806392d09ceb14610330578063a035b1fe1461035b578063a3b9e39d14610386578063a6f9dae1146103bc576101f6565b806357f7d74f116100c657806357f7d74f146102865780636164051a146102af578063786716fe146102da5780638da5cb5b14610305576101f6565b80630b168f21146101fb5780630fb5a6b4146102265780632c4e722e14610251578063330aec3e1461027c576101f6565b366101f657600660009054906101000a900460ff161561014c576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101439061094f565b60405180910390fd5b600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146101dc576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101d3906109bb565b60405180910390fd5b34600b60008282546101ee9190610a14565b925050819055005b600080fd5b34801561020757600080fd5b50610210610491565b60405161021d9190610ac7565b60405180910390f35b34801561023257600080fd5b5061023b61051f565b6040516102489190610af8565b60405180910390f35b34801561025d57600080fd5b50610266610525565b6040516102739190610af8565b60405180910390f35b61028461052b565b005b34801561029257600080fd5b506102ad60048036038101906102a89190610b76565b610636565b005b3480156102bb57600080fd5b506102c46106ba565b6040516102d19190610bbe565b60405180910390f35b3480156102e657600080fd5b506102ef6106cd565b6040516102fc9190610af8565b60405180910390f35b34801561031157600080fd5b5061031a6106d3565b6040516103279190610be8565b60405180910390f35b34801561033c57600080fd5b506103456106f9565b6040516103529190610af8565b60405180910390f35b34801561036757600080fd5b506103706106ff565b60405161037d9190610af8565b60405180910390f35b34801561039257600080fd5b5061039b610705565b6040516103b39c9b9a99989796959493929190610c03565b60405180910390f35b3480156103c857600080fd5b506103e360048036038101906103de9190610b76565b610858565b005b3480156103f157600080fd5b506103fa61089c565b6040516104079190610af8565b60405180910390f35b34801561041c57600080fd5b506104256108a2565b6040516104329190610be8565b60405180910390f35b34801561044757600080fd5b506104506108c6565b60405161045d9190610af8565b60405180910390f35b34801561047257600080fd5b5061047b6108cc565b6040516104889190610be8565b60405180910390f35b6009805461049e90610cf3565b80601f01602080910402602001604051908101604052809291908181526020018280546104ca90610cf3565b80156105175780601f106104ec57610100808354040283529160200191610517565b820191906000526020600020905b8154815290600101906020018083116104fa57829003601f168201915b505050505081565b60045481565b60035481565b670de0b6b3a76400006002546105419190610d24565b600354670de0b6b3a764000060025461055a9190610d24565b6105649190610d24565b61056e9190610a14565b4710156105b0576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105a790610db2565b60405180910390fd5b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc479081150290604051600060405180830381858888f19350505050158015610618573d6000803e3d6000fd5b506001600660006101000a81548160ff021916908315150217905550565b806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b600660009054906101000a900460ff1681565b60055481565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60075481565b600a5481565b6000806000806000806000806000606060008060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600254600354600454600554600660009054906101000a900460ff16600754600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166009600a54600b548280546107b290610cf3565b80601f01602080910402602001604051908101604052809291908181526020018280546107de90610cf3565b801561082b5780601f106108005761010080835404028352916020019161082b565b820191906000526020600020905b81548152906001019060200180831161080e57829003601f168201915b505050505092509b509b509b509b509b509b509b509b509b509b509b509b50909192939495969798999a9b565b80600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b60025481565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600b5481565b600860009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b600082825260208201905092915050565b7f4c6f616e20697320616c72656164792072657061696400000000000000000000600082015250565b60006109396016836108f2565b915061094482610903565b602082019050919050565b600060208201905081810360008301526109688161092c565b9050919050565b7f4f6e6c7920626f72726f7765722063616e206d616b652072657061796d656e74600082015250565b60006109a56020836108f2565b91506109b08261096f565b602082019050919050565b600060208201905081810360008301526109d481610998565b9050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000610a1f826109db565b9150610a2a836109db565b9250828201905080821115610a4257610a416109e5565b5b92915050565b600081519050919050565b60005b83811015610a71578082015181840152602081019050610a56565b60008484015250505050565b6000601f19601f8301169050919050565b6000610a9982610a48565b610aa381856108f2565b9350610ab3818560208601610a53565b610abc81610a7d565b840191505092915050565b60006020820190508181036000830152610ae18184610a8e565b905092915050565b610af2816109db565b82525050565b6000602082019050610b0d6000830184610ae9565b92915050565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610b4382610b18565b9050919050565b610b5381610b38565b8114610b5e57600080fd5b50565b600081359050610b7081610b4a565b92915050565b600060208284031215610b8c57610b8b610b13565b5b6000610b9a84828501610b61565b91505092915050565b60008115159050919050565b610bb881610ba3565b82525050565b6000602082019050610bd36000830184610baf565b92915050565b610be281610b38565b82525050565b6000602082019050610bfd6000830184610bd9565b92915050565b600061018082019050610c19600083018f610bd9565b610c26602083018e610bd9565b610c33604083018d610ae9565b610c40606083018c610ae9565b610c4d608083018b610ae9565b610c5a60a083018a610ae9565b610c6760c0830189610baf565b610c7460e0830188610ae9565b610c82610100830187610bd9565b818103610120830152610c958186610a8e565b9050610ca5610140830185610ae9565b610cb3610160830184610ae9565b9d9c50505050505050505050505050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b60006002820490506001821680610d0b57607f821691505b602082108103610d1e57610d1d610cc4565b5b50919050565b6000610d2f826109db565b9150610d3a836109db565b9250828202610d48816109db565b91508282048414831517610d5f57610d5e6109e5565b5b5092915050565b7f42616c616e6365206e6f742073756666696369656e7400000000000000000000600082015250565b6000610d9c6016836108f2565b9150610da782610d66565b602082019050919050565b60006020820190508181036000830152610dcb81610d8f565b905091905056fea2646970667358221220ad1c2b9f4db2f84bf5c1544617fa7eb572a3478d5a19c520df02c5b692fda0cf64736f6c63430008120033" });

            const gas = 3000000; // Set the gas limit to 3000000
            // const options = {
            //     from: accounts[0],
            //     gas: gas, // Pass the gas limit to the send method
            // };

            const args = [
                this.form.amount,
                this.form.rate,
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
                Toastify({
                            text: 'Deploying for '+this.form.collateralHolder,
                            backgroundColor: "green",
                            position: "center",
                        }).showToast();
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
                            text: `Deployed loan contract address: ` + this.loanContractAddress + " " + this.form.collateralHolder,
                            backgroundColor: "green",
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
            
            return;
                    
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
    border-radius: 25px;

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
}

#loanDetails{
    border-style: solid;
    border-color: white;
    margin-top: 15px;
    border-radius: 25px;
    border-width: thin;
}

.buttons{
    margin-right: 20px;
    padding: 10px;
}
  </style>
  