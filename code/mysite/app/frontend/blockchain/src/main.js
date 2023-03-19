import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {createRouter, createWebHashHistory} from 'vue-router'
//import {createApp} from "vue";
import Register from "./components/Register.vue"
import SendWei from './components/SendWei.vue'
import CreateAccount from './components/CreateAccount.vue'
import Login from './components/Login.vue'
import GetBalance from './components/GetBalance.vue'
import RequestLoan from './components/RequestLoan.vue'
import Contracts from './components/Contracts.vue'
export function logout() {
    localStorage.removeItem('token'); // remove the token from localStorage
}

const routes = [
    // { path: '/', component: Home },
    {path: '/login', component: Login, name: "Login"},
    {path: '/transaction', component: SendWei, name: "Send Transaction"},
    {path: '/create_account', component: CreateAccount, name: "Create Account"},
    {path: '/register', component: Register, name: "Register"},
    {path: '/eth_balance', component: GetBalance, name: "Balance"},
    {path: '/deploy_contract', component: RequestLoan, name: "Request Loan"},
    {path: '/contracts', component: Contracts, name: "Contracts"},
    {
        path: '/logout',
        name: 'Logout',
        beforeEnter: (to, from, next) => {
          logout().then(() => {
              // Redirect to the login page
              next('/login');
            })
            .catch(error => console.error(error));
        },
      },

  
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

const app = createApp(App).use(router) // mounting root instance
app.mount('#app')
