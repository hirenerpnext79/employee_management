<template>
  <div class="error-state">
    <div class="error-card">
      <h2>Page Not Found</h2>
      <p>Please create this page and link it on the menu.</p>
    </div>
  </div>
</template>

<style scoped>
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  padding: 2rem;
}

.error-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 4rem 5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.error-card h2 {
  color: #0f172a;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
}

.error-card p {
  color: #64748b;
  font-size: 1.05rem;
  margin: 0;
}
</style>
