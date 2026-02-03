<template>
  <div class="game-wrapper">
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
        
        <span v-if="getWordLabel(index - 1)" class="word-label">
          {{ getWordLabel(index - 1) }}
        </span>
      </div>
    </div>

    <div class="clue-panel" v-if="wordData.length > 0">
      <div class="clue-column">
        <h3>➡️ 横向 (Across)</h3>
        <ul>
          <li v-for="word in acrossWords" :key="word.id">
            <span class="clue-id">{{ word.id_label }}</span>
            <span class="clue-text">
              {{ word.clue_cn }} 
              <small class="jp-hint">({{ word.clue_jp_hint }})</small>
            </span>
          </li>
        </ul>
      </div>
      <div class="clue-column">
        <h3>⬇️ 纵向 (Down)</h3>
        <ul>
          <li v-for="word in downWords" :key="word.id">
            <span class="clue-id">{{ word.id_label }}</span>
            <span class="clue-text">
              {{ word.clue_cn }}
              <small class="jp-hint">({{ word.clue_jp_hint }})</small>
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { fetchNewGame } from '../services/puzzleService';

const emit = defineEmits(['progress-update', 'game-loaded']);

const gridSize = ref(8);
const wordData = ref([]);
const userInputs = reactive({});
const answerMap = reactive({});
const labelMap = reactive({}); // 存储格子的视觉序号 (1, 2, 3...)

// 过滤计算属性：确保 word 对象里有了 id_label 才能正确显示在列表中
const acrossWords = computed(() => wordData.value.filter(w => w.orientation === 'across'));
const downWords = computed(() => wordData.value.filter(w => w.orientation === 'down'));

const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${gridSize.value}, 1fr)`,
  gap: '4px',
  width: '100%',
  maxWidth: '400px',
  aspectRatio: '1 / 1',
  margin: '0 auto'
}));

const totalCells = computed(() => gridSize.value * gridSize.value);

onMounted(async () => {
  const data = await fetchNewGame();
  
  gridSize.value = data.meta.grid_dimension;
  wordData.value = data.matrix;
  
  parseMatrixToMap(data.matrix);
  emit('game-loaded', data.reward);
});

function parseMatrixToMap(matrix) {
  // 1. 清空旧数据
  Object.keys(answerMap).forEach(k => delete answerMap[k]);
  Object.keys(labelMap).forEach(k => delete labelMap[k]);

  // 2. 第一遍遍历：填充答案 (Model)
  matrix.forEach(word => {
    const chars = word.answer.split('');
    chars.forEach((char, i) => {
      let x = word.start_x;
      let y = word.start_y;
      if (word.orientation === 'across') x += i;
      else y += i;
      const flatIndex = y * gridSize.value + x;
      answerMap[flatIndex] = char;
    });
  });

  // 3. 第二遍遍历：生成序号 (Label Logic)
  // 规则：按格子顺序扫描，如果发现是某个单词的起点，且该格子还没序号，就分配新序号
  let currentLabelId = 1;
  
  // 为了保证序号顺序符合阅读习惯（从左到右，从上到下），我们先对单词按位置排序
  const sortedWords = [...matrix].sort((a, b) => {
    const posA = a.start_y * gridSize.value + a.start_x;
    const posB = b.start_y * gridSize.value + b.start_x;
    return posA - posB;
  });

  sortedWords.forEach(word => {
    const startFlatIndex = word.start_y * gridSize.value + word.start_x;
    
    // 如果这个起始格还没有贴过数字标签
    if (!labelMap[startFlatIndex]) {
      labelMap[startFlatIndex] = currentLabelId; // 在格子上贴数字
      currentLabelId++;
    }
    
    // 关键修复：让单词记住它属于哪个数字标签 (比如 1 Across, 1 Down)
    word.id_label = labelMap[startFlatIndex];
  });
}

function getCellInfo(index) { return answerMap.hasOwnProperty(index); }
function isCorrect(index) { return userInputs[index] === answerMap[index]; }
function getWordLabel(index) { return labelMap[index]; }

function handleInput() {
  const totalChars = Object.keys(answerMap).length;
  let correctCount = 0;
  for (const index in answerMap) {
    if (userInputs[index] === answerMap[index]) correctCount++;
  }
  const progress = totalChars === 0 ? 0 : Math.floor((correctCount / totalChars) * 100);
  emit('progress-update', progress);
}
</script>

<style scoped>
.game-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 800px;
  gap: 20px;
}

/* 棋盘样式 */
.game-board {
  background: rgba(0, 0, 0, 0.3);
  padding: 10px;
  border-radius: 8px;
}

.cell-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.cell-input {
  width: 100%;
  height: 100%;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  text-align: center;
  font-size: 1.2rem;
  border-radius: 4px;
  padding: 0; /* 修复某些浏览器 padding 导致输入框偏倚 */
}

.cell-input:focus {
  background: rgba(255, 255, 255, 0.2);
  outline: 2px solid #ff4081;
}

.cell-input.correct {
  background: rgba(76, 175, 80, 0.9);
  border-color: #4caf50;
}

/* 序号小标 (Superscript) */
.word-label {
  position: absolute;
  top: 1px;
  left: 2px;
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.7);
  pointer-events: none;
}

/* 提示面板样式 */
.clue-panel {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  width: 100%;
  background: rgba(0, 0, 0, 0.6); /* 半透明黑底，保证文字清晰 */
  border-radius: 10px;
  padding: 15px;
  box-sizing: border-box;
  backdrop-filter: blur(10px); /* 局部毛玻璃，增加高级感 */
}

.clue-column {
  flex: 1;
  min-width: 250px;
  padding: 0 10px;
}

h3 {
  color: #ff4081;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 5px;
  margin-top: 0;
  font-size: 1rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #eee;
  display: flex;
  align-items: baseline;
}

.clue-id {
  font-weight: bold;
  color: #4ecca3;
  margin-right: 8px;
  min-width: 15px;
}

.jp-hint {
  color: #aaa;
  margin-left: 5px;
}
</style>
