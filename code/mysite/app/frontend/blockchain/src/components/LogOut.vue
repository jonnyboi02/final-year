<template>
  <div>
    <!-- your other component code here -->
    <button @click="logout">Are you sure to Log out?</button>
  </div>
</template>

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
    
