<template>
    <div>
      <h2>List of Smart Contracts on the Geth Node</h2>
      <button @click="created">Get List</button>
      <ul>
        <li v-for="address in contractAddresses" :key="address">{{ address }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import Web3 from 'web3';
  
  export default {
    data() {
      return {
        contractAddresses: [],
      };
    },
  
    async created() {
      try {
        // Create a new Web3 instance and connect to a local Geth node
        const web3 = new Web3('http://localhost:8547');
  
        // Get the latest block number
        const latestBlock = await web3.eth.getBlockNumber();
  
        // Loop through all the blocks and transactions to find the contract addresses
        for (let i = 0; i <= latestBlock; i++) {
          const block = await web3.eth.getBlock(i, true);
  
          if (block) {
            block.transactions.forEach((tx) => {
              if (tx.to === null) {
                this.contractAddresses.push(tx.contractAddress);
              }
            });
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
  };
  </script>
  