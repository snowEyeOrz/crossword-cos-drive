// src/services/puzzleService.js
import staticLevel from '../data/level_mvp.json';

// 模拟异步获取数据，为未来联网做准备
export async function fetchNewGame() {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log("Loading data...", staticLevel);
      resolve(staticLevel);
    }, 300); // 模拟300ms延迟
  });
}
