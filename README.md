```markdown
# 🚗 Automotive Crossword Puzzle (Crossword-Cos-Drive)

![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

> 一个基于 Vue 3 + Vite 的自动化生成式填字游戏，融合了汽车工程专业术语与二次元奖励系统。
> A procedural generation crossword game built with Vue 3, featuring automotive engineering terminology and a Gacha reward system.

## 🌟 项目亮点 (Highlights)

* **♾️ 无限关卡 (Infinite Levels)**: 采用边缘计算架构，浏览器端实时运行“随机贪心构造法 (Randomized Greedy Construction)”，每次刷新自动生成全新的棋盘结构。
* **📱 全端适配 (Responsive Design)**: 完美适配桌面端与移动端，自动处理分辨率适配与交互逻辑。
* **🎁 抽卡奖励 (Gacha System)**: 通关后触发随机奖励系统，解锁精美的背景插画（支持本地配置与网络图源）。
* **🚀 自动化部署 (CI/CD)**: 集成 GitHub Actions，代码推送即自动构建并发布至 GitHub Pages。

---

## 🏗️ 系统架构 (System Architecture)

本项目遵循**系统工程 (Systems Engineering)** 方法论进行开发。

### 1. 人机料法环测 (5M1E) 模型

| 维度 | 定义 | 实现方案 |
| :--- | :--- | :--- |
| **料 (Material)** | 原始数据 | `src/data/wordBank.js` (汽车术语库), `reward_pool.json` (奖励池) |
| **法 (Method)** | 核心算法 | `src/utils/CrosswordGenerator.js` (基于 JS 的回溯生成算法) |
| **机 (Machine)** | 运行环境 | 浏览器客户端实时计算 (Client-side Generation) |
| **环 (Environment)** | 适配环境 | 响应式 CSS 布局 (`min()`, `clamp()`), 解决刘海屏与移动端滚动问题 |
| **测 (Measurement)** | 验证机制 | 算法内置碰撞检测与孤岛剔除逻辑 |
| **人 (Man)** | 用户体验 | 暗黑科幻风格 UI，高对比度交互设计 |

### 2. 目录结构 (Directory Structure)

```text
├── .github/workflows/   # CI/CD 自动化部署脚本
├── public/              # 静态资源 (图片)
├── src/
│   ├── components/      # Vue 组件 (GameBoard, RewardLayer)
│   ├── data/            # 数据源 (词库 wordBank, 奖励池 reward_pool)
│   ├── services/        # 业务逻辑 (puzzleService)
│   ├── utils/           # 核心算法 (CrosswordGenerator)
│   ├── App.vue          # 根组件 (布局控制)
│   └── main.js          # 入口文件
└── tools/               # 离线工具 (Python 原型验证脚本)

```

---

## 🛠️ 快速开始 (Getting Started)

### 环境要求

* Node.js 16.0+

### 安装与运行

1. **克隆项目**
```bash
git clone [https://github.com/snowEyeOrz/crossword-cos-drive.git](https://github.com/snowEyeOrz/crossword-cos-drive.git)
cd crossword-cos-drive

```


2. **安装依赖**
```bash
npm install

```


3. **本地开发**
```bash
npm run dev

```


打开浏览器访问 `http://localhost:5173`。
4. **构建生产版本**
```bash
npm run build

```



---

## ⚙️ 配置指南 (Configuration)

### 1. 添加新单词 (Material - Words)

修改 `src/data/wordBank.js`，按照以下格式添加汽车术语：

```javascript
{ 
  answer: "ターボ", 
  clue: "【动力】利用废气增加进气量的装置 (Turbo)", 
  hint: "タ__" 
}

```

### 2. 配置奖励池 (Material - Rewards)

修改 `src/data/reward_pool.json`，支持本地图片或网络图片：

```json
{
  "id": 101,
  "url": "images/my_fav_coser.jpg", 
  "credit": "Twitter: @ArtistName",
  "desc": "稀有奖励：赛博朋克风格"
}

```

*注意：本地图片请存放在 `public/images/` 目录下，路径**不要**以 `/` 开头。*

---

## 🤝 贡献指南 (Contributing)

本项目引入了**变更影响分析 (Impact Analysis)** 流程。提交 Pull Request 前，请考虑以下因素：

1. **Architecture**: 变更是否影响核心生成算法？
2. **Environment**: 变更是否破坏移动端/桌面端的显示一致性？
3. **Risk**: 是否引入了新的 CSS 全局污染？

---

## 📄 License

MIT License


