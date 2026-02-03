<template>
  <div class="app-container">
    <RewardLayer 
      :imageUrl="rewardInfo.url"
      :credit="rewardInfo.unlock_text"
      :progress="currentProgress"
    />

    <div class="content-layer">
      <h1>Crossword-Cos-Drive</h1>
      <p class="subtitle">汽车日语补完计划</p>
      
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
/* 全局样式 */
html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
.app-container {
  width: 100vw;
  height: 100vh;
  position: relative;
  background-color: #222;
  font-family: 'Segoe UI', sans-serif;
}
.content-layer {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  pointer-events: none; /* 让鼠标穿透背景 */
}
/* 恢复交互 */
.content-layer > * { pointer-events: auto; }

h1 { color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); margin-bottom: 5px; }
.subtitle { color: #aaa; margin-top: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
</style>

