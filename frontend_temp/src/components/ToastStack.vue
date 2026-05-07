<script setup>
import { toasts, dismissToast } from '../lib/notify'
</script>

<template>
  <div class="toast-stack" aria-live="polite">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="`toast--${toast.tone}`"
      >
        <span>{{ toast.message }}</span>
        <button type="button" @click="dismissToast(toast.id)">关闭</button>
      </div>
    </TransitionGroup>
  </div>
</template>
