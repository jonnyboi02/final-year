<template>
    <div id="funds">
      <h2>Balance</h2>
      <template v-if="loading">
        <p>Loading...</p>
      </template>
      <template v-else>
        <p> You currently have: {{ balance }} ETH. </p>
      </template>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      shouldRender: {
        type: Boolean,
        required: true,
      },
    },
    data() {
      return {
        senderAddress: localStorage.getItem("username")
          ? localStorage.getItem("username")
          : "0x13ca48E880D7A28F4648eEd3B1Dc558E0D0Dc264",
        senderPassword: "123456789",
        recipientAddress: "0xc63AB01569680E6388A7B4EbbdBaf260be9870dc",
        value: "0x20000000000000000000",
        balance: null,
        loading: true,
      };
    },
    async mounted() {
      try {
        await this.getAddress();
        await this.getBalance();
        this.loading = false;
      } catch (error) {
        console.error(error);
        this.loading = false;
      }
    },
    methods: {
      getBalance() {
        // Make a GET request to the Django view URL with the account parameter
        return fetch(`http://localhost:8000/eth_balance/${this.senderAddress}/`)
          .then((response) => response.json())
          .then((data) => {
            if (data.error) {
              console.error(data.error);
            } else {
              this.balance = data.balance;
            }
          })
          .catch((error) => console.error(error));
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
    },
    watch: {
      shouldRender() {
        // Listen for changes to the shouldRender prop and trigger a re-render of the component
        this.getBalance();
      },
    },
  };
  </script>
  