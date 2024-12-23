<template>
    <div class="verifyprof p-4">
        <div class="d-flex justify-content-between align-items-center" style="background-color: aquamarine;">
            <h2 class="mt-2 " style="margin-left: 370px;">Professional Verification Requests</h2>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
            <b-spinner variant="primary" label="Loading..."></b-spinner>
        </div>

        <!-- Error Alert -->
        <b-alert v-if="error" show variant="danger" class="mb-4">{{ error }}</b-alert>

        <!-- No Pending Verifications -->
        <b-alert v-if="!loading && getPendingProfessionals.length === 0" show variant="info">
            No pending verification requests found.
        </b-alert>

        <!-- Professionals Grid -->
        <div class="professionals-grid">
            <b-card v-for="professional in getPendingProfessionals" :key="professional.id" no-body
                class="professional-card">
                <!-- Card Header with Profile Picture -->
                <div class="card-img-container">
                    <img :src="getCorrectImagePath(professional.profile_image)" class="profile-pic"
                        alt="Profile Picture">
                </div>

                <!-- Card Body -->
                <b-card-body>
                    <h4 class="mb-2">{{ professional.fullname }}</h4>
                    <p class="text-muted mb-2">@{{ professional.username }}</p>

                    <div class="details-row mb-2">
                        <i class="fas fa-briefcase"></i>
                        <span>{{ service_category[professional.service_type] || 'No services listed' }}</span>
                    </div>

                    <div class="details-row mb-3">
                        <i class="fas fa-clock"></i>
                        <span>{{ professional.experience }} years experience</span>
                    </div>

                    <!-- Action Buttons -->
                    <div class="card-actions">
                        <b-button variant="outline-primary" block class="mb-2" @click="showDetails(professional)">
                            View Details
                        </b-button>

                        <div class="d-flex gap-2">
                            <b-button variant="success" class="flex-grow-1" @click="verifyProfessional(professional)">
                                Verify
                            </b-button>
                            <b-button variant="danger" class="flex-grow-1" @click="rejectProfessional(professional)">
                                Reject
                            </b-button>
                        </div>
                    </div>
                </b-card-body>
            </b-card>
        </div>

        <!-- Details Modal -->
        <b-modal v-model="showDetailsModal" size="lg" centered title="Professional Details">
            <div v-if="selectedProfessional" class="professional-details">
                <!-- Basic Information -->
                <section class="mb-4">
                    <h5 class="section-title">Basic Information</h5>
                    <div class="details-grid">
                        <div class="detail-item">
                            <span class="label">Email:</span>
                            <span class="value">{{ selectedProfessional.email }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Phone:</span>
                            <span class="value">{{ selectedProfessional.contact }}</span>
                        </div>
                    </div>
                </section>

                <!-- Professional Information -->
                <section class="mb-4">
                    <h5 class="section-title">Professional Information</h5>
                    <div class="details-grid">
                        <div class="detail-item">
                            <span class="label">Services:</span>
                            <span class="value">{{ selectedProfessional.service_type }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">About:</span>
                            <span class="value">{{ selectedProfessional.description }}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">Kudos:</span>
                            <span class="value">{{ selectedProfessional.kudos }}</span>
                        </div>
                    </div>
                </section>

                <!-- Portfolio Document -->
                <section>
                    <h5 class="section-title">Portfolio</h5>
                    <a v-if="selectedProfessional.document_path"
                        :href="getCorrectImagePath(selectedProfessional.document_path)" type="application/pdf"
                        target="_blank"><b-badge variant="primary" class="portfolio-badge"><i
                                class="bi bi-filetype-pdf"></i> Portfolio.pdf</b-badge></a>
                    <p v-else class="text-muted">No portfolio document available</p>
                </section>
            </div>
        </b-modal>

        <!-- Confirmation Modals -->
        <b-modal v-model="showVerifyModal" title="Confirm Verification" @ok="verifyProfessional(selectedProfessional)">
            Are you sure you want to verify this professional?
        </b-modal>

        <b-modal v-model="showRejectModal" title="Confirm Rejection" @ok="rejectProfessional(selectedProfessional)">
            Are you sure you want to reject this professional?
        </b-modal>
    </div>
</template>

<script>
export default {
    name: 'AdminVerification',

    data() {
        return {
            professionaldata: {},
            customerdata: {},
            loading: true,
            error: null,
            showDetailsModal: false,
            showVerifyModal: false,
            showRejectModal: false,
            showPortfolioModal: false,
            selectedProfessional: null,
            service_category : [],
        }
    },

    computed: {
        getPendingProfessionals() {
            return Object.values(this.professionaldata).filter(prof =>
                prof && prof.isActive === 0
            );
        }
    },

    async created() {
        await this.fetchUserDetails();
    },

    methods: {
        async fetchUserDetails() {
            this.loading = true;
            this.error = null;

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
                console.error('Error fetching data:', error);
                this.error = 'Failed to load Users data';
            } finally {
                this.loading = false;
            }
        },

        showDetails(professional) {
            this.selectedProfessional = professional;
            this.showDetailsModal = true;
        },

        confirmVerify(professional) {
            this.selectedProfessional = professional;
            this.showVerifyModal = true;
        },

        confirmReject(professional) {
            this.selectedProfessional = professional;
            this.showRejectModal = true;
        },
        viewPortfolio(professional) {
            this.selectedProfessional = professional;
            this.showPortfolioModal = true;
        },
        async verifyProfessional(professional) {
            try {
                const accessToken = localStorage.getItem('authToken');
                const formdata = new FormData()
                formdata.append('action', 'accept')
                const response = await fetch(`http://127.0.0.1:8000/api/verify-professional/${professional.professional_id}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                    body: formdata
                });

                if (response.ok) {
                    // Update local state
                    professional.isActive = 1;
                    this.$bvToast.toast('Professional verified successfully', {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    });
                    await this.fetchUserDetails(); // Refresh data
                } else {
                    throw new Error('Failed to verify professional');
                }
            } catch (error) {
                this.$bvToast.toast('Failed to verify professional', {
                    title: 'Error',
                    variant: 'danger',
                    solid: true
                });
            }
        },
        async rejectProfessional(professional) {
            try {
                const accessToken = localStorage.getItem('authToken');
                const formdata = new FormData()
                formdata.append('action', 'reject')
                const response = await fetch(`http://127.0.0.1:8000/api/verify-professional/${professional.id}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                    body: formdata
                });

                if (response.ok) {
                    professional.isActive = 2;
                    this.$bvToast.toast('Professional rejected', {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    });
                    await this.fetchUserDetails(); // Refresh data
                } else {
                    throw new Error('Failed to reject professional');
                }
            } catch (error) {
                this.$bvToast.toast('Failed to reject professional', {
                    title: 'Error',
                    variant: 'danger',
                    solid: true
                });
            }
        },
        getCorrectImagePath(profilePic) {
            if (!profilePic) return this.defaultProfilePic;

            // Get filename from path
            const filename = profilePic.split("\\").pop();

            // Use the complete Flask server URL
            return `http://127.0.0.1:8000/documents/${filename}`;
        },
    }
}
</script>

<style scoped>
.verifyprof {
    min-height: 77vh;
    background-color: #f8f9fa;
    border-radius: 20px;
}

.professionals-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
    padding: 20px 0;
}

.professional-card {
    transition: transform 0.2s, box-shadow 0.2s;
    border: none;
    border-radius: 12px;
    overflow: hidden;
}

.professional-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.card-img-container {
    height: 200px;
    overflow: hidden;
    background-color: #f0f0f0;
}

.profile-pic {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.details-row {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #6c757d;
}

.details-row i {
    width: 16px;
}

.card-actions {
    margin-top: 20px;
}

/* Modal Styles */
.professional-details {
    padding: 15px;
}

.section-title {
    color: #333;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 8px;
    margin-bottom: 15px;
}

.details-grid {
    display: grid;
    gap: 15px;
}

.detail-item {
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 10px;
}

.detail-item .label {
    font-weight: 600;
    color: #495057;
}

.detail-item .value {
    color: #212529;
}

@media (max-width: 768px) {
    .professionals-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }

    .detail-item {
        grid-template-columns: 1fr;
    }
}

.portfolio-badge {
    font-size: 1rem;
    /* Increased font size */
    padding: 8px 16px;
    /* More padding */
    cursor: pointer;
    transition: all 0.2s;
}

.portfolio-badge:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}
</style>