<!-- LoginCard.vue -->
<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="card login-card shadow-lg">
      <div class="card-header text-center bg-seagreen text-white py-4 border-0">
        <h3 class="mb-0 fw-bold">Welcome Back</h3>
      </div>
      <div class="card-body p-5">
        <form @submit.prevent="handleLogin">
          <div class="form-floating mb-4">
            <input type="text" class="form-control border-0 border-bottom rounded-0" id="username" v-model="username"
              autocomplete="username" required>
            <label for="username" class="text-muted">User Name</label>
          </div>

          <div class="form-floating mb-4">
            <input type="password" class="form-control border-0 border-bottom rounded-0" id="password"
              v-model="password" placeholder="Password" autocomplete="current-password" required>
            <label for="password" class="text-muted">Password</label>
          </div>

          <button type="submit" class="btn btn-seagreen w-100 py-3 mb-4">
            Sign In
          </button>

          <p class="text-center text-muted mb-0">
            Don't have an account?
            <router-link to="/sign-up" class="text-seagreen text-decoration-none">Sign up</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async handleLogin() {
        if(this.username === 'admin'){
          alert('You are not authorized!')
          throw new Error('You are not Authorized')
        }
      try {
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);

        console.log(formData);
        const response = await fetch('http://127.0.0.1:8000/api/login', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Login successful:', data);

          localStorage.setItem('authToken', data['access_token']);
          
          this.$router.push({ name: 'UserDashboard' });
        } else {
          const errorData = await response.json();
          alert(errorData.message);
          this.errorMessage = errorData.message || 'An error occurred. Please try again';
        }
      } catch (error) {
        console.error('Error:', error);
        this.errorMessage = 'An error occurred. Please try again.';
      }
    }
  }
}
</script>

<style scoped>
.login-card {
  width: 100%;
  max-width: 450px;
  border: none;
  border-radius: 15px;
}

.bg-seagreen {
  background-color: #2e8b57 !important;
}

.text-seagreen {
  color: #2e8b57 !important;
}

.btn-seagreen {
  background-color: #2e8b57;
  color: white;
  border: none;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-seagreen:hover {
  background-color: #246b43;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(46, 139, 87, 0.3);
}

.form-control:focus {
  border-color: #2e8b57;
  box-shadow: none;
}

.form-check-input:checked {
  background-color: #2e8b57;
  border-color: #2e8b57;
}

/* Custom floating label colors */
.form-floating>.form-control:focus~label,
.form-floating>.form-control:not(:placeholder-shown)~label {
  color: #2e8b57;
}

.form-floating>.form-control:focus,
.form-floating>.form-control:not(:placeholder-shown) {
  border-bottom: 2px solid #2e8b57 !important;
}
</style>