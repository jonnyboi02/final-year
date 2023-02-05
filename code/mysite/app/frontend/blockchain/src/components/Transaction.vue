<template>
    <h2>Send Ether</h2>
    <div>
        <div>
            Recipient key: <input v-model = "user['recipient']"/>
        </div>
        <div>
            Ether to send: <input v-model = "user['funds']"/>
        </div>

        <button onclick=""></button>

    </div>

</template>

<script>
export default{
    data(){
        return{
            user: {
                recipient:"",
                funds: "",
            }

        }
    },
    methods:{
        sendTransaction(){
            
            


        }
    }
}

</script>