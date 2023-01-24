<template>
    <h2>Send Ether</h2>
    <div>
        <div>
            Recipient key: <input v-model = "recipient"/>
        </div>
        <div>
            Ether to send: <input v-model = 'funds'/>
        </div>

        <button onclick=""></button>

    </div>

</template>

<script>
export default{
    data(){

        return{
            recipient:"",
            funds: "",


        }
    }
}

</script>