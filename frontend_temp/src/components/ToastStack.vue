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

<style scoped>
.toast-stack {
  position: fixed;
  right: 18px;
  top: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 9999;
  pointer-events: none;
}

.toast {
  background: #222;
  color: #fff;
  padding: 10px 14px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.18);
  pointer-events: auto;
}

.toast--success {
  /* center success toasts on screen */
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: #8B5E3C; /* 温暖的褐色 */
  color: #fff;
  min-width: 220px;
  justify-content: center;
}

.toast--danger { background: #b91c1c; }
.toast--warning { background: #b45f03; }
.toast--info { background: #0f172a; }

.toast button {
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.8);
  cursor: pointer;
  font-size: 12px;
}

/* TransitionGroup simple animation */
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-6px); }
.toast-enter-active, .toast-leave-active { transition: all 220ms ease; }
</style>
