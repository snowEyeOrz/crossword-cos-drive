<template>
  <div class="reward-container">
    <div 
      class="bg-image" 
      :style="{ backgroundImage: `url(${resolvedImageUrl})` }"
    ></div>

    <div class="blur-mask" :style="maskStyle">
      <div v-if="isUnlocked" class="success-banner">
        <div class="main-text">🎉 恭喜通关！</div>
        <div class="sub-text">{{ credit }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 1. 关键：必须引入 computed
import { computed } from 'vue';

const props = defineProps({
  imageUrl: String,
  credit: String,
  progress: Number 
});

const isUnlocked = computed(() => props.progress >= 100);

// 2. 关键：这就是报错说找不到的变量
// 它的作用是智能处理路径（本地路径 vs 网络路径）
const resolvedImageUrl = computed(() => {
  if (!props.imageUrl) return ''; // 防止空值

  // 如果是网络图片（http开头），直接用
  if (props.imageUrl.startsWith('http')) return props.imageUrl;
  
  // 如果是本地图片，清理掉开头的斜杠（如果有的话）
  const cleanPath = props.imageUrl.startsWith('/') ? props.imageUrl.slice(1) : props.imageUrl;
  
  // 拼接 Vite 的基础路径 (确保 GitHub Pages 也能正常显示)
  return import.meta.env.BASE_URL + cleanPath;
});

const maskStyle = computed(() => {
  // 模糊逻辑：进度 0% -> 40px, 进度 100% -> 0px
  const blurPx = 40 - (props.progress * 0.4);
  return {
    backdropFilter: `blur(${blurPx}px)`,
    webkitBackdropFilter: `blur(${blurPx}px)`,
    backgroundColor: `rgba(26, 26, 46, ${0.6 - props.progress * 0.006})`
  };
});
</script>

<style scoped>
.reward-container {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  overflow: hidden;
}

.bg-image {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  
  /* 之前的 CSS 修复：确保图片居中且铺满 */
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  
  z-index: 0;
}

.blur-mask {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  z-index: 1;
  transition: backdrop-filter 0.5s ease, background-color 0.5s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}

.success-banner {
  background: rgba(255, 64, 129, 0.95);
  color: white;
  padding: 20px 40px;
  border-radius: 50px;
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  
  /* 文字居中排版 */
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.main-text { font-size: 1.5rem; font-weight: bold; }
.sub-text { font-size: 1rem; font-weight: normal; opacity: 0.9; }

@keyframes popIn {
  from { transform: scale(0.5); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>

