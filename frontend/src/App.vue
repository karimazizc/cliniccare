<template>
  <div class="app">
    <!-- Top Navigation Bar -->
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <!-- Brand -->
          <router-link to="/" class="brand" aria-label="ClinicCare EMR Home">
            <div class="brand-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 2a2 2 0 0 0-2 2v5H4a2 2 0 0 0-2 2v2c0 1.1.9 2 2 2h5v5c0 1.1.9 2 2 2h2a2 2 0 0 0 2-2v-5h5a2 2 0 0 0 2-2v-2a2 2 0 0 0-2-2h-5V4a2 2 0 0 0-2-2h-2z"/>
              </svg>
            </div>
            <div class="brand-text">
              <span class="brand-name">ClinicCare</span>
              <span class="brand-label">Mini EMR</span>
            </div>
          </router-link>

          <!-- Navigation -->
          <nav class="nav" role="navigation" aria-label="Main navigation">
            <router-link to="/" class="nav-link" :class="{ active: $route.name === 'consultations' }">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
              </svg>
              Consultations
            </router-link>
            <router-link to="/new" class="nav-link nav-link-cta">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              New Consultation
            </router-link>
          </nav>

          <!-- Doctor Profile -->
          <div class="header-end">
            <div class="doctor-profile">
              <div class="doctor-avatar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="doctor-info">
                <span class="doctor-name">Dr. Karim</span>
                <span class="doctor-role">Practitioner</span>
              </div>
            </div>
          </div>

          <!-- Mobile Menu Toggle -->
          <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle menu">
            <svg v-if="!mobileMenuOpen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Mobile Navigation -->
        <div v-if="mobileMenuOpen" class="mobile-nav">
          <router-link to="/" class="mobile-nav-link" @click="mobileMenuOpen = false">
            Consultations
          </router-link>
          <router-link to="/new" class="mobile-nav-link" @click="mobileMenuOpen = false">
            New Consultation
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <div class="container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="container">
        <div class="footer-content">
          <p class="footer-text">&copy; {{ currentYear }} ClinicCare Mini EMR &middot; Electronic Medical Records</p>
          <p class="footer-version">v1.0.0</p>
        </div>
      </div>
    </footer>

    <!-- Toast Notifications -->
    <teleport to="body">
      <transition-group name="slide-fade" tag="div" class="toast-container">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast"
          :class="`toast-${toast.type}`"
        >
          <!-- Success Icon -->
          <svg v-if="toast.type === 'success'" class="toast-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#14966c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <!-- Error Icon -->
          <svg v-else class="toast-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#d64545" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          <span>{{ toast.message }}</span>
        </div>
      </transition-group>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, provide, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentYear = computed(() => new Date().getFullYear())
const mobileMenuOpen = ref(false)

// Toast notification system
const toasts = ref([])
let toastCounter = 0

const showToast = (message, type = 'success', duration = 3500) => {
  const id = ++toastCounter
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, duration)
}

// Provide toast function to child components
provide('showToast', showToast)

// Close mobile menu on route change
onMounted(() => {
  // Handled by click handler on links
})
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* --- Header --- */
.app-header {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
}

.header-content {
  display: flex;
  align-items: center;
  height: 60px;
  gap: 2rem;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex-shrink: 0;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-color) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-icon svg {
  width: 18px;
  height: 18px;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.brand-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.brand-label {
  font-size: 0.625rem;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Navigation */
.nav {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: auto;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  border: 1.5px solid transparent;
}

.nav-link svg {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.nav-link:hover {
  color: var(--text-primary);
  background-color: var(--gray-50);
}

.nav-link.active {
  color: var(--primary-color);
  background-color: var(--primary-50);
}

.nav-link-cta {
  background-color: var(--primary-color);
  color: white !important;
  border-color: var(--primary-color);
}

.nav-link-cta:hover {
  background-color: var(--primary-hover) !important;
  border-color: var(--primary-hover);
  box-shadow: 0 1px 3px rgba(26, 111, 196, 0.25);
}

/* Doctor Profile */
.header-end {
  margin-left: 1.5rem;
  flex-shrink: 0;
}

.doctor-profile {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 6px 10px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  background-color: var(--gray-25);
}

.doctor-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--primary-100);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-600);
}

.doctor-avatar svg {
  width: 16px;
  height: 16px;
}

.doctor-info {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.doctor-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.doctor-role {
  font-size: 0.625rem;
  color: var(--text-muted);
}

/* Mobile */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
  color: var(--text-secondary);
  margin-left: auto;
}

.mobile-menu-btn svg {
  width: 22px;
  height: 22px;
}

.mobile-nav {
  display: none;
  flex-direction: column;
  gap: 2px;
  padding-bottom: 12px;
}

.mobile-nav-link {
  display: block;
  padding: 10px 14px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.mobile-nav-link:hover {
  background-color: var(--gray-50);
  color: var(--text-primary);
}

/* --- Main --- */
.app-main {
  flex: 1;
  padding: 2rem 0;
}

/* --- Footer --- */
.app-footer {
  border-top: 1px solid var(--border-light);
  padding: 1.25rem 0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.footer-version {
  font-size: 0.6875rem;
  color: var(--text-muted);
  font-family: 'SF Mono', 'Fira Code', Menlo, Consolas, monospace;
}

/* --- Responsive --- */
@media (max-width: 768px) {
  .header-content {
    height: 56px;
    gap: 0;
  }

  .nav,
  .header-end {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-nav {
    display: flex;
  }

  .app-main {
    padding: 1.5rem 0;
  }

  .footer-content {
    flex-direction: column;
    gap: 4px;
    text-align: center;
  }
}
</style>