<template>
  <div class="admin-users">
    <div class="card">
      <div class="card-header">
        <h4>Users Management</h4>
      </div>
      <div class="card-body">
        <div class="admin-users-container">
          <div class="row g-4">
            <!-- Professional Cards -->
            <div class="col-md-4" v-for="professional in professionaldata" :key="professional.professional_id">
              <div class="user-card-prof">
                <!-- Profile Section -->
                <div class="profile-section">
                  <div class="profile-image-container">
                    <img :src="getCorrectImagePath(professional.profile_image)" :alt="professional.username"
                      class="profile-image">
                  </div>
                  <div class="name">{{ professional.fullname }}</div>
                  <div class="user-name">@{{ professional.username }}</div>
                </div>

                <!-- Stats Section -->
                <div class="stats-section">
                  <div class="stat-item">
                    <div class="stat-number">User Type</div>
                    <div class="badge bg-success mb-3">Professional</div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-number" style="text-wrap:balance;">{{ professional.email || 'Not specified' }}</div>
                    <div class="stat-label">Email</div>
                  </div>
                </div>

                <!-- Menu Button -->
                <div class="menu-button">
                  <b-button variant="link" class="p-0" @click="showOptions(professional)">
                    <b-icon icon="three-dots-vertical"></b-icon>
                  </b-button>
                </div>
              </div>
            </div>

            <!-- Customer Cards -->
            <div class="col-md-4" v-for="customer in customerdata" :key="customer.customer_id">
              <div class="user-card-cus">
                <!-- Profile Section -->
                <div class="profile-section">
                  <div class="profile-image-container">
                    <img :src="getCorrectImagePath(customer.profile_image)" :alt="customer.profile_image"
                      class="profile-image">
                  </div>
                  <div class="name">{{ customer.fullname }}</div>
                  <div class="user-name">@{{ customer.username }}</div>
                </div>

                <!-- Stats Section -->
                <div class="stats-section">
                  <div class="stat-item">
                    <div class="stat-number">User Type</div>
                    <div class="badge bg-primary mb-3">Customer</div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-number">{{ customer.email || 0 }}</div>
                    <div class="stat-label">Email</div>
                  </div>
                </div>

                <!-- Menu Button -->
                <div class="menu-button">
                  <b-button variant="link" class="p-0" @click="showOptions(customer)">
                    <b-icon icon="three-dots-vertical"></b-icon>
                  </b-button>
                </div>
              </div>
            </div>
          </div>

          <!-- Options Modal -->
          <b-modal id="options-modal" v-model="showOptionsModal" title="User Options" size="sm" centered>
            <b-button variant="primary" class="w-100 mb-2" @click="showUserDetails">
              View Full Details
            </b-button>
            <b-button :variant="selectedUser?.is_blocked ? 'success' : 'danger'" class="w-100"
              @click="toggleBlockStatus">
              {{ selectedUser?.is_blocked ? 'Unblock User' : 'Block User' }}
            </b-button>
          </b-modal>

          <!-- Details Modal -->
          <b-modal id="options-modal" v-model="showDetailsModal"
            :title="`${selectedUser?.role == 2 ? 'Professional' : 'Customer'} Details`" size="lg" centered>
            <div v-if="selectedUser" class="user-details">
              <div class="row">
                <!-- Common Profile Section -->
                <div class="col-md-4 text-center">
                  <img :src="getCorrectImagePath(selectedUser.profile_image)" :alt="selectedUser.username"
                    class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;">
                  <h3>{{ selectedUser.fullname }}</h3>
                  <h4 style="opacity: 0.5;">@{{ selectedUser.username }}</h4>
                  <b-badge :variant="selectedUser.role == 2 ? 'primary' : 'info'" class="mb-2">
                    {{ selectedUser.role == 2 ? 'Professional' : 'Customer' }}
                  </b-badge> <br>
                  <b-badge :variant="selectedUser.is_blocked ? 'danger' : 'success'">
                    {{ selectedUser.is_blocked ? 'Blocked' : 'Active' }}
                  </b-badge>
                </div>

                <!-- Details Section -->
                <div class="col-md-8">
                  <!-- Common Information -->
                  <h6 class="details-section-title">Basic Information</h6>
                  <b-table-simple>
                    <b-tbody>
                      <b-tr>
                        <b-th>User ID</b-th>
                        <b-td>{{ selectedUser.user_id }}</b-td>
                      </b-tr>
                      <b-tr>
                        <b-th>Email</b-th>
                        <b-td>{{ selectedUser.email }}</b-td>
                      </b-tr>
                      <b-tr>
                        <b-th>Contact</b-th>
                        <b-td>{{ selectedUser.contact }}</b-td>
                      </b-tr>
                    </b-tbody>
                  </b-table-simple>

                  <!-- Professional Specific Details -->
                  <template v-if="selectedUser.role == 2">
                    <h6 class="details-section-title mt-4">Professional Details</h6>
                    <b-table-simple>
                      <b-tbody>
                        <b-tr>
                          <b-th>Service Provided</b-th>
                          <b-td>{{ service_category[selectedUser.service_type] || 'Not specified' }}</b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Service Area Pincode</b-th>
                          <b-td>{{ selectedUser.service_pincode || 'Not specified' }}</b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Experience</b-th>
                          <b-td>{{ selectedUser.experience || 'Not specified' }} years</b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Description</b-th>
                          <b-td>{{ selectedUser.description || 'Not specified' }} </b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Portfolio</b-th>
                          <b-td><a :href="getCorrectImagePath(selectedUser.document_path)" :alt="selectedUser.username"
                              target="_blank" class="rounded-circle mb-3"
                              style="width: 150px; height: 150px; object-fit: cover;"><b-badge
                                variant="">Portfolio.pdf</b-badge></a>
                          </b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Verification Status</b-th>
                          <b-td>
                            <b-badge :variant="selectedUser.isActive === 1 ? 'success' :
                              selectedUser.isActive === 0 ? 'warning' : 'danger'">
                              {{ selectedUser.isActive === 1 ? 'Verified' :
                                selectedUser.isActive === 0 ? 'Not Verified' : 'Rejected' }}
                            </b-badge>
                          </b-td>
                        </b-tr>
                        <b-tr>
                          <b-th>Kudos</b-th>
                          <b-td>
                            {{ selectedUser.kudos }}
                          </b-td>
                        </b-tr>
                      </b-tbody>
                    </b-table-simple>
                  </template>

                  <!-- Customer Specific Details -->
                  <template v-else>
                    <b-table-simple>
                      <b-tbody>
                        <b-tr>
                          <b-th>Address</b-th>
                          <b-td>{{ selectedUser.address.split(":").join(",") || 'Not specified' }}</b-td>
                        </b-tr>
                      </b-tbody>
                    </b-table-simple>
                  </template>
                </div>
              </div>
            </div>

            <template #modal-footer>
              <b-button :variant="selectedUser?.is_blocked ? 'success' : 'danger'" @click="toggleBlockStatus">
                {{ selectedUser?.is_blocked ? 'Unblock User' : 'Block User' }}
              </b-button>
              <b-button variant="secondary" @click="hideDetailsModal">
                Close
              </b-button>
            </template>
          </b-modal>


        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminUsers',
  data() {
    return {
      customerdata: {},
      professionaldata: {},
      loading: true,
      error: null,
      defaultProfilePic: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/800px-User_icon_2.svg.png',
      selectedUser: null,
      showOptionsModal: false,  // For options modal
      showDetailsModal: false,  // Add this property
      service_category:[],
    
    }
  },
  async created() {
    await this.fetchUserDetails();
  },
  computed: {
    userTypeClass() {
      return this.selectedUser?.user_type === 'professional'
        ? 'bg-primary'
        : 'bg-info';
    }
  },
  methods: {
    async fetchUserDetails() {
      try {
        const accessToken = localStorage.getItem('authToken');
        const response = await fetch("http://127.0.0.1:8000/api/get-user", {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });
        const data = await response.json();

        if (response.ok) {
          this.customerdata = data['customerdata'];
          this.professionaldata = data['professionaldata'];
          this.service_category = data['service-mapping'];
        } else {
          this.error = data.message;
        }
      } catch (error) {
        console.error('Error fetching Customer or Professional data:', error);
        this.error = 'Failed to load Users data'
      }
    },
    async toggleBlockStatus() {
      try {
        const accessToken = localStorage.getItem('authToken');
        const response = await fetch(`http://127.0.0.1:8000/api/toggle-block/${this.selectedUser.user_id}`, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          }
        });

        if (response.ok) {
          // Update the user's blocked status locally
          this.selectedUser.is_blocked = !this.selectedUser.is_blocked;
          // Find and update the user in the customerdata array
          const userIndex = this.customerdata.findIndex(u => u.user_id === this.selectedUser.user_id);
          if (userIndex !== -1) {
            this.customerdata[userIndex].is_blocked = this.selectedUser.is_blocked;
          }
          // Show success message
          alert(`User successfully ${this.selectedUser.is_blocked ? 'blocked' : 'unblocked'}`);
        } else {
          alert('Failed to update user status');
        }
      } catch (error) {
        console.error('Error toggling block status:', error);
        alert('Failed to update user status');
      }
    },

    getCorrectImagePath(profilePic) {
      if (!profilePic) return this.defaultProfilePic;

      // Get filename from path
      const filename = profilePic.split("\\").pop();

      // Use the complete Flask server URL
      return `http://127.0.0.1:8000/documents/${filename}`;
    },
    showOptions(user) {
      this.selectedUser = user;
      this.showOptionsModal = true;
      this.optionsModal = true;
    },
    hideOptionsModal() {
      this.optionsModal = false;
    },
    showUserDetails() {
      this.showOptionsModal = false;
      this.$nextTick(() => {
        this.showDetailsModal = true;

      });
    },
    hideDetailsModal() {
      this.showDetailsModal = false;
    },
    formatDate(date) {
      if (!date) return 'Not available';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    getReportClass(count) {
      if (count === 0) return 'text-success';
      if (count < 3) return 'text-warning';
      return 'text-danger';
    }
  }
}
</script>

<style scoped>
.card-header {
  background-color: aquamarine;
}

.admin-users-container {
  padding: 20px;
}

.user-card-cus,
.user-card-prof {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.2s;
}

.user-card-prof:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 10px rgba(122, 209, 81, 0.5);
}

.user-card-cus:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 10px rgba(81, 158, 209, 0.5);
}


.profile-section {
  text-align: center;
  margin-bottom: 20px;
}

.profile-image-container {
  width: 100px;
  height: 100px;
  margin: 0 auto 15px;
  position: relative;
}

.profile-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-name {
  font-weight: 500;
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 10px;
}

.stats-section {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-weight: 600;
  font-size: 1.2rem;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.menu-button {
  position: absolute;
  top: 15px;
  right: 15px;
}

.user-details h6 {
  color: #666;
  border-bottom: 2px solid #eee;
  padding-bottom: 8px;
  margin-bottom: 16px;
  font-weight: 600;
}

.table th {
  width: 40%;
  color: #666;
  font-weight: 500;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}
</style>
