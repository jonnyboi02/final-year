
<template>
  <GetAccounts/>
  <Register/>
  <CreateAccount/>
  <!-- <Loan/> -->
  <SendWei/>


</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Register from './components/Register.vue'
import Loan from './components/Loan.vue'
import GetAccounts from './components/GetAccounts.vue'
import CreateAccount from './components/CreateAccount.vue'
import SendWei from './components/SendWei.vue'

export default{
  components:{
    Register,
    Loan,
    GetAccounts,
    CreateAccount,
    SendWei,
  },
}
</script>
