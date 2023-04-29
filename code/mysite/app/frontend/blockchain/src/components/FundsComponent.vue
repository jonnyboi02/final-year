<template>
  <div>
    <div id='details' style="background-color: transparent; box-shadow: none; border-color: transparent;">
      
      <div class="requests"  style="">
        <div class="request-list" style="width: 450px;">
          <h2>Details</h2>
        <div class="request-box" style="padding-left: 80px;">
      <form @submit.prevent="submitForm">
        <div class="user-box">
          <input type="text" v-model="description" required>
          <label>Description</label>
        </div>
        <div class="user-box">
          <input type="text" v-model="amount" required>
          <label>Number of NFTs</label>
        </div>
        <div class="user-box">
          <input type="file" ref="fileInput" @change="handleFileUpload">
          <label>Image</label>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
    </div>
        <div class="request-list">
          <h2>Asset Evaluations</h2>
          <nav id="lists" style=" padding-top: 10px; height: 220px;">
            <ul v-if="negotiations && negotiations.length > 0"  >
              <div style="padding-bottom: 100px;">
                <li v-for="(negotiation, index) in negotiations" :key="negotiation" :value="negotiation"  :class="{'selected': isSelected(index)}" @click="selectNFT(index)" style="width: 330px;padding: 2px; border-style: solid; border-radius: 10px; align: center; padding-left: 10px; padding-right: 15px; ">
                  {{  negotiation.collateralHolder }} Request {{ negotiation.id }}
                </li>
              </div>
            </ul>
           
          </nav>
          <div v-if="currentNftRequest" style="margin-top: 20px;">
            <button @click="viewAsset">View Asset</button>
          </div>
        </div>
      </div>
      </div>
    
  </div>
</template>

<script>

import Web3 from 'web3';
  import Toastify from 'toastify-js';
  import 'toastify-js/src/toastify.css';
export default {
  data() {
    return {
      selected: -1,
      description: '',
      file: null,
      amount: '',
      senderAddress: "",
      negotiations: [],
      nftindex: 0,
      currentNftRequest: null,
    };
  },
  computed:{
  
    isSelected() {
      return (index) => index === this.selected;
    }
  },
  async mounted(){
    await this.getAddress();
    await this.getNegotiations();
  },
  methods: {
    viewAsset(){
      window.location.href = "http://localhost:8000/media/" + this.currentNftRequest.photo;
    },
    selectNFT(index){
      this.selected = index;
      this.nftindex = index;
      this.currentNftRequest = this.negotiations[index];
      var currentNegotiation = this.currentNftRequest;
      var message = "Details of Asset Evaluation\nRequest ID: " + this.currentNftRequest.id + "\n" +
              "Requester: " + this.currentNftRequest.user + "\n" +
              "Picture: " + (this.currentNftRequest.photo ? 'http://localhost:8000/media/' + this.currentNftRequest.photo : "") + "\n" +
              "NFTs requested: " + this.currentNftRequest.amount + "\n" +
              "Description: " + this.currentNftRequest.description + "\n" +
              "Agreed? " + (this.currentNftRequest.accepted ? "Yes" : "No");
      Toastify({
          text: message,
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
          position: "center",
          duration: 5000,

        }).showToast();
    },
    async getNegotiations(){
          fetch('http://127.0.0.1:8000/get_negotiations/')
            .then(response => response.json())
            .then(data => {
              this.negotiations = data;
              this.negotiations = this.negotiations.filter((cur)=> cur.user.toLowerCase() === this.senderAddress.toLowerCase())
            })
            .catch(error => console.log(error));

            console.log(this.negotiations.length)
        },
    async getAddress() {
        const response = await fetch("http://127.0.0.1:8000/get_address/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: localStorage.getItem("username"),
          }),
        });
        const data = await response.json();
        if (data.error) {
          console.log(error);
        } else {
          this.senderAddress = data.key;
          this.senderPassword = localStorage.getItem("password");
        }
      },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    //submits the negotiation request.
    async submitForm() {
      const formData = new FormData();
      
      formData.append('amount',this.amount);
      formData.append('password', localStorage.getItem('password'))
      formData.append('user', this.senderAddress);
      formData.append('customer_offer', "True");
      formData.append('bank_offer', "False");
      formData.append('photo', this.file);
      formData.append('description', this.description);
     
      
      //formData.append('bank_offer', "False");
      Toastify({
                        text: "Request Made",
                        
                        close: true,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                        
            }).showToast();



      const response = await fetch('http://127.0.0.1:8000/create_negotiation/', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      console.log(data);

    }
  }
};
</script>




<style>
.selected {
  background-color: #ccc;
}

.request-box {

  top: 40%;
  left: 50%;
  width: 400px;
  padding: 40px;

 /* background: rgba(0,0,0,.6); */
  box-sizing: border-box;
  /* box-shadow: 0 15px 10px rgba(0,0,0,.6); */
  border-radius: 10px;

}

.request-box h2 {
  margin: 0 0 30px;
  padding: 0;
  color: #fff;
  text-align: center;
}

.request-box .user-box {
  position: relative;
}

.request-box .user-box input {
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

.request-box .user-box label {
  position: absolute;
  top:0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: .5s;
}

.request-box .user-box input:focus ~ label,
.request-box .user-box input:valid ~ label {
  top: -24px;
  left: 0;
  color: #f68e44;
  font-size: 12px;
}

.request-box form a {
  position: relative;
  display: inline-block;
  padding: 10px 10px;
  color: #b79726;
  font-size: 16px;
  text-decoration: none;
  text-transform: uppercase;
  overflow: hidden;
  transition: .5s;
  margin-top: 40px;
  letter-spacing: 4px
}

.request-box a:hover {
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              0 0 50px #f4e403,
              0 0 100px #d5cf1e;
}

.request-box a span {
  position: absolute;
  display: block;
}

.request-box a span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f4c003);
  animation: btn-anim1 1s linear infinite;
}

@keyframes btn-anim1 {
  0% {
    left: -100%;
  }
  50%,100% {
    left: 100%;
  }
}

.request-box a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #f4bc03);
  animation: btn-anim2 1s linear infinite;
  animation-delay: .25s
}

@keyframes btn-anim2 {
  0% {
    top: -100%;
  }
  50%,100% {
    top: 100%;
  }
}

.request-box a span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #f4dc03);
  animation: btn-anim3 1s linear infinite;
  animation-delay: .5s
}

@keyframes btn-anim3 {
  0% {
    right: -100%;
  }
  50%,100% {
    right: 100%;
  }
}

.request-box a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #f4b003);
  animation: btn-anim4 1s linear infinite;
  animation-delay: .75s
}

@keyframes btn-anim4 {
  0% {
    bottom: -100%;
  }
  50%,100% {
    bottom: 100%;
  }
}


</style>