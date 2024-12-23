# UserCard.vue
<template>
  <div class="card user-card">
    <div class="card-content row g-0 p-4">
      <!-- Left column -->
      <div class="col-md-3 text-center">
        <div class="avatar-container mb-3">
          <div class="avatar-wrapper">
            <img :src="getCorrectPath(user.profile_image)" :alt="user.username" class="rounded-circle img-fluid profile-image">
          </div>
        </div>
        <h4 class="user-name mb-2">{{ user.fullname }}</h4>
        <p class="username mb-2">@{{ user.username }}</p>
        <span v-if="user.role==1" class="user-type-badge">Customer</span>
        <span v-else class="user-type-badge">Professional</span>
      </div>

      <!-- Right column -->
      <div class="col-md-9">
        <div class="card-body">
          <!-- Personal Details -->
          <div class="details-section mb-4">
            <h5 class="section-title">Personal Details</h5>
            <div class="row g-3">
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">User-id</span>
                  <span class="detail-value">{{ user.user_id }}</span>
                </div>
              </div>
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">Contact</span>
                  <span class="detail-value">{{ user.contact }}</span>
                </div>
              </div>
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">Email</span>
                  <span class="detail-value">{{ user.email }}</span>
                </div>
              </div>
            </div>
            
            <div v-if="user.role == 1" class="row mt-3">
              <div class="col-12">
                <div class="detail-item">
                  <span class="detail-label">Address</span>
                  <span class="detail-value">{{ user.address }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Work Details -->
          <div v-if="user.role == 2" class="details-section mb-4">
            <h5 class="section-title">Work Details</h5>
            <div class="row g-3">
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">Service</span>
                  <span class="detail-value">{{ serviceMapping[user.service_type] }}</span>
                </div>
              </div>
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">Experience</span>
                  <span class="detail-value">{{ user.experience }}</span>
                </div>
              </div>
              <div class="col-md-4">
                <div class="detail-item">
                  <span class="detail-label">Kudos</span>
                  <span class="detail-value">{{ user.kudos }}</span>
                </div>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-12">
                <div class="detail-item">
                  <span class="detail-label">Description</span>
                  <span class="detail-value">{{ user.description }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="text-end">
            <button class="edit-btn me-2" @click="showEditModal">
              <i class="bi bi-pencil-square"></i> Edit Profile
            </button>
            <button v-if="user.role == 2" class="portfolio-btn" @click="viewPortfolio">
              <i class="bi bi-file-pdf"></i> View Portfolio
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <b-modal v-model="showModal" title="Edit Profile" size="lg" @hidden="resetForm" @ok.prevent="handleSubmit">
      <b-form>
        <b-form-group label="Password" description="Leave blank if you don't want to change">
          <b-form-input type="password" v-model="editForm.password" :state="!formErrors.password"></b-form-input>
          <b-form-invalid-feedback>{{ formErrors.password }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Full Name">
          <b-form-input v-model="editForm.fullname" :state="!formErrors.fullname"></b-form-input>
          <b-form-invalid-feedback>{{ formErrors.fullname }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Contact">
          <b-form-input v-model="editForm.contact" :state="!formErrors.contact"></b-form-input>
          <b-form-invalid-feedback>{{ formErrors.contact }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Email">
          <b-form-input v-model="editForm.email" type="email" :state="!formErrors.email"></b-form-input>
          <b-form-invalid-feedback>{{ formErrors.email }}</b-form-invalid-feedback>
        </b-form-group>

        <!-- Customer fields -->
        <template v-if="user.role == 1">
          <b-form-group label="address">
            <b-form-textarea v-model="editForm.address" rows="2" :state="!formErrors.address"></b-form-textarea>
            <b-form-invalid-feedback>{{ formErrors.address }}</b-form-invalid-feedback>
          </b-form-group>
        </template>

        <!-- Professional fields -->
        <template v-if="user.role == 2">

          <b-form-group label="Work Experience">
            <b-form-input v-model="editForm.experience" :state="!formErrors.experience"></b-form-input>
            <b-form-invalid-feedback>{{ formErrors.experience }}</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Description">
            <b-form-textarea v-model="editForm.description" rows="3" :state="!formErrors.description"></b-form-textarea>
            <b-form-invalid-feedback>{{ formErrors.description }}</b-form-invalid-feedback>
          </b-form-group>

          <b-form-group label="Portfolio (PDF)">
            <b-form-file v-model="editForm.portfolio" accept=".pdf"></b-form-file>
          </b-form-group>
        </template>

        <b-form-group label="Profile Image">
          <b-form-file v-model="editForm.profile_image" accept="image/*"></b-form-file>
        </b-form-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true,
    }
  },

  data() {
    return {
      showModal: false,
      formErrors: {},
      editForm: {
        password: '',
        fullname: '',
        contact: '',
        email: '',
        address: '',
        experience: '',
        description: '',
        profile_image: null,
        portfolio: null,
      defaultProfilePic: 'https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_1280.png'
    },
    serviceMapping : {1:"General Home Cleaning",2:"Deep Cleaning",3:"Kitchen Cleaning",4:"Bathroom Cleaning",5:"Sofa and Carpet Cleaning",6:"Window and Glass Cleaning",7:"Electrical Repairs",8:"Fan Installation and Repairs",9:"Light and Socket Fitting",10:"Wiring and Electrical Panel Work",11:"Appliance Installation",12:"Leak Repairs",13:"Pipe Fitting and Replacement",14:"Faucet and Sink Repair",15:"Water Tank Cleaning",16:"Bathroom Fittings Installation",17:"AC Installation and Servicing",18:"Refrigerator Repair",19:"Washing Machine Repair",20:"Microwave Oven Repair",21:"Water Purifier Installation and Servicing",22:"Furniture Repair",23:"Custom Furniture Building",24:"Door and Window Fitting",25:"Lock and Handle Repairs",26:"Modular Kitchen Installations",27:"Wall Painting",28:"Textured Wall Designs",29:"Polishing and Wood Painting",30:"Waterproofing Solutions",31:"Termite Control",32:"Cockroach Control",33:"Mosquito Control",34:"Bed Bug Control",35:"Rodent Control",36:"Flooring and Tiling",37:"Bathroom Remodeling",38:"Waterproofing",39:"Masonry Work",40:"Lawn Mowing and Maintenance",41:"Plant Installation",42:"Garden Designing",43:"Tree Trimming and Removal",44:"CCTV Installation",45:"Home Automation",46:"Doorbell and Intercom Installation",47:"Handyman Services",48:"Pack and Move Services",49:"Home Sanitization Services",50:"Curtain and Blind Installation"},
  }
  },

  methods: {
    showEditModal() {
      this.editForm = { 
        password: '',
        ...this.user,
        profile_image: null,
        portfolio: null
      };
      this.showModal = true;
    },

    resetForm() {
      this.editForm = {
        password: '',
        fullname: '',
        contact: '',
        email: '',
        address: '',
        experience: '',
        description: '',
        profile_image: null,
        portfolio: null
      };
      this.formErrors = {};
    },

    validateForm() {
      this.formErrors = {};
      const errors = {};

      // Only validate password if it's provided
      if (this.editForm.password && this.editForm.password.length < 6) {
        errors.password = 'Password must be at least 6 characters';
      }

      // Only validate fields that have been modified
      if (this.editForm.fullname !== this.user.fullname && !this.editForm.fullname?.trim()) {
        errors.fullname = 'Full name is required';
      }
      
      if (this.editForm.contact !== this.user.contact && !this.editForm.contact?.trim()) {
        errors.contact = 'Contact is required';
      }

      if (this.editForm.email !== this.user.email) {
        if (!this.editForm.email?.trim()) {
          errors.email = 'Email is required';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.editForm.email)) {
          errors.email = 'Invalid email format';
        }
      }

      if (this.user.role == 1 && this.editForm.address !== this.user.address && !this.editForm.address?.trim()) {
        errors.address = 'Address is required';
      }

      if (this.user.role == 2) {
        if (this.editForm.experience !== this.user.experience && !this.editForm.experience?.trim()) {
          errors.experience = 'Experience is required';
        }
      }

      this.formErrors = errors;
      return Object.keys(errors).length === 0;
    },

    async handleSubmit() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const formData = new FormData();
        
        // Only append fields that have changed
        Object.keys(this.editForm).forEach(key => {
          if (key === 'profile_image' || key === 'portfolio') {
            if (this.editForm[key] instanceof File) {
              formData.append(key, this.editForm[key]);
            }
          } else if (key === 'password') {
            if (this.editForm.password) {
              formData.append(key, this.editForm[key]);
            }
          } else if (this.editForm[key] !== this.user[key]) {
            formData.append(key, this.editForm[key]);
          }
        });

        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }

        const response = await fetch('http://127.0.0.1:8000/api/user', {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
          },
          body: formData
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Update failed');
        }

        this.$bvToast.toast('Profile updated successfully', {
          title: 'Success',
          variant: 'success',
          solid: true
        });

        this.$emit('user-updated');
        this.showModal = false;
        this.resetForm();

      } catch (error) {
        console.error('Error updating profile:', error);
        this.$bvToast.toast(error.message || 'Failed to update profile', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },

    viewPortfolio() {
      if (this.user.portfolio) {
        window.open(this.getCorrectPath(this.user.portfolio), '_blank');
      }
    },

    getCorrectPath(path) {
      if (!path) return this.defaultProfilePic;
      const filename = path.split('\\').pop();
      return `http://127.0.0.1:8000/documents/${filename}`;
    }
  }
}
</script>


<style scoped>
.user-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
}

.card-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0));
}

.avatar-wrapper {
  width: 150px;
  height: 150px;
  margin: 0 auto;
  border: 4px solid rgba(46, 139, 87, 0.5);
  border-radius: 50%;
  padding: 4px;
  transition: transform 0.3s ease;
}

.avatar-wrapper:hover {
  transform: scale(1.05);
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.user-name {
  color: #2E8B57;
  font-weight: 600;
}

.username {
  color: #666;
  font-size: 0.9rem;
}

.user-type-badge {
  background: linear-gradient(135deg, #2E8B57, #3CB371);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.section-title {
  color: #2E8B57;
  font-weight: 600;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(46, 139, 87, 0.2);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.detail-label {
  color: #666;
  font-size: 0.85rem;
  font-weight: 600;
}

.detail-value {
  color: #2E8B57;
  font-weight: 700;
}

.edit-btn, .portfolio-btn {
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: white;
}

.edit-btn {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
}

.portfolio-btn {
  background: linear-gradient(135deg, #2E8B57, #3CB371);
  box-shadow: 0 4px 15px rgba(46, 139, 87, 0.2);
}

.edit-btn:hover, .portfolio-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(46, 139, 87, 0.3);
}

.edit-btn:active, .portfolio-btn:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .avatar-wrapper {
    width: 120px;
    height: 120px;
  }
  
  .card-content {
    padding: 1.5rem !important;
  }
}
</style>