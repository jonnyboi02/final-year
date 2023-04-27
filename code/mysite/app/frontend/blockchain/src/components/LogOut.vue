<template>
  <div style="padding: 10px;   position: absolute;
  top: 40%;
  left: 50%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
 background: rgba(0,0,0,.6);
  box-sizing: border-box;
  box-shadow: 0 15px 10px rgba(0,0,0,.6);
  border-radius: 10px;
  margin-top: -180px">
    <!-- your other component code here -->
    <a  id = 'logout' type="submit" @click="registerUser">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                Are you sure to Log out?
            </a>
    <!-- <button @click="logout">Are you sure to Log out?</button> -->
  </div>
</template>
<style>

#logout{
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

#logout:hover{
  background: #f49803;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #f4c803,
              0 0 10px #bd9d0b,
              0 0 50px #f4e403,
              0 0 100px #d5cf1e;
}



</style>
<script>
    export default {
      methods: {
        logout() {
          localStorage.removeItem('token');
          localStorage.removeItem('username');
          this.$router.replace('/login');
        },
        created() {
            window.addEventListener('beforeunload', this.logout);
        },
        destroyed() {
            window.removeEventListener('beforeunload', this.logout);
        },
      },
    };
    
    </script>
    
