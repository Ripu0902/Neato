<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Left Sidebar with Profile and Tools -->
      <div class="col-3 position-fixed start-0">
        <!-- Admin Profile Card -->
        <div class="admindash">
          <div class="card profile-card text-white">
            <div class="card-body p-4">
              <!-- Profile Picture Section -->
              <div class="text-center mb-4">
                <div class="profile-picture-container position-relative mx-auto">
                  <img src="https://i.pinimg.com/736x/e5/7b/98/e57b987df5b29f59db3eb669499154ee.jpg"
                    class="profile-picture rounded-circle border border-3 border-white" alt="Admin Profile">
                </div>
              </div>

              <!-- Profile Details -->
              <div class="profile-details">
                <div class="mb-3">
                  <label class="form-label small">User ID:</label>
                  <div class="d-flex align-items-center">
                    <span class="flex-grow-1 text-dark">{{ getUserId }}</span>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label small">Username:</label>
                  <div class="d-flex align-items-center">
                    <span class="flex-grow-1 text-dark">{{ getUsername }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tools Box -->
          <div class="tools-box mt-4">
            <div class="card">
              <div class="card-header bg-light">
                <h5 class="mb-0">TOOLS</h5>
              </div>
              <div class="card-body">
                <div class="list-group">
                  <router-link :to="{ name: 'admin-stats' }" class="list-group-item list-group-item-action">
                    Dashboard
                  </router-link>
                  <router-link :to="{ name: 'admin-users' }" class="list-group-item list-group-item-action">
                    Users
                  </router-link>
                  <router-link :to="{ name: 'admin-services' }" class="list-group-item list-group-item-action">
                    Services
                  </router-link>
                  <router-link :to="{ name: 'admin-verification' }" class="list-group-item list-group-item-action">
                    Verification request
                  </router-link>
                  <router-link :to="{ name: 'admin-sr' }" class="list-group-item list-group-item-action">
                    All Service Requests
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="col-8 main-content">
        <admin-stats v-if="!$route.name || $route.name === 'admin-stats'" />
      <router-view v-else />
      </div>
    </div>

  </div>
</template>

<script>
import AdminStats from './AdminComponents/AdminStats.vue';

export default {
  name: 'AdminDashboard',
  components :{
    AdminStats
  },
  data() {
    return {
      admindata: {},
      loading: true,
      error: null,

    }
  },
  computed: {
    getUserId() {
      return this.admindata?.admindata?.user_id || 'N/A'
    },
    getUsername() {
      return this.admindata?.admindata?.username || 'N/A'
    },
  },
  async created() {
    await this.fetchAdminDetails();
  },
  methods: {
    async fetchAdminDetails() {
      try {
        this.loading = true
        const accessToken = localStorage.getItem('authToken');
        const response = await fetch("http://127.0.0.1:8000/api/user", {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        const data = await response.json()

        if (response.ok) {
          this.admindata = data
          console.log('Admin data loaded:', this.admindata);
        } else {
          this.error = data.message || 'Failed to load profile';
        }
      } catch (error) {
        console.error('Error fetching profile:', error)
        this.error = 'Failed to load profile'
      } finally {
        this.loading = false;  // Always set loading to false when done
      }
    },
  },
  beforeDestroy() {
    if (this.exportCheckInterval) {
      clearInterval(this.exportCheckInterval)
    }
  }
}
</script>

<style scoped>

.form-switch {
  padding-left: 2.5em;
}

input {
    width: 300px;
    margin-left: 1400px;
    border-radius: 40px;
    background-color: rgba(255, 255, 255, 0.514);
    /* White with transparency */
}

input:hover {
    box-shadow: 0 6px 8px rgba(23, 255, 158, 0.8);
}

#search {
    border-radius: 40px;
    width: 50px;
    margin-top: 100px;
}


.container-fluid {
  padding-top: 20px;
  padding-left: 20px;
}

.admindash {
  margin-top: 80px;
  margin-left: 20px;
  padding: 10px;
  max-height: 800px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 50px;
  box-shadow: 0 6px 8px rgba(23, 255, 158, 0.8);
}

.profile-card {
  border-radius: 15px;
  margin: 20px;
  max-width: 400px;
  background-color: rgba(141, 168, 228, 0.8);
}

.profile-picture-container {
  width: 120px;
  height: 120px;
}

.profile-picture {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tools-box {
  border-radius: 20px;
  margin: 20px;
  max-width: 400px;
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.list-group-item {
  padding: 12px 20px;
  color: #333;
  transition: all 0.2s ease;
}

.list-group-item:hover {
  background-color: rgba(0, 0, 0, 0.05) !important;
  color: #000;
  font-weight: bolder;
}

.list-group-item:active {
  transform: scale(0.98);
}

.main-content {
  margin-left: 10px;
  /* Adjust this value based on your sidebar width */
  padding: 10px;
  margin-top: 80px;
}

/* Make sure the router-view content doesn't overlap with the sidebar */
@media (min-width: 768px) {
  .main-content {
    margin-left: 27.333%;
    /* Matches col-3 width */
  }
}
</style>