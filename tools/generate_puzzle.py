import json
import random
import os

# ==========================================
# 1. 原材料 (Material): 30个汽车领域专业词汇
# ==========================================
RAW_WORDS = [
    # --- 核心龙骨词 (长词，容易形成骨架) ---
    {"answer": "トランスミッション", "clue": "【动力】改变扭矩和转速的装置 (Transmission)", "hint": "ト_______"},
    {"answer": "ワイヤーハーネス", "clue": "【电子】汽车的神经血管，线束 (Wire Harness)", "hint": "ワ_______"},
    {"answer": "サスペンション", "clue": "【底盘】缓冲震动的悬挂系统 (Suspension)", "hint": "サ______"},
    {"answer": "スピードメーター", "clue": "【内饰】显示车速的仪表 (Speedometer)", "hint": "ス_______"},
    {"answer": "フロントガラス", "clue": "【车身】前面的挡风玻璃 (Windshield)", "hint": "フ______"},
    {"answer": "オルタネーター", "clue": "【电气】给电瓶充电的发电机 (Alternator)", "hint": "オ_______"},
    
    # --- 中等长度词 (主力军) ---
    {"answer": "バッテリー", "clue": "【电气】储存电能的装置 (Battery)", "hint": "バ____"},
    {"answer": "ラジエーター", "clue": "【动力】冷却引擎的散热器 (Radiator)", "hint": "ラ_____"},
    {"answer": "エンジン", "clue": "【动力】汽车的心脏 (Engine)", "hint": "エ___"},
    {"answer": "マフラー", "clue": "【排气】减少噪音的消音器 (Muffler)", "hint": "マ___"},
    {"answer": "バンパー", "clue": "【车身】前后防撞的护板 (Bumper)", "hint": "バ___"},
    {"answer": "ハンドル", "clue": "【内饰】控制方向的方向盘 (Steering Wheel)", "hint": "ハ___"},
    {"answer": "ブレーキ", "clue": "【底盘】让车减速的装置 (Brake)", "hint": "ブ___"},
    {"answer": "ガソリン", "clue": "【能源】内燃机的燃料 (Gasoline)", "hint": "ガ___"},
    {"answer": "ワイパー", "clue": "【车身】刮雨器 (Wiper)", "hint": "ワ___"},
    {"answer": "エアコン", "clue": "【舒适】空气调节系统 (Air Con)", "hint": "エ___"},
    {"answer": "センサー", "clue": "【电子】感知道路信息的器件 (Sensor)", "hint": "セ___"},
    {"answer": "カメラ", "clue": "【电子】辅助驾驶的眼睛 (Camera)", "hint": "カ__"},
    {"answer": "エアバッグ", "clue": "【安全】碰撞时弹出的气囊 (Airbag)", "hint": "エ____"},
    
    # --- 短词 (用于填补缝隙，极重要) ---
    {"answer": "タイヤ", "clue": "【底盘】唯一接触地面的橡胶 (Tire)", "hint": "タ__"},
    {"answer": "ドア", "clue": "【车身】乘客进出的门 (Door)", "hint": "ド_"},
    {"answer": "キー", "clue": "【车身】启动汽车的钥匙 (Key)", "hint": "キ_"},
    {"answer": "ギア", "clue": "【机械】传递动力的齿轮 (Gear)", "hint": "ギ_"},
    {"answer": "オイル", "clue": "【维护】润滑用的油 (Oil)", "hint": "オ__"},
    {"answer": "バス", "clue": "【通信】CAN___，数据总线 (Bus)", "hint": "バ_"},
    {"answer": "リレー", "clue": "【电子】电磁继电器 (Relay)", "hint": "リ__"},
    {"answer": "ヒューズ", "clue": "【电子】过流保护熔断器 (Fuse)", "hint": "ヒ___"},
    {"answer": "ランプ", "clue": "【电子】照明灯具 (Lamp)", "hint": "ラ__"},
    {"answer": "ミラー", "clue": "【车身】后视镜 (Mirror)", "hint": "ミ__"},
    {"answer": "シート", "clue": "【内饰】乘客坐的椅子 (Seat)", "hint": "シ__"}
]

# ==========================================
# 2. 核心算法类 (Method)
# ==========================================
class CrosswordGenerator:
    def __init__(self, size=12):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)] # N*N 空矩阵
        self.placed_words = [] # 记录已放置的单词信息

    def can_place(self, word, r, c, direction):
        """
        质量检测 (Measurement): 检查放置位置是否合法
        1. 边界检查
        2. 冲突检查 (已有字母是否匹配)
        3. 邻接检查 (避免单词并排粘连)
        """
        length = len(word)
        
        # A. 边界检查
        if direction == 'across':
            if c + length > self.size: return False
            if c - 1 >= 0 and self.grid[r][c-1] != '': return False # 左边要有空
            if c + length < self.size and self.grid[r][c+length] != '': return False # 右边要有空
        else: # down
            if r + length > self.size: return False
            if r - 1 >= 0 and self.grid[r-1][c] != '': return False # 上边要有空
            if r + length < self.size and self.grid[r+length][c] != '': return False # 下边要有空

        # B. 逐格检查 (碰撞与匹配)
        for i in range(length):
            curr_r = r + (0 if direction == 'across' else i)
            curr_c = c + (i if direction == 'across' else 0)
            
            cell_char = self.grid[curr_r][curr_c]
            
            # 如果格子非空，必须字符一致 (交叉点)
            if cell_char != '' and cell_char != word[i]:
                return False
            
            # 如果格子是空的，我们需要检查它的"两侧"是否有其他单词
            # (防止出现非预期的并排粘连)
            if cell_char == '':
                if direction == 'across':
                    # 检查上下是否为空
                    if curr_r-1 >= 0 and self.grid[curr_r-1][curr_c] != '' and self.grid[curr_r-1][curr_c] != word[i]: return False # 这里简化逻辑，只要上下有东西就很难办，除非是十字交叉，这里为了MVP先严一点
                    if curr_r+1 < self.size and self.grid[curr_r+1][curr_c] != '': return False
                else: # down
                    # 检查左右是否为空
                    if curr_c-1 >= 0 and self.grid[curr_r][curr_c-1] != '': return False
                    if curr_c+1 < self.size and self.grid[curr_r][curr_c+1] != '': return False

        return True

    def place(self, word_obj, r, c, direction):
        """执行放置动作"""
        word = word_obj['answer']
        for i in range(len(word)):
            curr_r = r + (0 if direction == 'across' else i)
            curr_c = c + (i if direction == 'across' else 0)
            self.grid[curr_r][curr_c] = word[i]
        
        # 记录数据，准备输出 JSON
        self.placed_words.append({
            "id": f"gen_{len(self.placed_words)+1}",
            "answer": word,
            "clue_cn": word_obj['clue'],
            "clue_jp_hint": word_obj['hint'],
            "start_x": c + 1,  # 注意：Vue 里也是从 0 开始还是 1 开始？我们之前的 JSON 好像是从 1 开始的，这里我们输出 0索引，前端适配一下，或者这里 +1
            "start_y": r + 1,
            "orientation": direction,
            "length": len(word)
        })

    def generate(self, words):
        """
        主生产逻辑 (升级版：引入随机性)
        """
        # 1. 龙骨策略：先找出最长的一个词作为“地基”，保证棋盘铺得开
        # 先按长度排序，取最长的一个
        words.sort(key=lambda x: len(x['answer']), reverse=True)
        first_word = words.pop(0) # 取出并从列表中移除
        
        # 放置第一个词 (正中间)
        start_r = self.size // 2
        start_c = (self.size - len(first_word['answer'])) // 2
        self.place(first_word, start_r, start_c, 'across')
        
        # 2. 随机策略：剩下的词，我们打乱顺序再试
        # 这就是让每次结果不一样的关键！
        random.shuffle(words) 
        
        # 记录已放置的单词，目前的列表里虽然移除了first_word，但我们需要一个放置队列
        # 为了简单起见，我们不断循环尝试剩余的列表
        
        added_count = 0
        max_attempts = 100 # 防止死循环
        
        while max_attempts > 0 and len(words) > 0:
            max_attempts -= 1
            
            # 遍历每一个还没放进去的词
            # 我们倒序遍历，这样如果成功放进去，可以安全地从列表移除
            for i in range(len(words) - 1, -1, -1):
                candidate = words[i]
                placed = False
                
                # 全局扫描寻找挂载点
                # (为了增加随机性，我们甚至可以随机打乱遍历格子的顺序，但这里先只打乱单词顺序)
                for r in range(self.size):
                    for c in range(self.size):
                        if self.grid[r][c] != '':
                            common_char = self.grid[r][c]
                            # 在候选词里找公共点
                            for char_i, char in enumerate(candidate['answer']):
                                if char == common_char:
                                    # 试横向
                                    start_c_try = c - char_i
                                    if start_c_try >= 0 and self.can_place(candidate['answer'], r, start_c_try, 'across'):
                                        self.place(candidate, r, start_c_try, 'across')
                                        placed = True
                                        break
                                    
                                    # 试纵向
                                    start_r_try = r - char_i
                                    if start_r_try >= 0 and self.can_place(candidate['answer'], start_r_try, c, 'down'):
                                        self.place(candidate, start_r_try, c, 'down')
                                        placed = True
                                        break
                            if placed: break
                    if placed: break
                
                # 如果放成功了，就从待办列表里移除
                if placed:
                    words.pop(i)
                    added_count += 1

# ==========================================
# 4. 执行生产 (Execution)
# ==========================================
if __name__ == "__main__":
    generator = CrosswordGenerator(size=10) # 10x10 网格
    generator.generate(RAW_WORDS)
    
    # 构造最终 JSON 结构
    output_data = {
        "meta": {
            "version": "2.0 (Auto-Generated)",
            "grid_dimension": 10
        },
        "reward": {
            "id": "gen_reward",
            "type": "random", # 标记为随机，前端已经不看这个字段了，看 Service
            "desc": "Auto Generated Level"
        },
        "matrix": generator.placed_words
    }
    
    # 写入文件
    # 自动定位到 src/data/level_gen.json
    output_path = os.path.join(os.path.dirname(__file__), '../src/data/level_gen.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ 生产完成！已生成 {len(generator.placed_words)}/{len(RAW_WORDS)} 个单词。")
    print(f"📂 文件路径: {output_path}")
    