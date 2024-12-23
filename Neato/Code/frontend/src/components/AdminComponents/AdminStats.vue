<template>
    <div class="container mt-4">
      <!-- Summary Cards -->
      <div class="row mb-4">
        <div class="col-md-3" v-for="(value, key) in summary" :key="key">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ formatTitle(key) }}</h5>
              <h3>{{ value }}</h3>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Charts Row -->
      <div class="row">
        <!-- Request Status Chart -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5>Service Requests by Status</h5>
              <canvas ref="statusChart"></canvas>
            </div>
          </div>
        </div>
  
        <!-- Top Services Chart -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5>Top Services</h5>
              <canvas ref="servicesChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'AdminStats',
    data() {
      return {
        summary: {},
        statusChart: null,
        servicesChart: null
      }
    },
  
    async created() {
      await this.fetchAnalytics()
    },
  
    mounted() {
      this.initializeCharts()
    },
  
    methods: {
      async fetchAnalytics() {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/admin/analytics', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
          })
          const data = await response.json()
          this.summary = data.summary
          this.updateCharts(data)
        } catch (error) {
          console.error('Error fetching analytics:', error)
        }
      },
  
      initializeCharts() {
        this.statusChart = new Chart(this.$refs.statusChart, {
          type: 'doughnut',
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        })
  
        this.servicesChart = new Chart(this.$refs.servicesChart, {
          type: 'bar',
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: false
              }
            }
          }
        })
      },
  
      updateCharts(data) {
        // Update Status Chart
        this.statusChart.data = {
          labels: Object.keys(data.request_status),
          datasets: [{
            data: Object.values(data.request_status),
            backgroundColor: [
              '#FF6384',
              '#36A2EB',
              '#FFCE56',
              '#4BC0C0',
              '#9966FF'
            ]
          }]
        }
        this.statusChart.update()
  
        // Update Services Chart
        this.servicesChart.data = {
          labels: Object.keys(data.top_services),
          datasets: [{
            data: Object.values(data.top_services),
            backgroundColor: '#36A2EB'
          }]
        }
        this.servicesChart.update()
      },
  
      formatTitle(key) {
        return key.split('_').map(word => 
          word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ')
      }
    }
  }
  </script>