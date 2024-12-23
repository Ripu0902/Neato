<template>
    <div class="search-results container">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- No Results State -->
        <div v-else-if="services.length === 0" class="text-center py-5">
            <i class="bi bi-search display-1 text-muted"></i>
            <p class="mt-3">No services found matching your search.</p>
        </div>

        <!-- Results Display -->
        <div v-else class="row">
            <div v-for="service in services" :key="service.id" class="col-md-6 mb-4">
                <div class="card service-card h-100">
                    <div class="card-body">
                        <!-- Service Header -->
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <h5 class="card-title mb-1">{{ service.service_details.name }}</h5>
                                <p class="text-muted mb-0">
                                    <i class="bi bi-person-circle me-1"></i>
                                    {{ service.professional_name }}
                                </p>
                            </div>
                            <span class="badge bg-success">₹{{ service.service_details.price }}</span>
                        </div>

                        <!-- Service Details -->
                        <div class="service-details mb-3">
                            <p class="card-text">{{ service.service_details.description }}</p>
                            <div class="service-meta">
                                <p class="mb-1">
                                    <i class="bi bi-geo-alt me-1"></i>
                                    {{ service.service_pincode }}
                                </p>
                                <p class="mb-1">
                                    <i class="bi bi-briefcase me-1"></i>
                                    Experience: {{ service.experience }} years
                                </p>
                                <p class="mb-0">
                                    <i class="bi bi-star-fill text-warning me-1"></i>
                                   {{ service.kudos }} kudos
                                </p>
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div class="d-flex justify-content-between align-items-center mt-auto">
                            <button 
                                @click="sendRequest(service.service_details.service_id,service.professional_id)"
                                class="btn btn-success"
                            >
                                <i class="bi bi-send me-1"></i>
                                Send Request
                            </button>
                            <button 
                                @click="viewDetails(service)"
                                class="btn btn-outline-success ms-2"
                            >
                                <i class="bi bi-info-circle me-1"></i>
                                View Details
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showDetailModal && selectedService" 
             class="modal fade show" 
             style="display: block; background-color: rgba(0,0,0,0.5)">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center bg-light">
                            <h5 class="mb-0">Service Details</h5>
                            <button @click="closeDetails" 
                                    class="btn-close"
                                    aria-label="Close"></button>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <!-- Professional Info -->
                                <div class="col-md-6 mb-3">
                                    <h5>Professional Information</h5>
                                    <div class="professional-info">
                                        <p><strong>Name:</strong> {{ selectedService.professional_name }}</p>
                                        <p><strong>Experience:</strong> {{ selectedService.experience }} years</p>
                                        <p><strong>Contact:</strong> {{ selectedService.contact }}</p>
                                        <p><strong>Rating:</strong> 
                                            <span class="text-warning">
                                                <i class="bi bi-star-fill"></i>
                                            </span> 
                                            {{ selectedService.kudos }} reviews
                                        </p>
                                    </div>
                                </div>

                                <!-- Service Info -->
                                <div class="col-md-6 mb-3">
                                    <h5>Service Information</h5>
                                    <div class="service-info">
                                        <p><strong>Service:</strong> {{ selectedService.service_details.name }}</p>
                                        <p><strong>Category:</strong> {{ selectedService.service_details.category }}</p>
                                        <p><strong>Price:</strong> ₹{{ selectedService.service_details.price }}</p>
                                        <p><strong>Duration:</strong> {{ selectedService.service_details.time_required }} minutes</p>
                                    </div>
                                </div>

                                <!-- Description -->
                                <div class="col-12">
                                    <h5>Description</h5>
                                    <p>{{ selectedService.service_details.description }}</p>
                                </div>

                                <!-- Action Button -->
                                <div class="col-12 mt-3">
                                    <button @click="sendRequest(selectedService.service_details.service_id, selectedService.professional_id)" 
                                            class="btn btn-success w-100">
                                        <i class="bi bi-send me-2"></i>
                                        Send Service Request
                                    </button>
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
    name: 'SearchResults',
    props: {
        query: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            services: [],
            loading: false,
            error: null,
            selectedService: null,
            showDetailModal: false,

            selectedServiceId: null,
            selectedProfessionalId: null,

        }
    },
    watch: {
        query: {
            handler(newQuery) {
                if (newQuery) {
                    this.fetchServices(newQuery);
                }
            },
            immediate: true
        }
    },
    methods: {
        async fetchServices(query) {
            this.loading = true;
            try {
                const authToken = localStorage.getItem('authToken');
                const response = await fetch(`http://127.0.0.1:8000/api/services/search?query=${encodeURIComponent(query)}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch services');
                }
                const data = await response.json();
                this.services = data.services;
            } catch (error) {
                console.error('Error fetching services:', error);
                this.error = 'Failed to load services. Please try again.';
            } finally {
                this.loading = false;
            }
        },
     
        async  sendRequest(serviceId,professionalId)  {
            try{    
                const authToken = localStorage.getItem('authToken');
                if (!authToken) {
                    throw new Error('Please login to schedule a service');
                }

                const response = await fetch('http://127.0.0.1:8000/api/service-request', {
                    method: 'POST',
                    credentials: 'include',  // Add this
                    mode: 'cors',           // Add this
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({
                        service_id: serviceId,
                        professional_id: professionalId,
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message);
                }
                alert('Service request scheduled successfully!');
                
            } catch (error) {
                alert(`Failed to schedule request: ${error.message}`);
            }
        }
        ,
        viewDetails(service) {
        this.selectedService = service;
        this.showDetailModal = true;
        document.body.classList.add('modal-open');
    },

        closeDetails() {
            this.selectedService = null;
            this.showDetailModal = false;
            // Remove body class to allow scrolling again
            document.body.classList.remove('modal-open');
        }
    }
}
</script>

<style scoped>


.service-card {
    transition: transform 0.2s ease-in-out;
    border: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.service-meta {
    font-size: 0.9rem;
    color: #666;
}

.badge {
    font-size: 1rem;
    padding: 0.5em 1em;
}

/* Loading spinner customization */
.spinner-border {
    width: 3rem;
    height: 3rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .col-md-6 {
        padding: 0 10px;
    }
    
    .service-card {
        margin-bottom: 15px;
    }
}

/* Button hover effects */
.btn-success:hover {
    background-color: #157347;
    border-color: #146c43;
}

.btn-outline-success:hover {
    background-color: #198754;
    color: white;
}

/* Card content spacing */
.service-details {
    min-height: 100px;
}

.card-body {
    display: flex;
    flex-direction: column;
}

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1050;
}

.modal-content {
    border: none;
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.professional-info p, 
.service-info p {
    margin-bottom: 0.5rem;
}

.card-header {
    border-bottom: 1px solid rgba(0,0,0,0.1);
}

/* Add transition effects */
.modal-dialog {
    transition: transform 0.3s ease-out;
}

.modal.show .modal-dialog {
    transform: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .modal-dialog {
        margin: 0.5rem;
    }
}

</style>