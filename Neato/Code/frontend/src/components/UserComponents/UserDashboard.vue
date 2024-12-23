<template>
  <div class="main">
    <!-- Header with refresh controls -->
    <div class="justify-content-between align-items-center mb-2" v-if="userData?.isActive==1 || userData?.is_blocked ==false">
      <h2>User Dashboard</h2>
    </div>
    <form 
      v-if="userData.role !== 2" 
      @submit.prevent="handleSearch" 
      class="d-flex" 
      role="search"
    >
      <input 
        v-model="searchQuery" 
        class="form-control me-2" 
        type="search" 
        placeholder="Search Services" 
        aria-label="Search"
      >
      <button class="btn btn-outline-success" type="submit" id="search">
        <i class="bi bi-search"></i>
      </button>
    </form>

    <div class="col-md-12">
      <div v-if="userData &&  (userData?.isActive==1 || userData?.is_blocked==false)">
        <div class="row mb-4">
          <!-- Tools box -->
          <div class="tools-box mt-4">
            <div class="card mt-4">
              <div class="card-header bg-light">
                <h5 class="mb-0">TOOLS</h5>
              </div>
              <div class="card-body">
                <div class="list-group">
                  <a 
                    class="list-group-item list-group-item-action" 
                    @click="clearSearch"
                  >
                    Dashboard
                  </a>
                  <router-link 
                    to="/user/user-services" 
                    class="list-group-item list-group-item-action"
                  >
                    Services Requests
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Content area -->
          <div class="col-8" id="card">
            <router-view v-if="$route.name === 'UserServices'" />
            <template v-else>
              <template v-if="!isSearching">

                  <UserCard :user="userData" @user-updated="fetchUserData" />
              </template>

              <template v-else>
                <div class="search-results-container">
                  <SearchResults 
                    :query="searchQuery"
                    @close-search="clearSearch"
                  />
                  <button 
                    @click="clearSearch" 
                    class="btn btn-outline-secondary mb-3"
                  >
                    <i class="bi bi-arrow-left"></i> Back to Profile
                  </button>
                </div>
              </template>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserCard from '@/components/UserComponents/UserCard.vue'
import SearchResults from '@/components/UserComponents/SearchResults.vue'


export default {
  name: 'UserDashboard',
  
  components: {
    UserCard,
    SearchResults,
  },

  data() {
    return {
      userData: {
        'role' : 1
      },
      searchQuery: '',
      isSearching: false,
      searchResults: []
    }
  },

  async created() {
    await this.fetchUserData()
    if(this.userData?.role === 2 && this.userData?.isActive === 0) {
      localStorage.removeItem('authToken');
      alert("You are not verified yet . Logging Out. Please try again later");
      this.$router.push('/');
  }else if(this.userData?.role===2 && this.userData?.is_blocked==true){
    localStorage.removeItem('authToken');
      alert("You are blocked by Admin. For Suspicious activity. Contact Admin @ example.gmail.com");
      this.$router.push('/');
  }
  },

  methods: {
    async fetchUserData() {
      const accessToken = localStorage.getItem('authToken')
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.message}`)
        }

        const data = await response.json()
        console.log('Raw API response:', data)
        this.rawApiData = data

        const isCustomer = 'customerdata' in data
        const specificData = isCustomer ? data.customerdata : data.professionaldata

        const transformedData = {
          username: data.userdata.username,
          role: data.userdata.role,
          user_id: data.userdata.user_id,
          is_blocked : data.userdata.is_blocked
        }

        if (isCustomer) {
          transformedData.address = specificData.address
          transformedData.contact = specificData.contact
          transformedData.email = specificData.email
          transformedData.fullname = specificData.fullname
          transformedData.profile_image = specificData.profile_image
        } else {
          transformedData.service_type = specificData.service_type
          transformedData.experience = specificData.experience
          transformedData.kudos = specificData.kudos
          transformedData.contact = specificData.contact
          transformedData.description = specificData.description
          transformedData.email = specificData.email
          transformedData.fullname = specificData.fullname
          transformedData.profile_image = specificData.profile_image
          transformedData.portfolio = specificData.document_path
          transformedData.isActive = specificData.isActive
        }

        this.userData = transformedData

      } catch (error) {
        console.error('Error in fetchUserData:', error)
        this.error = `Failed to fetch user data: ${error.message}`
      }
    },

    handlePortfolioView(userId) {
      console.log('Viewing portfolio for user:', userId)
      this.$router.push(`http://127.0.0.1:8000/documents/${userId}.pdf`)
    },

    getCorrectPath(profilePic) {
      if (!profilePic) return this.defaultProfilePic

      const filename = profilePic.split('\\').pop()
      return `http://127.0.0.1:8000/documents/${filename}`
    },

    async handleSearch(e) {
      e.preventDefault()
      if (this.searchQuery.trim()) {
        this.isSearching = true
      }
    },

    clearSearch() {
      this.searchQuery = ''
      this.isSearching = false
      this.searchResults = []
      if (this.$route.name !== 'UserDashboard') {
        this.$router.push('/user')
      }
    },
  },
}
</script>

<style scoped>
.router-link-active {
  background-color: #198754 !important;
  color: white !important;
}

#id{
  margin-left: 100px;
}
.main{
  margin:100px;
}
h2 {
  margin-left: 20px;
  background-color: rgb(128, 148, 17);
  max-width: 1650px;
  max-height: 100px;
  border-radius: 80px;
  border: 5px black;
  transition: background-color 0.5s;
}
h2:hover{
  background-color: rgb(207, 130, 58);
  border-color: rgb(128, 148, 17)
}
.container {
    margin-top: 20px;
    max-width:1200px;
}

pre {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.25rem;
  white-space: pre-wrap;
  word-wrap: break-word;
}

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
}

.tools-box {
  border-radius: 20px;
  margin: 20px;
  max-width: 400px;
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>