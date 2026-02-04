// src/services/puzzleService.js

// 1. 引入 原材料 和 引擎
import { RAW_WORDS } from '../data/wordBank';
import { CrosswordGenerator } from '../utils/CrosswordGenerator';

import rewardPool from '../data/reward_pool.json'; 

// 辅助函数：获取随机整数
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

export async function fetchNewGame() {
  return new Promise(resolve => {
    // 模拟一点点加载延迟，让用户感觉"正在生成"
    setTimeout(() => {
      console.log("正在启动浏览器端生成引擎...");
      const startTime = Date.now();

      // 2. 实例化引擎并执行生成
      // 这里可以动态传入 grid 大小，目前默认 15
      const generator = new CrosswordGenerator(15);
      const generatedMatrix = generator.generate(RAW_WORDS);

      const endTime = Date.now();
      console.log(`生成完毕！耗时 ${endTime - startTime}ms, 生成单词数: ${generatedMatrix.length}`);

      // 3. 组装成前端需要的数据格式
      const gameData = {
        meta: {
            version: "3.0 (Client-Side Realtime)",
            grid_dimension: 15
        },
        // 这里先给个默认奖励，马上就会被下面的逻辑替换
        reward: {
            id: "gen_reward",
            url: "",
            desc: "Loading..."
        },
        matrix: generatedMatrix
      };

      // 4. 随机抽卡逻辑 (保持不变)
      if (rewardPool && rewardPool.length > 0) {
        const randomIndex = getRandomInt(rewardPool.length);
        const selectedReward = rewardPool[randomIndex];
        
        gameData.reward = {
          ...gameData.reward, 
          url: selectedReward.url,
          unlock_text: selectedReward.credit,
          description: selectedReward.desc
        };
      }

      resolve(gameData);
    }, 500); // 延迟 500ms，给一点仪式感
  });
}


