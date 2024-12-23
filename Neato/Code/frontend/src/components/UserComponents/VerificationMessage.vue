<template>
    <div class="alert alert-warning p-4 text-center">
      <h4>Verification Pending</h4>
      <p>Your account is currently under review. Please wait for admin verification.</p>
      <button @click="handleLogout" class="btn btn-primary mt-2">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'VerificationMessage',
    methods: {
      handleLogout() {
        localStorage.removeItem('authToken')
        this.$router.push('/login')
      }
    }
  }
  </script>