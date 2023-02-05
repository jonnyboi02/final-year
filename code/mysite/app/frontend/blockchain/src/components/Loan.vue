<template>
    <h2>Request loan</h2>
    <div>
        Amount Requested: <input v-model="funds.requestedLoan"/>
    </div>
    <div>
        Upload NFT:<input @change="uploadFile" type = "file" ref="fileInput" />
        
    </div>
    <button @click='submitFile'>Request Loan</button>

</template>

<script>
export default{
    data(){
        return{
            file: null,
            username: '',
            funds:{
                requestedLoan: 0,
            }
        }
    },
    methods:{
        uploadFile(){
            this.file = this.$refs.fileInput.files[0]
        },
        submitFile(){
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('username', this.username)
            fetch("url", {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
            .catch(error => {
                console.error(error)
            })
        }
    }

}

</script>