// src/utils/CrosswordGenerator.js

export class CrosswordGenerator {
  constructor(size = 15) {
    this.size = size;
    // JS 初始化二维数组的写法
    this.grid = Array.from({ length: size }, () => Array(size).fill(''));
    this.placedWords = [];
  }

  // 辅助函数：检查是否能放置
  canPlace(word, r, c, direction) {
    const length = word.length;

    // A. 边界检查
    if (direction === 'across') {
      if (c + length > this.size) return false;
      if (c - 1 >= 0 && this.grid[r][c - 1] !== '') return false;
      if (c + length < this.size && this.grid[r][c + length] !== '') return false;
    } else { // down
      if (r + length > this.size) return false;
      if (r - 1 >= 0 && this.grid[r - 1][c] !== '') return false;
      if (r + length < this.size && this.grid[r + length][c] !== '') return false;
    }

    // B. 逐格检查
    for (let i = 0; i < length; i++) {
      const currR = r + (direction === 'across' ? 0 : i);
      const currC = c + (direction === 'across' ? i : 0);
      
      const cellChar = this.grid[currR][currC];

      // 冲突检查：格子非空且字符不匹配
      if (cellChar !== '' && cellChar !== word[i]) return false;

      // 粘连检查：格子为空时，检查两侧
      if (cellChar === '') {
        if (direction === 'across') {
          if (currR - 1 >= 0 && this.grid[currR - 1][currC] !== '' && this.grid[currR - 1][currC] !== word[i]) return false;
          if (currR + 1 < this.size && this.grid[currR + 1][currC] !== '') return false;
        } else {
          if (currC - 1 >= 0 && this.grid[currR][currC - 1] !== '') return false;
          if (currC + 1 < this.size && this.grid[currR][currC + 1] !== '') return false;
        }
      }
    }
    return true;
  }

  // 放置单词
  place(wordObj, r, c, direction) {
    const word = wordObj.answer;
    for (let i = 0; i < word.length; i++) {
      const currR = r + (direction === 'across' ? 0 : i);
      const currC = c + (direction === 'across' ? i : 0);
      this.grid[currR][currC] = word[i];
    }

    this.placedWords.push({
      id: `gen_${this.placedWords.length + 1}`,
      answer: word,
      clue_cn: wordObj.clue,
      clue_jp_hint: wordObj.hint,
      // ⚠️ 关键：坐标+1 适配 CSS Grid
      start_x: c + 1,
      start_y: r + 1,
      orientation: direction,
      length: word.length
    });
  }

  // 核心生成方法
  generate(wordsInput) {
    // 深拷贝输入数组
    const words = JSON.parse(JSON.stringify(wordsInput));

    // 1. 龙骨策略：按长度排序，取最长
    words.sort((a, b) => b.answer.length - a.answer.length);
    if (words.length === 0) return [];

    const firstWord = words.shift();
    const startR = Math.floor(this.size / 2);
    const startC = Math.floor((this.size - firstWord.answer.length) / 2);
    
    this.place(firstWord, startR, startC, 'across');

    // 2. 随机策略：Fisher-Yates 洗牌算法打乱剩余单词
    for (let i = words.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [words[i], words[j]] = [words[j], words[i]];
    }

    let maxAttempts = 200;
    while (maxAttempts > 0 && words.length > 0) {
      maxAttempts--;
      
      // 倒序遍历
      for (let i = words.length - 1; i >= 0; i--) {
        const candidate = words[i];
        let placed = false;

        // 生成随机的行列遍历顺序
        const rows = Array.from({length: this.size}, (_, k) => k).sort(() => Math.random() - 0.5);
        const cols = Array.from({length: this.size}, (_, k) => k).sort(() => Math.random() - 0.5);

        for (const r of rows) {
            if (placed) break;
            for (const c of cols) {
                if (placed) break;
                if (this.grid[r][c] !== '') {
                    const commonChar = this.grid[r][c];
                    // 在候选词中找公共点
                    for (let charI = 0; charI < candidate.answer.length; charI++) {
                        if (candidate.answer[charI] === commonChar) {
                            // 试横向
                            const startCTry = c - charI;
                            if (startCTry >= 0 && this.canPlace(candidate.answer, r, startCTry, 'across')) {
                                this.place(candidate, r, startCTry, 'across');
                                placed = true;
                                break;
                            }
                            // 试纵向
                            const startRTry = r - charI;
                            if (startRTry >= 0 && this.canPlace(candidate.answer, startRTry, c, 'down')) {
                                this.place(candidate, startRTry, c, 'down');
                                placed = true;
                                break;
                            }
                        }
                    }
                }
            }
        }

        if (placed) {
          words.splice(i, 1); // 移除已放置的词
        }
      }
    }
    
    return this.placedWords;
  }
}
