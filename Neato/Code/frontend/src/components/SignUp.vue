<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <!-- Customer Signup Form -->
        <div v-if="!showProfessionalForm" class="card shadow-lg">
          <div class="card-body p-4" id="form">
            <div class="row">
              <div class="col-3"></div>
              <h2 class="col-6  text-success mb-4">Customer </h2>
              <button @click="showProfessionalForm = true"
                class="col-3 text-end btn btn-link text-success text-decoration-none">
                Professional<i class="bi bi-arrow-right"></i>
              </button>
            </div>
            <form @submit.prevent="submitCustomerForm">
              <!-- Personal Information -->
              <div class="row">
                <div class="col-md-6 bg-light p-4 rounded mb-3">
                  <h3 class="h5 text-success mb-3">Personal Information</h3>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">First Name *</label>
                      <input v-model="customerForm.firstName" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-4">
                      <label class="form-label">Last Name *</label>
                      <input v-model="customerForm.lastName" type="text" class="form-control" required>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <label for="contact" class="form-label">Contact No.</label>
                      <input v-model="customerForm.contact" type="tel" maxlength="10" minlength="10"
                        class="form-control" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Email *</label>
                      <input v-model="customerForm.email" type="email" class="form-control" required>
                      <p class="small text-muted">Example@email.com</p>
                    </div>
                  </div>
                </div>

                <!-- Account Information -->
                <div class="col-md-6 bg-light p-4 rounded mb-3">
                  <h3 class="h5 text-success mb-3">Account Details</h3>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Username *</label>
                      <input v-model="customerForm.username" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Password *</label>
                      <input v-model="customerForm.password" type="password" class="form-control" minlength="8"
                        maxlength="15" required>
                      <p class="small text-muted mb-1">
                        <span
                          :class="{ 'text-success': lengthValid, 'text-danger': !lengthValid && customerForm.password }">8-15
                          Char</span>,
                        <span
                          :class="{ 'text-success': uppercaseValid, 'text-danger': !uppercaseValid && customerForm.password }">A-Z</span>,
                        <span
                          :class="{ 'text-success': lowercaseValid, 'text-danger': !lowercaseValid && customerForm.password }">a-z</span>,
                        <span
                          :class="{ 'text-success': numberValid, 'text-danger': !numberValid && customerForm.password }">0-9</span>,
                        <span
                          :class="{ 'text-success': specialValid, 'text-danger': !specialValid && customerForm.password }">!@#$%^&*</span>
                      </p>
                    </div>
                    <div class="col-md-6 mb-2">
                      <label class="form-label">Confirm Password *</label>
                      <input v-model="customerForm.confirmPassword" type="password" class="form-control" minlength="8"
                        maxlength="15" required>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row">
                <!-- Address Information -->
                <div class="col-md-8 bg-light p-4 rounded mb-3">
                  <h3 class="h5 text-success mb-3">Address</h3>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Flat/House/Apartment No. *</label>
                      <input v-model="customerForm.houseNo" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Locality/Area *</label>
                      <input v-model="customerForm.locality" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label class="form-label">City *</label>
                      <input v-model="customerForm.city" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label class="form-label">State *</label>
                      <input v-model="customerForm.state" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label class="form-label">Pin Code *</label>
                      <input v-model="customerForm.pincode" type="number" class="form-control" min:000000 minlength="6"
                        maxlength="6" placeholder="123456" required>
                    </div>
                  </div>
                </div>


                <!-- Profile Image -->
                <div class="col-md-4 bg-light p-4 rounded mb-3">
                  <h3 class="h5 text-success mb-3">Profile Image</h3>
                  <div class="d-flex justify-content-center">
                    <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                      style="width: 100px; height: 100px;">
                      <img v-if="imagePreview" :src="imagePreview" class="rounded-circle"
                        style="width: 100px; height: 100px; object-fit: cover;">
                      <i v-else class="fas fa-user fa-2x text-white"></i>
                    </div>
                  </div>
                  <div class="mt-4">
                    <label class="btn btn-success">
                      Upload Photo
                      <input type="file" class="d-none" accept="image/*" @change="handleImageUpload">
                    </label>
                    <p class="small text-muted mt-2">Maximum file size: 5MB</p>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn btn-success w-100 py-2">
                Create Account
              </button>
            </form>
          </div>
        </div>

        <!-- Professional Signup Form -->
        <div v-else class="card shadow-lg">
          <div class="card-body p-4">
            <div class="row">
              <div class="col-3"></div>
              <h2 class=" col-6 text-success mb-4">Professional</h2>
              <button @click="showProfessionalForm = false"
                class=" col-3 text-end btn btn-link text-success text-decoration-none">
                <i class="bi bi-arrow-left"></i>
                Customer
              </button>
            </div>
            <form @submit.prevent="submitProfessionalForm">
              <!-- Personal Information -->
              <div class="row">
                <div class="col-md-6 bg-light p-4 rounded mb-4">
                  <h3 class="h5 text-success mb-3">Personal Information</h3>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">First Name *</label>
                      <input v-model="professionalForm.firstName" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Last Name *</label>
                      <input v-model="professionalForm.lastName" type="text" class="form-control" required>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Contact No. *</label>
                      <input v-model="professionalForm.contact" type="contact" class="form-control" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Email *</label>
                      <input v-model="professionalForm.email" type="email" class="form-control" required>
                      <p class="small text-muted">Example@email.com</p>
                    </div>
                  </div>
                </div>

                <!-- Professional Information -->
                <div class="col-md-6 bg-light p-4 rounded mb-4">
                  <h3 class="h5 text-success mb-3">Professional Details</h3>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Service Type *</label>
                      <select v-model="professionalForm.service_type" class="form-select" placeholder="Select service" required>
                        <option value="">Select a service</option>
                        <option v-for="service in service_data" 
                                :key="service.service_id" 
                                :value="service.service_id">
                          {{service.service_name}}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Years of Experience *</label>
                      <input v-model="professionalForm.experience" type="number" min="0" class="form-control" required>
                    </div>
                    <div class="col-md-7 mb-3">
                      <label class="form-label">Description</label>
                      <textarea v-model="professionalForm.description" type="text" class="form-control" rows="1"
                        placeholder="100 Characters" required>
                    </textarea>
                    </div>
                    <div class="col-md-5 mb-3">
                      <label class="form-label">Service Pincode</label>
                      <input v-model="professionalForm.service_pincode" type="number" min="0" class="form-control" required>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Portfolio Documents -->
              <div class="row">
                <div class="col-md-5 bg-light p-4 rounded mb-4">
                  <h3 class="h5 text-success mb-4">Profile & Portfolio</h3>
                  <div class="row">
                    <div class="mb-3">
                      <label class="form-label">Profile Image</label>
                      <div class="input-group">
                        <label class="input-group-text bg-white">
                          <i class="fas fa-images text-success"></i>
                        </label>
                        <input type="file" class="form-control" accept="image/*" @change="handleImageUpload" required>
                      </div>
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Work Portfolio (PDF)</label>
                      <div class="input-group">
                        <label class="input-group-text bg-white">
                          <i class="fas fa-images text-success"></i>
                        </label>
                        <input type="file" class="form-control" accept=".pdf" @change="handlePortfolioUpload" required>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Account Information -->
                <div class="col-md-7 bg-light pt-4 rounded mb-4">
                  <h3 class="h5 text-success mb-3">Account Details</h3>
                  <div class="row">
                    <div class="col-md-6">
                      <label class="form-label">Username *</label>
                      <input v-model="professionalForm.username" type="text" class="form-control" required>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">Password *</label>
                      <input v-model="professionalForm.password" type="password" class="form-control" required>
                      <p class="small text-muted mb-1">
                        <span
                          :class="{ 'text-success': profLengthValid, 'text-danger': !profLengthValid && professionalForm.password }">8-15
                          Char</span>,
                        <span
                          :class="{ 'text-success': profUppercaseValid, 'text-danger': !profUppercaseValid && professionalForm.password }">A-Z</span>,
                        <span
                          :class="{ 'text-success': profLowercaseValid, 'text-danger': !profLowercaseValid && professionalForm.password }">a-z</span>,
                        <span
                          :class="{ 'text-success': profNumberValid, 'text-danger': !profNumberValid && professionalForm.password }">0-9</span>,
                        <span
                          :class="{ 'text-success': profSpecialValid, 'text-danger': !profSpecialValid && professionalForm.password }">!@#$%^&*</span>
                      </p>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Confirm Password *</label>
                      <input v-model="professionalForm.confirmPassword" type="password" class="form-control" required>
                    </div>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn btn-success w-100 py-2">
                Create Professional Account
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignUp',
  data() {
    return {
      showProfessionalForm: false,
      customerForm: {
        firstName: '',
        lastName: '',
        contact: null,
        email: '',
        houseNo: '',
        locality: '',
        city: '',
        state: '',
        pincode: null,
        username: '',
        password: '',
        confirmPassword: '',
        profile_image: '',
      },
      professionalForm: {
        firstName: '',
        lastName: '',
        contact: null,
        service_type: '',
        experience: null,
        description: '',
        username: '',
        email: '',
        service_pincode: null,
        password: '',
        confirmPassword: '',
        profile_image: '',
        portfolio: '',
      },
      service_data: [],
      imagePreview: null,
    }
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file && file.size <= 5 * 1024 * 1024) { // 5MB limit
        if (this.showProfessionalForm) {
          this.professionalForm.profile_image = file;
          this.imagePreview = URL.createObjectURL(file);
        }
        else {
          this.customerForm.profile_image = file;
          this.imagePreview = URL.createObjectURL(file);
        }
      } else {
        alert('File size should not exceed 5MB')
        event.target.value = ''
      }
    },
    handlePortfolioUpload(event) {
      const file = event.target.files[0]
      if (file && file.size <= 10 * 1024 * 1024) { // 10MB limit for PDF
        this.professionalForm.portfolio = file;
      } else {
        alert('PDF size should not exceed 10MB')
        event.target.value = ''
      }
    },
    async submitCustomerForm() {
      // Validate passwords match
      if (this.customerForm.password !== this.customerForm.confirmPassword) {
        alert('Passwords do not match')
        return
      }
      if (!this.isCustomerPasswordValid) {
        alert('Password is not valid')
        return
      }
      if (!this.customerForm.firstName || !this.customerForm.lastName || !this.customerForm.contact || !this.customerForm.email) {
        alert("Please fill all personal details.")
        return
      }
      if (!this.customerForm.username) {
        alert('Please fill your username!')
        return
      }
      if (!this.customerForm.houseNo || !this.customerForm.locality || !this.customerForm.city || !this.customerForm.state || !this.customerForm.pincode) {
        alert('Please complete your Address.')
        return
      }
      if (this.customerForm.pincode.length != 6) {
        alert('Provide valid Pin code.')
        return
      }
      // TODO: Add API call to submit customer form
      let formData = new FormData();
      formData.append("firstName", this.customerForm.firstName);
      formData.append("lastName", this.customerForm.lastName);
      formData.append("contact", this.customerForm.contact);
      formData.append("email", this.customerForm.email);
      formData.append("houseNo", this.customerForm.houseNo);
      formData.append("locality", this.customerForm.locality);
      formData.append("city", this.customerForm.city);
      formData.append("state", this.customerForm.state);
      formData.append("pincode", this.customerForm.pincode);
      formData.append("username", this.customerForm.username);
      formData.append("password", this.customerForm.password);
      formData.append("confirmPassword", this.customerForm.confirmPassword);
      formData.append("profile_image", this.customerForm.profile_image);

      try {
        console.log('now pinging API')
        let response = await fetch("http://127.0.0.1:8000/api/customer-signup", {
          method: "POST",
          body: formData,
        });
        let data = await response.json();
        console.log('full response:', response);
        console.log("API Response:", data);

        if (response.ok) {
          alert("Signup successful!");
          this.$router.push({ name: "LoginPage" });
        } else {
          alert(data.message || "Signup failed. Please try again.");
        }
      } catch (error) {
        console.error("Signup Error:", error);
      }
      console.log('Customer form submitted:', this.customerForm)
    },
    async submitProfessionalForm() {
      // Validate passwords match
      if (this.professionalForm.password !== this.professionalForm.confirmPassword) {
        alert('Passwords do not match')
        return
      }
      if (!this.isProfPasswordValid) {
        alert('Password is ot valid')
        return
      }

      if (!this.professionalForm.firstName || !this.professionalForm.lastName || !this.professionalForm.contact || !this.professionalForm.email) {
        alert("Please fill all personal details.")
        return
      }
      if (!this.professionalForm.service_type || !this.professionalForm.experience) {
        alert('Serrvice Type or Experience is missing')
        return
      }
      if (!this.professionalForm.username) {
        alert('Fill your username!')
        return
      }
      if (!this.professionalForm.profile_image) {
        alert('Upload profile image.')
        return
      }
      if (!this.professionalForm.portfolio) {
        alert('Please upload your work portfolio!')
        return
      }
      // TODO: Add API call to submit professional form
      try {
        let formData = new FormData();
        formData.append("firstName", this.professionalForm.firstName);
        formData.append("lastName", this.professionalForm.lastName);
        formData.append("contact", this.professionalForm.contact);
        formData.append("service_pincode", this.professionalForm.service_pincode);
        formData.append("service_type", this.professionalForm.service_type);
        formData.append("experience", this.professionalForm.experience);
        formData.append("description", this.professionalForm.description);
        formData.append("username", this.professionalForm.username);
        formData.append("email", this.professionalForm.email);
        formData.append("password", this.professionalForm.password);
        formData.append("confirmPassword", this.professionalForm.confirmPassword);
        formData.append("profile_image", this.professionalForm.profile_image);
        formData.append("portfolio", this.professionalForm.portfolio);

        let response = await fetch("http://127.0.0.1:8000/api/professional-signup", {
          method: "POST",
          body: formData
        });

        let data = await response.json();
        console.log("API Response:", data);

        if (response.ok) {
          alert("Signup successful!");
          this.$router.push({ name: "LoginPage" });
        } else {
          alert(data.message || "Signup failed. Please try again.");
        }
      } catch (error) {
        console.error("Signup Error:", error);
      }
      console.log('Professional form submitted:', this.professionalForm)
    },
    async fetchProfessionalServiceTypes() {
      try {
        console.log("Fetching service types...");
        let response = await fetch("http://127.0.0.1:8000/api/services", {
          method: "GET",
        });
        let data = await response.json();

        if (response.ok) {
          console.log("Service Types:", data);
          this.service_data = data['services'];
        } else {
          alert(data.message || "Failed to load service types.");
        }
      } catch (error) {
        console.error("Error fetching service types:", error);
      }
    },
  },
  computed: {
    // Customer password validations
    lengthValid() {
      return this.customerForm.password.length >= 8 && this.customerForm.password.length <= 15;
    },
    uppercaseValid() {
      return /[A-Z]/.test(this.customerForm.password);
    },
    lowercaseValid() {
      return /[a-z]/.test(this.customerForm.password);
    },
    numberValid() {
      return /[0-9]/.test(this.customerForm.password);
    },
    specialValid() {
      return /[!@#$%^&*]/.test(this.customerForm.password);
    },
    isCustomerPasswordValid() {
      return this.lengthValid && this.uppercaseValid && this.lowercaseValid &&
        this.numberValid && this.specialValid;
    },

    // Professional password validations
    profLengthValid() {
      return this.professionalForm.password.length >= 8 && this.professionalForm.password.length <= 15;
    },
    profUppercaseValid() {
      return /[A-Z]/.test(this.professionalForm.password);
    },
    profLowercaseValid() {
      return /[a-z]/.test(this.professionalForm.password);
    },
    profNumberValid() {
      return /[0-9]/.test(this.professionalForm.password);
    },
    profSpecialValid() {
      return /[!@#$%^&*]/.test(this.professionalForm.password);
    },
    isProfPasswordValid() {
      return this.profLengthValid && this.profUppercaseValid && this.profLowercaseValid &&
        this.profNumberValid && this.profSpecialValid;
    },   
  },
  watch: {
    showProfessionalForm() {
      if (this.showProfessionalForm) {
        console.log("Professional form selected.");
        this.fetchProfessionalServiceTypes(); // Call API when `showProfessionalForm` changes to true
      }
    }
  }
}
</script>

<style scoped>
.container {
  margin-top: 75px;
}

.card {
  border: none;
  border-radius: 1rem;
}

.form-control:focus,
.form-select:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}

.btn-success {
  background-color: #198754;
}

.btn-success:hover {
  background-color: #157347;
}

.text-success {
  color: #198754 !important;
}
</style>