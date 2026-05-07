<script setup>
import { RouterView } from 'vue-router'

import SiteShell from './components/SiteShell.vue'
import ToastStack from './components/ToastStack.vue'
</script>

<template>
  <SiteShell>
    <RouterView />
    <ToastStack />
  </SiteShell>
</template>
