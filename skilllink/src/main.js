import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import GoogleSignInPlugin from "vue3-google-signin";

const app = createApp(App);
const clientId = process.env.VUE_APP_GOOGLE_CLIENT_ID;
//console.log('Client ID:', clientId);

app.use(router)
app.use(GoogleSignInPlugin, { clientId });

app.config.globalProperties.$gAuth ? console.log('Google Sign-In Initialized') : console.log('Google Sign-In Not Initialized');
app.mount('#app');
