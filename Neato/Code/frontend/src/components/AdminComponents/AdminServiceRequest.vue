<template>
    <div class="container py-4">
      <h2 class="mb-4">Service Requests Overview</h2>
        <!-- Export Button -->
        <div class="export mb-4">
        <button 
            @click="startExport" 
            class="btn btn-primary"
            :disabled="isExporting"
        >
            <i class="bi bi-download me-2"></i>
            {{ isExporting ? 'Generating Export...' : 'Export Service Reports' }}
        </button>
        </div>

        <!-- Export Status Alert -->
        <div v-if="exportStatus" 
            :class="['alert', exportStatus.type === 'success' ? 'alert-success' : 'alert-danger']">
        {{ exportStatus.message }}
        <a v-if="exportStatus.downloadUrl" 
            :href="exportStatus.downloadUrl"
            class="btn btn-sm btn-success ms-2">
            Download CSV
        </a>
    </div>
      <!-- Loading State -->
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
  
      <div v-else class="row g-4">
        <!-- Service Request Cards -->
        <div v-for="request in serviceRequests" :key="request.service_request_id" class="col-md-6">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h5 class="card-title">Request #{{ request.service_request_id }}</h5>
                  <p class="text-muted mb-1">
                    Service: {{ getServiceName(request.service_id) }}
                  </p>
                </div>
                <span :class="getStatusBadgeClass(request.service_status)">
                  {{ request.service_status }}
                </span>
              </div>
  
              <!-- Professional Info -->
              <div class="professional-info mb-3">
                <h6 class="text-primary">Professional Details</h6>
                <p class="mb-1">
                  <i class="bi bi-person"></i>
                  {{ request.professional.fullname }}
                </p>
                <p class="mb-1">
                  <i class="bi bi-envelope"></i>
                  {{ request.professional.email }}
                </p>
                <p class="mb-1">
                  <i class="bi bi-telephone"></i>
                  {{ request.professional.contact }}
                </p>
              </div>
  
              <!-- Request Dates -->
              <div class="dates-info mb-3">
                <p class="mb-1">
                  <i class="bi bi-calendar-event"></i>
                  Requested: {{ formatDate(request.date_of_request) }}
                </p>
                <p v-if="request.date_of_completion" class="mb-1">
                  <i class="bi bi-calendar-check"></i>
                  Completed: {{ formatDate(request.date_of_completion) }}
                </p>
              </div>
  
              <!-- View Details Button -->
              <button 
                @click="showDetails(request)" 
                class="btn btn-outline-primary btn-sm"
              >
                <i class="bi bi-info-circle me-1"></i>
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Details Modal -->
      <b-modal 
        v-model="showModal" 
        title="Service Request Details"
        size="lg"
        hide-footer
      >
        <div v-if="selectedRequest" class="request-details">
          <!-- Request Info -->
          <div class="section mb-4">
            <h5>Request Information</h5>
            <div class="info-grid">
              <p><strong>Request ID:</strong> #{{ selectedRequest.service_request_id }}</p>
              <p><strong>Service Type:</strong> {{ getServiceName(selectedRequest.service_id) }}</p>
              <p><strong>Status:</strong> 
                <span :class="getStatusBadgeClass(selectedRequest.service_status)">
                  {{ selectedRequest.service_status }}
                </span>
              </p>
              <p><strong>Date Requested:</strong> {{ formatDate(selectedRequest.date_of_request) }}</p>
              <p v-if="selectedRequest.date_of_completion">
                <strong>Date Completed:</strong> {{ formatDate(selectedRequest.date_of_completion) }}
              </p>
            </div>
          </div>
  
          <!-- Professional Details -->
          <div class="section mb-4">
            <h5>Professional Details</h5>
            <div class="info-grid">
              <p><strong>Name:</strong> {{ selectedRequest.professional.fullname }}</p>
              <p><strong>Email:</strong> {{ selectedRequest.professional.email }}</p>
              <p><strong>Contact:</strong> {{ selectedRequest.professional.contact }}</p>
              <p><strong>Experience:</strong> {{ selectedRequest.professional.experience }} years</p>
              <p><strong>Service Area:</strong> {{ selectedRequest.professional.service_pincode }}</p>
            </div>
          </div>
  
          <!-- Remarks if any -->
          <div v-if="selectedRequest.remarks" class="section">
            <h5>Remarks</h5>
            <p>{{ selectedRequest.remarks }}</p>
          </div>
        </div>
      </b-modal>
    </div>
  </template>

<script>

export default {
    name: 'AdminServiceRequests',
    data(){
        return{
            serviceRequests: [],
            error : '',
            serviceMapping: {},
            loading: true,
            showModal: false,
            selectedRequest: null,
            isExporting: false,
            exportStatus: null,
            exportCheckInterval: null
        }
    },
    async created(){
        await this.fetchServiceRequests();
    },
    methods:{
    async fetchServiceRequests(){
        try{
            const accessToken = localStorage.getItem('authToken');
            const response = await fetch("http://127.0.0.1:8000/api/service-request",{
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            const data = await response.json()

            if(response.ok){
                this.serviceRequests = data.services
                this.serviceMapping = data['service-mapping']
                console.log('ServiceRequest data loaded:', this.srdata);
            }else{
                this.error = data.message || 'Failed to load Service Request data';
                }
            } catch (error) {
                console.error('Error fetching data:', error)
                this.error = 'Failed to load Service Request Data'
            } finally {
                this.loading = false
            }
        },
        getServiceName(serviceId) {
        return this.serviceMapping[serviceId] || 'Unknown Service'
        },
        formatDate(dateString) {
        return new Date(dateString).toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
        },
        getStatusBadgeClass(status) {
      const classes = {
        REQUESTED: 'badge bg-warning',
        ACCEPTED: 'badge bg-info',
        IN_PROGRESS: 'badge bg-primary',
        COMPLETED: 'badge bg-success',
        REJECTED: 'badge bg-danger'
      }
      return classes[status] || 'badge bg-secondary'
    },
    showDetails(request) {
      this.selectedRequest = request
      this.showModal = true
    },    async startExport() {
      try {
        this.isExporting = true
        const response = await fetch('http://127.0.0.1:8000/api/export-services', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        })
        
        const data = await response.json()
        if (response.ok) {
          this.checkExportStatus(data.task_id)
        } else {
          this.exportStatus = {
            type: 'error',
            message: data.message
          }
        }
      } catch (error) {
        this.exportStatus = {
          type: 'error',
          message: 'Failed to start export'
        }
      }
    },

    async checkExportStatus(taskId) {
      this.exportCheckInterval = setInterval(async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/export-services/${taskId}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
          })
          
          const data = await response.json()
          if (data.status === 'completed') {
            clearInterval(this.exportCheckInterval)
            this.isExporting = false
            this.exportStatus = {
              type: 'success',
              message: 'Export completed successfully!',
              downloadUrl: data.download_url
            }
          } else if (data.status === 'failed') {
            clearInterval(this.exportCheckInterval)
            this.isExporting = false
            this.exportStatus = {
              type: 'error',
              message: `Export failed: ${data.error}`
            }
          }
        } catch (error) {
          clearInterval(this.exportCheckInterval)
          this.isExporting = false
          this.exportStatus = {
            type: 'error',
            message: 'Failed to check export status'
          }
        }
      }, 2000) // Check every 2 seconds
    }
    },

}
</script>

<style scoped>
.export{
    margin-left: 880px;
}


.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.badge {
  padding: 0.5em 0.8em;
}

.professional-info i,
.dates-info i {
  margin-right: 0.5rem;
  color: #6c757d;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.section h5 {
  margin-bottom: 1rem;
  color: #0d6efd;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>