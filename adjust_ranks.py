import sqlite3
from pathlib import Path

def adjust():
    # 查找数据库文件
    db_paths = [
        Path(r"c:\Users\Fa1th\Desktop\Yue\data\yue.db"),
        Path(r"c:\Users\Fa1th\Desktop\Yue\backend\data\yue.db"),
        Path(r"data/yue.db"),
        Path(r"backend/data/yue.db")
    ]
    
    db_path = None
    for p in db_paths:
        if p.exists():
            db_path = p
            break
            
    if not db_path:
        print("未找到 SQLite 数据库！")
        return
        
    print(f"正在连接数据库: {db_path.resolve()}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 设计差异化的点击量与点赞数（制造“高点击低点赞”和“低点击高点赞”的趣味差异）
    adjustments = [
        # (views, likes, title)
        (152000, 9821, "剑来"),
        (112000, 920, "三国之惧内王爷"),          # 高点击，低点赞 (标题党/快餐文)
        (94000, 1050, "我的美女总裁未婚妻"),      # 高点击，中点赞 (经典爽文)
        (85100, 4500, "全世界只有我不知道我是高人"), # 中等点击，极高点赞 (神作)
        (43200, 3200, "从追老婆开始走向巅峰"),      # 低点击，高点赞 (小众口碑作)
        (35000, 2500, "修仙从极简代码开始"),        # 极简修仙，极高口碑
        (12053, 850, "银河战纪：全栈大帝"),
        (8600, 420, "重回1998：我是系统架构师"),
        (4342, 380, "大唐：我的代码能推演国运")
    ]
    
    for views, likes, title in adjustments:
        cursor.execute("""
            UPDATE books 
            SET views = ?, likes = ? 
            WHERE title = ?
        """, (views, likes, title))
        if cursor.rowcount > 0:
            print(f"成功调整《{title}》: 点击量={views}, 点赞数={likes}")
        else:
            print(f"未找到图书《{title}》，跳过调整")
            
    conn.commit()
    conn.close()
    print("数据库点击量与点赞数差异化调整完成！")

if __name__ == "__main__":
    adjust()
