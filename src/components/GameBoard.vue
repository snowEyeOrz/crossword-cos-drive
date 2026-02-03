<template>
  <div class="game-board" :style="gridStyle">
    <div 
      v-for="index in totalCells" 
      :key="index"
      class="cell-wrapper"
    >
      <input 
        v-if="getCellInfo(index - 1)"
        type="text"
        maxlength="1"
        class="cell-input"
        :class="{ 'correct': isCorrect(index - 1) }"
        v-model="userInputs[index - 1]"
        @input="handleInput(index - 1)"
      />
      <div v-else class="cell-empty"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { fetchNewGame } from '../services/puzzleService'; // 引入我们之前定义的 Service

const emit = defineEmits(['progress-update', 'game-loaded']);

const gridSize = ref(8); // 默认值，会被 API 覆盖
const wordData = ref([]);
const userInputs = reactive({}); // 存储用户的输入 { index: 'エ' }
const answerMap = reactive({});  // 存储正确答案 { index: 'エ' }

// 计算 CSS Grid 布局样式
const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${gridSize.value}, 1fr)`,
  gap: '5px',
  width: '100%',
  maxWidth: '500px', // 限制最大宽度
  aspectRatio: '1 / 1'
}));

const totalCells = computed(() => gridSize.value * gridSize.value);

// 初始化：调用 Service 获取数据
onMounted(async () => {
  const data = await fetchNewGame(); // 模拟网络请求
  
  // 1. 设置棋盘元数据
  gridSize.value = data.meta.grid_dimension;
  wordData.value = data.matrix;
  
  // 2. 将 JSON 里的单词解析映射到 flat index (扁平索引)
  parseMatrixToMap(data.matrix);
  
  // 3. 通知父组件加载奖励图片
  emit('game-loaded', data.reward);
});

// 辅助函数：将 JSON 坐标转换为一维数组索引
function parseMatrixToMap(matrix) {
  matrix.forEach(word => {
    const chars = word.answer.split('');
    chars.forEach((char, i) => {
      let x = word.start_x;
      let y = word.start_y;
      
      if (word.orientation === 'across') x += i;
      else y += i;
      
      const flatIndex = y * gridSize.value + x;
      answerMap[flatIndex] = char; // 记录这个格子应该填什么
    });
  });
}

// 检查某个位置是否是填字格
function getCellInfo(index) {
  return answerMap.hasOwnProperty(index);
}

// 检查单个格子是否填对
function isCorrect(index) {
  return userInputs[index] === answerMap[index];
}

// 处理输入：计算总进度
function handleInput() {
  const totalChars = Object.keys(answerMap).length;
  let correctCount = 0;
  
  for (const index in answerMap) {
    if (userInputs[index] === answerMap[index]) {
      correctCount++;
    }
  }
  
  const progress = Math.floor((correctCount / totalChars) * 100);
  emit('progress-update', progress);
}
</script>

<style scoped>
.game-board {
  position: relative;
  z-index: 10; /* 保证在遮罩之上 */
  padding: 20px;
}

.cell-input {
  width: 100%;
  height: 100%;
  border: 1px solid rgba(255, 255, 255, 0.4);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  text-align: center;
  font-size: 1.2rem;
  border-radius: 4px;
}

.cell-input:focus {
  background: rgba(255, 255, 255, 0.2);
  outline: 2px solid #ff4081;
}

.cell-input.correct {
  background: rgba(76, 175, 80, 0.8); /* 绿色背景 */
  border-color: #4caf50;
  color: white;
}
</style>
