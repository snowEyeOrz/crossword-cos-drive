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
/* 全局样式 */
/* 确保 html 和 body 占满屏幕，且禁止滚动 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 禁止整个页面滚动，防止背景图乱跑 */
}

.app-container {
  width: 100%;
  height: 100%;
  position: relative;
  background-color: #222;
  
  /* 解决移动端软键盘弹出时顶起页面的问题 */
  display: flex;
  flex-direction: column;
}

/* 允许内容区域内部滚动 */
.content-layer {
  flex: 1;
  width: 100%;
  overflow-y: auto; /* 只有中间的内容区可以滚动 */
  overflow-x: hidden;
  padding-top: 20px;
  padding-bottom: 50px; /* 底部留白，防止被手机Home条遮挡 */
  
  /* 弹性布局居中 */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* justify-content: center;  <-- 删掉这行，手机竖屏时不需要垂直居中，从顶开始排 */
}
/* 恢复交互 */
.content-layer > * { pointer-events: auto; }

h1 { color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); margin-bottom: 5px; }
.subtitle { color: #aaa; margin-top: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
</style>

