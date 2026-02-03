<template>
  <div class="reward-container">
    <div 
      class="bg-image" 
      :style="{ backgroundImage: `url(${imageUrl})` }"
    ></div>

    <div 
      class="blur-mask"
      :style="maskStyle"
    >
      <div v-if="isUnlocked" class="success-banner">
        🎉 恭喜通关！Coser: {{ credit }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  imageUrl: String,
  credit: String,
  progress: Number // 0 到 100
});

const isUnlocked = computed(() => props.progress >= 100);

// 核心视觉逻辑：进度越高，模糊度越低 (40px -> 0px)
const maskStyle = computed(() => {
  const blurPx = 40 - (props.progress * 0.4);
  return {
    backdropFilter: `blur(${blurPx}px)`,
    webkitBackdropFilter: `blur(${blurPx}px)`, // 兼容 Safari
    backgroundColor: `rgba(26, 26, 46, ${0.6 - props.progress * 0.006})` // 变亮
  };
});
</script>

<style scoped>
.reward-container, .bg-image, .blur-mask {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
}
.bg-image {
  background-size: cover;
  background-position: center;
  z-index: 0;
}
.blur-mask {
  z-index: 1;
  transition: backdrop-filter 0.5s ease, background-color 0.5s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}
.success-banner {
  background: rgba(255, 64, 129, 0.9);
  color: white;
  padding: 20px 40px;
  border-radius: 50px;
  font-size: 1.5rem;
  font-weight: bold;
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes popIn {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
