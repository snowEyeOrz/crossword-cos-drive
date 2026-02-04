import staticLevel from '../data/level_mvp.json';
import rewardPool from '../data/reward_pool.json'; 
// 1. 引入奖池

// 辅助函数：获取随机整数
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

export async function fetchNewGame() {
  return new Promise(resolve => {
    setTimeout(() => {
      // 深拷贝一份关卡数据，避免修改原对象
      const gameData = JSON.parse(JSON.stringify(staticLevel));
      
      // 2. 核心逻辑：随机抽卡
      // 从奖池里随机选一个索引
      const randomIndex = getRandomInt(rewardPool.length);
      const selectedReward = rewardPool[randomIndex];
      
      // 3. 偷梁换柱：把关卡原本的固定奖励替换成抽到的奖励
      gameData.reward = {
        ...gameData.reward, // 保留 blur_strength 等通用配置
        url: selectedReward.url,
        unlock_text: selectedReward.credit, // 用 credit 替换原本的 unlock_text
        description: selectedReward.desc
      };

      console.log("本次抽中奖励:", selectedReward.desc);
      resolve(gameData);
    }, 300);
  });
}

