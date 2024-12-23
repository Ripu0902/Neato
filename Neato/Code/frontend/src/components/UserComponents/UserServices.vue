<template>
  <div class="container">
    <div class="row">
      <div class="col-12">
        <h2 class="mb-4">{{ userRole === 2 ? 'Service Requests Received' : 'My Service Requests' }}</h2>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <!-- No Requests State -->
        <div v-else-if="!serviceRequests.services.length" class="text-center py-5">
          <i class="bi bi-inbox display-1 text-muted"></i>
          <p class="mt-3">No service requests found.</p>
        </div>

        <!-- Requests List -->
        <div v-else class="row g-4">
          <div v-for="request in serviceRequests.services" :key="request.service_request_id" class="col-12">
            <div class="card">
              <div class="card-body">
                <div class="justify-content-between mb-3">
                  <div class="row">
                    <h5 class="card-title">Service Request #{{ request.service_request_id }}</h5>
                    <div class="col-6">
                      
                      <p class="mb-1" v-if="userRole===2" >
                        Customer: {{ request.customer.fullname }}
                      </p>
                      <p class="mb-1" v-if="userRole===1" >
                        Professional Name: {{ request.professional.fullname }}
                      </p>
                      <p class="mb-1" v-if="userRole===1" >
                        Experience : {{ request.professional.experience }}
                      </p>
                      <p class="mb-1" v-if="userRole===1" >
                        Service : {{ serviceMapping[request.professional.service_type] }}
                      </p>
                      <p class="text-muted mb-1">
                        Requested: {{ formatDate(request.date_of_request) }}
                      </p>
                      <p class="mb-1">
                        Status:
                        <span :class="getStatusBadgeClass(request.service_status)">
                          {{ request.service_status }}
                        </span>
                      </p>
                      <p class="mb-1" v-if="userRole===2 && request.service_status != 'REQUESTED'" >
                        Contact : {{ request.customer.contact }}
                      </p>
                      <p class="mb-1" v-if="userRole===1 && request.service_status != 'REQUESTED'" >
                        Contact : {{ request.professional.contact }}
                      </p>
                    </div>
                    <div class="col-6">

                    </div>
                  </div>
                </div>

                <!-- Professional View -->
                <div v-if="userRole === 2" class="ms-4 ps-4">
                  <div v-if="request.service_status === 'REQUESTED'" class="d-flex gap-2 mt-3 ms-4 ps-5">
                    <button @click="updateRequestStatus(request.service_request_id, 'ACCEPTED')"
                      class="btn btn-success">
                      Accept Request
                    </button>
                    <button @click="updateRequestStatus(request.service_request_id, 'REJECTED')" class="btn btn-danger">
                      Reject Request
                    </button>
                  </div>
                  <div v-if="request.service_status === 'IN_PROGRESS'" class="mt-3">
                    <p class="text-info">
                      <i class="bi bi-info-circle"></i>
                      Service is currently in progress
                    </p>
                  </div>
                </div>

                <!-- Customer View -->
                <div v-if="userRole === 1 && request.service_status === 'ASSIGNED'" class="d-flex gap-2 mt-3">
                  <!-- For Accepted but not started services -->
                  <button @click="updateRequestStatus(request.service_request_id, 'IN_PROGRESS')"
                    class="btn btn-primary">
                    Open Service
                    <small class="d-block text-white-50">Click when professional arrives</small>
                  </button>
                </div>

                <!-- For In Progress services -->
                <template>
                  <div v-if="userRole === 1 && request.service_status === 'IN_PROGRESS'" class="d-flex gap-2 mt-3">
                    <button @click="completeServiceWithRemarks(request.service_request_id)" class="btn btn-success">
                      Complete Service with Remarks
                      <small class="d-block text-white-50">Click when service is complete</small>
                    </button>
                  </div>

                  <div v-if="request.remarks" class="mt-3">
                    <h6>Remarks:</h6>
                    <p class="mb-0">{{ request.remarks }}</p>
                  </div>
                </template>


                <!-- Service Timeline -->
                <div class="service-timeline mt-4">
                  <div class="timeline-item" :class="{ 'completed': ['REQUESTED', 'ACCEPTED', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED'].includes(request.service_status) }">
                    <div class="timeline-icon">
                      <i class="bi bi-1-circle"></i>
                    </div>
                    <div class="timeline-content">Request Placed</div>
                  </div>
                  <div class="timeline-item" :class="{ 'completed': ['ACCEPTED', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED'].includes(request.service_status) }">
                    <div class="timeline-icon">
                      <i class="bi bi-2-circle"></i>
                    </div>
                    <div class="timeline-content">Professional Accepted</div>
                  </div>
                  <div class="timeline-item" :class="{ 'completed': ['IN_PROGRESS', 'COMPLETED'].includes(request.service_status) }">
                    <div class="timeline-icon">
                      <i class="bi bi-3-circle"></i>
                    </div>
                    <div class="timeline-content">Service Started</div>
                  </div>
                  <div class="timeline-item" :class="{ 'completed': ['COMPLETED'].includes(request.service_status) }">
                    <div class="timeline-icon">
                      <i class="bi bi-4-circle"></i>
                    </div>
                    <div class="timeline-content">Service Completed</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserServices',
  data() {
    return {
      serviceRequests: [],
      loading: true,
      error: null,
      userRole: null,
      remarkText: {},
      serviceMapping:{},
    }
  },
  async created() {
    await this.fetchUserRole();
    await this.fetchServiceRequests();
  },
  methods: {
    async fetchUserRole() {
      const authToken = localStorage.getItem('authToken');
      try {
        console.log('userRole requested')
        const response = await fetch('http://127.0.0.1:8000/api/user', {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });
        const userData = await response.json();
        console.log('userData');
        this.userRole = userData.userdata.role;
      } catch (error) {
        console.error('Error fetching user role:', error);
      }
    },

    async fetchServiceRequests() {
      const authToken = localStorage.getItem('authToken');
      try {
        const response = await fetch('http://127.0.0.1:8000/api/service-request', {
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch service requests');
        }

        this.serviceRequests = await response.json();
        this.serviceMapping = this.serviceRequests['service-mapping']
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },

    async updateRequestStatus(requestId, status) {
      const authToken = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/service-request/${requestId}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            service_status: status
          })
        });

        if (!response.ok) {
          throw new Error('Failed to update request status');
        }

        await this.fetchServiceRequests();
      } catch (error) {
        alert(error.message);
      }
    },
    async completeServiceWithRemarks(requestId) {
      try {
        const remarkText = prompt('Please enter your remarks:');
        const ratingnum = prompt('Please enetr rating out of 5')
        if (!remarkText?.trim()) {
          alert('Please enter your remarks');
          alert('Please enter rating!')
          return;
        }


        const response = await fetch(`http://127.0.0.1:8000/api/service-request/${requestId}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'service_status': 'COMPLETED',
            'remarks': remarkText,
            'ratingnum': ratingnum
          })
        });

        if (!response.ok) {
          throw new Error('Failed to complete service with remarks');
        }

        await this.fetchServiceRequests();
      } catch (error) {
        alert(error.message);
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    getStatusBadgeClass(status) {
      const classes = {
        REQUESTED: 'badge bg-warning',
        ACCEPTED: 'badge bg-info',
        IN_PROGRESS: 'badge bg-primary',
        REJECTED: 'badge bg-danger',
        COMPLETED: 'badge bg-success'
      };
      return classes[status] || 'badge bg-secondary';
    }
  }
}
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.badge {
  padding: 0.5em 0.8em;
  font-size: 0.85em;
}

.btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.service-timeline {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.timeline-item {
  flex: 1;
  text-align: center;
  color: #6c757d;
  font-size: 0.9rem;
  position: relative;
  padding: 0 10px;
}

.timeline-item::after {
  content: '';
  position: absolute;
  top: 50%;
  right: -50%;
  width: 100%;
  height: 2px;
  background-color: #e9ecef;
  z-index: 1;
}

.timeline-item:last-child::after {
  display: none;
}

.timeline-item.completed {
  color: #198754;  /* Bootstrap's success green color */
}

.timeline-item.completed::after {
  background-color: #198754;  /* Bootstrap's success green color */
}

.timeline-icon {
  background: white;
  padding: 0 5px;
  position: relative;
  z-index: 2;
  display: inline-block;
}

.timeline-content {
  margin-top: 5px;
}

small.text-white-50 {
  font-size: 0.75rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>