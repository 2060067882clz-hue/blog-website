<template>
  <section class="profile-shell">
    <button class="profile-button" @click="goToProfile">个人中心</button>
  </section>
</template>

<script>
export default {
  methods: {
    goToProfile() {
      this.$router.push('/center')
    }
  }
}
</script>

<style scoped>
.profile-shell {
  position: relative;
}

.profile-button {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #5B9FD8;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
