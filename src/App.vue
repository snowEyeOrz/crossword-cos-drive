<template>
  <div class="app-container">
    <RewardLayer 
      :imageUrl="rewardInfo.url"
      :credit="rewardInfo.unlock_text"
      :progress="currentProgress"
    />

    <div class="content-layer">
      <h1>DIY填字游戏</h1>
      <p class="subtitle">coser卡片收集Project</p>
      
      <GameBoard 
        @game-loaded="handleGameLoaded"
        @progress-update="handleProgress"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import RewardLayer from './components/RewardLayer.vue';
import GameBoard from './components/GameBoard.vue';

const currentProgress = ref(0);
const rewardInfo = ref({ url: '', unlock_text: '' });

// 接收 GameBoard 传来的数据
const handleGameLoaded = (rewardData) => {
  rewardInfo.value = rewardData;
};

// 接收实时进度更新
const handleProgress = (progress) => {
  currentProgress.value = progress;
};
</script>

<style>
/* 1. 全局重置：锁死最外层，防止整个页面在手机上乱动 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 关键：禁止 body 滚动 */
  background-color: #222; /* 防止加载时白屏 */
}

.app-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden; /* 双重保险 */
  font-family: 'Segoe UI', sans-serif;
}

/* 2. 视觉层：必须在最底层 */
/* 注意：RewardLayer 组件内部通常是 absolute，这里不需要额外样式，但确保它没有 z-index 或者很低 */

/* 3. 内容交互层：核心修改 */
.content-layer {
  position: absolute; /* 绝对定位，铺满屏幕 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10; /* 保证在背景图之上 */
  
  /* 滚动逻辑的核心 */
  overflow-y: auto; /* 允许垂直滚动 */
  -webkit-overflow-scrolling: touch; /* iOS 丝滑滚动支持 */
  
  /* 布局逻辑 */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* ⚠️ 移除 justify-content: center; 这会导致长内容在手机上无法滚动到顶部 */
  
  padding-top: 40px; /* 顶部留出空间 */
  padding-bottom: 80px; /* 底部留出空间，防止被手机 Home 条遮挡 */
  box-sizing: border-box; /* 确保 padding 算在 height 内 */
}

/* 标题样式适配 */
h1 { 
  color: white; 
  text-shadow: 0 2px 4px rgba(0,0,0,0.8); 
  margin: 0 0 5px 0; 
  font-size: clamp(1.5rem, 5vw, 2.5rem); /* 标题字号也随屏幕缩放 */
  text-align: center;
}

.subtitle { 
  color: #aaa; 
  margin: 0 0 20px 0; 
  text-shadow: 0 1px 2px rgba(0,0,0,0.8); 
  font-size: clamp(0.8rem, 3vw, 1rem);
  text-align: center;
}
</style>


