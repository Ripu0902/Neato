<template>
  <section class="about-us-section py-5">
    <div class="container">
      <!-- Main Content -->
      <div class="row align-items-center">
        <!-- Left Side: Image -->
        <div class="col-lg-6 mb-4 mb-lg-0">
          <div class="about-image-wrapper">
            <img src="../assets/office.jpg" alt="About Us"
              class="img-fluid rounded shadow">
            <div class="experience-badge">
              <span class="number">5+</span>
              <span class="text">Years Experience</span>
            </div>
          </div>
        </div>

        <!-- Right Side: Content -->
        <div class="col-lg-6">
          <div class="about-content">
            <h6 class="text-primary fw-bold text-uppercase mb-2">About Us</h6>
            <h2 class="mb-4">Your Trusted Partner for Professional Home Services</h2>
            <p class="lead mb-4">
              At NEATO, we bring together skilled professionals and homeowners, creating perfect matches for all your
              home service needs.
            </p>

            <!-- Key Points -->
            <div class="key-points mb-4">
              <div class="point">
                <i class="bi bi-check-circle-fill text-success"></i>
                <span>Verified Professionals</span>
              </div>
              <div class="point">
                <i class="bi bi-check-circle-fill text-success"></i>
                <span>Quality Guaranteed Services</span>
              </div>
              <div class="point">
                <i class="bi bi-check-circle-fill text-success"></i>
                <span>24/7 Customer Support</span>
              </div>
            </div>

            <!-- Stats -->
            <div class="row stats g-4 mb-4">
              <div class="col-6 col-md-3">
                <div class="stat-item">
                  <h3 class="stat-number">500+</h3>
                  <p class="stat-label">Professionals</p>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="stat-item">
                  <h3 class="stat-number">1000+</h3>
                  <p class="stat-label">Customers</p>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="stat-item">
                  <h3 class="stat-number">50+</h3>
                  <p class="stat-label">Services</p>
                </div>
              </div>
              <div class="col-6 col-md-3">
                <div class="stat-item">
                  <h3 class="stat-number">4.8</h3>
                  <p class="stat-label">Rating</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-us-section {
  background-color: #f8f9fa;
  margin-top: 100px;
}

.about-image-wrapper {
  position: relative;
  padding: 20px;
}

.experience-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #198754;
  color: white;
  padding: 20px;
  border-radius: 10px;
  transform: translate(25%, 25%);
}

.experience-badge .number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.experience-badge .text {
  font-size: 0.9rem;
}

.key-points {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.point {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}

.point i {
  font-size: 1.2rem;
}

.stats {
  border-top: 1px solid #dee2e6;
  padding-top: 2rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #198754;
  margin-bottom: 0;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .experience-badge {
    transform: translate(0, 50%);
  }
}
</style>

<script>
export default {
  name: 'AboutUs'
}
</script>