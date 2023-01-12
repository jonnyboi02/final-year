<template>
    Hi

    <div>
        <form ref="form">
            <div>
            Username:<input class = 'form-control' v-model='form["username"]' />
            </div> 
            <div>
            Password:<input class = 'form-control' type = 'password' v-model='form["password"]'/>
            </div>
            <button @click="registerUser">Register</button>

        </form>
    </div>

    

</template>

<script>





export default{
    data(){
        return{
            form:{
                username : "",
                password : "",
            },

        }
    },
    methods :{
        async registerUser(){
            response = fetch("http://127.0.0.1:8000/register/", {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form),
            })
            if (reponse.status === 400){
                alert("User already exists!")
            } 
            else{
                alert("Account created")
            }
        
        },

    }

}

</script>