# AdminServices.vue
<template>
  <div class="services">
    <div class="card">
      <div class="card-header">
        <h4>Service Management</h4>
      </div>
      <div class="card-body">
        <div class="d-flex justify-content-end mb-3">
          <b-button variant="success" @click="showCreateModal = true">
            <i class="bi bi-plus-circle"></i> Create Service
          </b-button>
        </div>
        <div class="services-container">
          <div class="row g-4">
            <!-- Service Cards -->
            <div class="col-md-4" v-for="service in services.services" :key="service.id">
              <b-card class="h-100 service-card">
                <b-card-title class="d-flex justify-content-between align-items-center">
                  {{ service.service_name }}
                  <b-button variant="outline-primary" size="sm" @click="showUpdateModal(service)">
                    <i class="bi bi-pencil"></i> Update
                  </b-button>
                  <b-button variant="outline-danger" size="sm" @click="confirmDelete(service)">
                    <i class="bi bi-trash"></i> Delete
                  </b-button>
                </b-card-title>

                <b-card-text>
                  <p class="description">{{ service.description }}</p>
                  <div class="service-details">
                    <p><strong>Price:</strong> ${{ service.price }}</p>
                    <p><strong>Time Required:</strong> {{ formatTime(service.time_required) }}</p>
                    <p><strong>Category:</strong> {{ service.category }}</p>
                    <p><strong>Created:</strong> {{ service.date_created }}</p>
                  </div>
                </b-card-text>
              </b-card>
            </div>
            <!-- Update Modal -->
            <b-modal id="update-service-modal" v-model="showModal" title="Update Service" @ok.prevent="handleUpdate"
              @hidden="resetForm" hide-footer>
              <form @submit.prevent="handleUpdate">
                <b-form-group label="Service Name">
                  <b-form-input v-model="updateForm.service_name" required></b-form-input>
                </b-form-group>

                <b-form-group label="Description">
                  <b-form-textarea v-model="updateForm.description" rows="3" max-rows="6"></b-form-textarea>
                </b-form-group>

                <b-form-group label="Price">
                  <b-form-input v-model.number="updateForm.price" type="number" required></b-form-input>
                </b-form-group>

                <b-form-group label="Time Required (minutes)">
                  <b-form-input v-model.number="updateForm.time_required" type="number" required></b-form-input>
                </b-form-group>

                <b-form-group label="Category">
                  <b-form-input v-model="updateForm.category"></b-form-input>
                </b-form-group>

                <div class="mt-3 d-flex justify-content-end">
                  <b-button variant="secondary" class="mr-2" @click="showModal = false">Cancel</b-button>
                  <b-button variant="primary" type="submit">Update Service</b-button>
                </div>
              </form>
            </b-modal>
            <!-- Add this after your update modal -->
            <b-modal id="create-service-modal" v-model="showCreateModal" title="Create New Service" @hidden="resetForm"
              hide-footer>
              <form @submit.prevent="handleCreate">
                <b-form-group label="Service Name">
                  <b-form-input v-model="createForm.service_name" required></b-form-input>
                </b-form-group>

                <b-form-group label="Description">
                  <b-form-textarea v-model="createForm.description" rows="3" max-rows="6"></b-form-textarea>
                </b-form-group>

                <b-form-group label="Price">
                  <b-form-input v-model.number="createForm.price" type="number" required></b-form-input>
                </b-form-group>

                <b-form-group label="Time Required (minutes)">
                  <b-form-input v-model.number="createForm.time_required" type="number" required></b-form-input>
                </b-form-group>

                <b-form-group label="Category">
                  <b-form-input v-model="createForm.category" required></b-form-input>
                </b-form-group>

                <div class="mt-3 d-flex justify-content-end">
                  <b-button variant="secondary" class="me-2" @click="showCreateModal = false">Cancel</b-button>
                  <b-button variant="success" type="submit">Create Service</b-button>
                </div>
              </form>
            </b-modal>

            <!-- Delete Confirmation Modal -->
            <b-modal id="delete-confirmation-modal" v-model="showDeleteModal" title="Confirm Delete" @ok="handleDelete">
              Are you sure you want to delete this service?
            </b-modal>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminServices',
  data() {
    return {
      services: [],
      showModal: false,
      showCreateModal: false,
      showDeleteModal: false,
      selectedService: null,
      createForm: {
        service_name: '',
        description: '',
        price: '',
        time_required: '',
        category: ''
      },
      updateForm: {
        service_id: null,
        service_name: '',
        description: '',
        price: '',
        time_required: '',
        category: ''
      },
      loading: false,
      error: null
    }
  },
  async created() {
    await this.fetchServices()
  },
  methods: {
    async fetchServices() {
      try {
        this.loading = true
        const response = await fetch('http://127.0.0.1:8000/api/services', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        })
        const data = await response.json()
        if (response.ok) {
          console.log(data)
          this.services = data

        } else {
          throw new Error(data.message || 'Failed to fetch services')
        }
      } catch (error) {
        console.error('Error:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    formatTime(minutes) {
      const hours = Math.floor(minutes / 60)
      const remainingMinutes = minutes % 60
      if (hours === 0) return `${minutes} minutes`
      if (remainingMinutes === 0) return `${hours} hour${hours > 1 ? 's' : ''}`
      return `${hours} hour${hours > 1 ? 's' : ''} ${remainingMinutes} minute${remainingMinutes > 1 ? 's' : ''}`
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },

    showUpdateModal(service) {
      this.updateForm = { ...service }
      this.showModal = true
    },

    async handleUpdate(bvModalEvent) {
      bvModalEvent.preventDefault()
      console.log(this.updateForm);
      try {
        const formData = new FormData()
        formData.append('service_name', this.updateForm.service_name);
        formData.append('description', this.updateForm.description);
        formData.append('price', this.updateForm.price);
        formData.append('time_required', this.updateForm.time_required);
        formData.append('category', this.updateForm.category);

        console.log(formData);

        const response = await fetch(`http://127.0.0.1:8000/api/service/${this.updateForm.service_id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          },
          body: formData
        })

        const data = await response.json()
        console.log(data);

        if (response.ok) {
          // Update the service in the local array
          await this.fetchServices()
          this.$bvToast.toast('Service updated successfully', {
            title: 'Success',
            variant: 'success',
            solid: true
          })
          this.showModal = false
        } else {
          console.log('Reponse not okay');
          throw new Error(data.message || 'Failed to update service')
        }
      } catch (error) {
        console.error('Error-catch:', error)
        this.$bvToast.toast(error.message, {
          title: 'Error',
          variant: 'danger',
          solid: true
        })
      }
    },
    async handleCreate() {
      try {
        const formData = new FormData()
        formData.append('service_name', this.createForm.service_name)
        formData.append('description', this.createForm.description)
        formData.append('price', this.createForm.price)
        formData.append('time_required', this.createForm.time_required)
        formData.append('category', this.createForm.category)

        const response = await fetch('http://127.0.0.1:8000/api/create-service', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          },
          body: formData
        })

        const data = await response.json()

        if (response.ok) {
          await this.fetchServices()
          this.$bvToast.toast('Service created successfully', {
            title: 'Success',
            variant: 'success',
            solid: true
          })
          this.showCreateModal = false
          this.resetForm()
          await this.fetchServices() // Refresh the list
        } else {
          throw new Error(data.message || 'Failed to create service')
        }
      } catch (error) {
        console.error('Error:', error)
        this.$bvToast.toast(error.message, {
          title: 'Error',
          variant: 'danger',
          solid: true
        })
      }
    },

    confirmDelete(service) {
      this.selectedService = service
      this.showDeleteModal = true
    },

    async handleDelete() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/service/${this.selectedService.service_id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          }
        })

        if (response.ok) {
          await this.fetchServices();
          this.$bvToast.toast('Service deleted successfully', {
            title: 'Success',
            variant: 'success',
            solid: true
          })
        } else {
          const data = await response.json()
          throw new Error(data.message || 'Failed to delete service')
        }
      } catch (error) {
        console.error('Error:', error)
        this.$bvToast.toast(error.message, {
          title: 'Error',
          variant: 'danger',
          solid: true
        })
      }
    },

    resetForm() {
      this.createForm = {
        service_name: '',
        description: '',
        price: '',
        time_required: '',
        category: ''
      }
      this.updateForm = {
        service_id: null,
        service_name: '',
        description: '',
        price: '',
        time_required: '',
        category: ''
      }
    }
  }
}
</script>

<style scoped>
.card-header {
  background-color: aquamarine;
}

.services-container {
  padding: 20px;
}

.service-card {
  transition: transform 0.2s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.service-card:hover {
  transform: translateY(-5px);
}

.description {
  color: #666;
  margin-bottom: 15px;
  min-height: 48px;
}

.service-details {
  font-size: 0.9rem;
}

.service-details p {
  margin-bottom: 0.5rem;
}

/* Loading state */
.loading {
  text-align: center;
  padding: 20px;
}

/* Error state */
.error {
  color: #dc3545;
  text-align: center;
  padding: 20px;
}
</style>