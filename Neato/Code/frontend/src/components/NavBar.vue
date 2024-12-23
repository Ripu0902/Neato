<template>
    <div class="navbar">
        <nav class="navbar fixed-top bg-custom">
            <div class="container-fluid d-flex justify-content-between align-items-center mb-0 ms-4 me-4">
                <ul class="navbar-nav d-flex flex-row mb-lg-0">
                    <a class="navbar-brand d-flex align-items-center" href="#">
                        <img src="../assets/logo.png" alt="Logo" width="40" height="40"
                            class="d-inline-block align-top pb-2">
                    </a>
                    <li class="nav-item">
                        <a class="nav-link pb-0 active" aria-current="page" href="/" style="color: darkgreen;">Neato</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link ms-3 pb-0 active" aria-current="page" href="/"
                            style="color: darkgreen;">Home</a>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link ms-3 pb-0 active" aria-current="page" to="/about-us"
                            style="color: darkgreen;">Who we are</router-link>
                    </li>
                </ul>
                    <ul class="navbar-nav d-flex flex-row mb-lg-0">
                        <template v-if="!isloggedin">
                            <li class="nav-item">
                                <router-link to="/login" class="nav-link pb-0 active" 
                                    style="color: darkgreen;">Login</router-link>
                            </li>
                            <li class="nav-item">
                                <router-link to="/sign-up" class="nav-link ms-3 pb-0 active" 
                                    style="color: darkgreen;">Signup</router-link>
                            </li>
                        </template>
                        <li v-else class="nav-item">
                            <a @click="logout" class="nav-link ms-3 pb-0 active" href="#"
                                style="color: darkgreen;">Logout</a>
                        </li>
                        <li v-if="!isloggedin" class="nav-item">
                            <router-link to="/admin-login" class="nav-link ms-3 pb-0 active"
                                style="color: darkgreen;">Admin</router-link>
                        </li>
                    </ul>
            </div>
        </nav>
    </div>
</template>



<script>
export default {
   name: 'NavBar',
   data() {
       return {
           isloggedin: false
       }
   },
   created() {
       this.checkLoginStatus(); // Check login status when component is created
   },
   watch: {
       '$route'() {
           this.checkLoginStatus();
       }
   },
   methods: {
       checkLoginStatus() {
           this.isloggedin = !!localStorage.getItem('authToken');
       },
       logout() {
           localStorage.removeItem('authToken');
           this.isloggedin = false;
           this.$router.push('/login');
       }
   }
}
</script>

<style scoped>
.navbar {
    margin: 0px;
}

.bg-custom {
    margin: 30px;
    border-radius: 40px;
    background-color: rgba(23, 255, 158, 0.20);
    /* White with transparency */
    backdrop-filter: blur(10px);
    /* Optional: Adds a blur effect */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    /* Adds a soft shadow */
    border: 1px solid rgba(255, 255, 255, 0.18);
    /* Optional: Adds a light border */
}

li {
    font-weight: normal;
    font-size: x-large;
    margin-left: 2px;
}

</style>