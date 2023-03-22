import {reactive} from "vue";

export const user = reactive({
    isAuthenticated: false,
    authToken: '',
    username: '',
    init(){
        if (localStorage.getItem('isAuthenticated')) {
          try {
            this.isAuthenticated = JSON.parse(localStorage.getItem('isAuthenticated'));
          } catch(e) {
            localStorage.removeItem('isAuthenticated');
          }
        }
        if (localStorage.getItem('authToken')) {
          try {
            this.authToken = JSON.parse(localStorage.getItem('authToken'));
          } catch(e) {
            localStorage.removeItem('authToken');
          }
        }
        console.log(user);
    },
    setUserName(username){
        this.username = username;
    },
    setIsAuthenticated(authenticatedState) {
        this.isAuthenticated = authenticatedState;
        const parsed = JSON.stringify(this.isAuthenticated);
        localStorage.setItem('isAuthenticated', parsed);
    },
    setAuthToken(token) {
        this.authToken = token;
        const parsed = JSON.stringify(this.authToken);
        localStorage.setItem('authToken', parsed);
    }
});
