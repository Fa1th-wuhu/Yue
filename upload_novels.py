import os
import re
import sqlite3
from pathlib import Path

# 映射小说文件名到书籍元数据
BOOKS_META = {
    "全世界只有我不知道我是高人.txt": {
        "title": "全世界只有我不知道我是高人",
        "author": "老魔童",
        "category": "都市",
        "views": 85100,
        "likes": 2341,
        "is_daily_rec": True,
        "max_chapters": 150 # 导入前150章
    },
    "三国之惧内王爷.txt": {
        "title": "三国之惧内王爷",
        "author": "一杯咸汁",
        "category": "历史",
        "views": 62400,
        "likes": 1823,
        "is_daily_rec": False,
        "max_chapters": 150 # 导入前150章
    },
    "剑来(1-500章).txt": {
        "title": "剑来",
        "author": "烽火戏诸侯",
        "category": "玄幻",
        "views": 152000,
        "likes": 9821,
        "is_daily_rec": True,
        "max_chapters": 50 # 剑来非常长，导入前50章
    },
    "我的美女总裁未婚妻.txt": {
        "title": "我的美女总裁未婚妻",
        "author": "霉干菜烧肉",
        "category": "都市",
        "views": 71100,
        "likes": 1941,
        "is_daily_rec": False,
        "max_chapters": 50 # 导入前50章
    },
    "从追老婆开始走向巅峰.txt": {
        "title": "从追老婆开始走向巅峰",
        "author": "九月不度",
        "category": "都市",
        "views": 43200,
        "likes": 1102,
        "is_daily_rec": False,
        "max_chapters": 50 # 导入前50章
    }
}

# 常见章节正则表达式（支持：第1章、第一章、第123章、第 1 章等）
CHAPTER_PATTERN = re.compile(r'^\s*(第\s*[0-9一二三四五六七八九十百千两]+\s*[章节集卷].*)$')

def read_file_with_encoding(file_path):
    """尝试用不同编码读取文本文件"""
    encodings = ["utf-8", "gb18030", "gbk", "ansi"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
                print(f"成功使用 {enc} 编码读取: {file_path.name}")
                return content
        except UnicodeDecodeError:
            continue
    raise ValueError(f"无法读取文件 {file_path.name}，请检查编码。")

def parse_and_insert_books():
    # 确定数据库路径
    # 本地路径
    db_paths = [
        Path(r"c:\Users\Fa1th\Desktop\Yue\data\yue.db"),
        Path(r"c:\Users\Fa1th\Desktop\Yue\backend\data\yue.db"),
        Path(r"/var/lib/docker/volumes/yue_yue_data/_data/yue.db"), # 云端宿主机路径
        Path(r"data/yue.db"),
        Path(r"backend/data/yue.db")
    ]
    
    db_path = None
    for p in db_paths:
        if p.exists():
            db_path = p
            break
            
    if not db_path:
        print("未找到 SQLite 数据库，将在本地创建一个新的数据库 (data/yue.db)")
        db_path = Path("data/yue.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
    print(f"准备连接数据库: {db_path.resolve()}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 确保分类存在（添加‘都市’、‘科幻’、‘玄幻’、‘历史’等）
    existing_categories = [row[0] for row in cursor.execute("SELECT name FROM categories").fetchall()]
    for cat in ["玄幻", "都市", "科幻", "历史"]:
        if cat not in existing_categories:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
            print(f"添加新分类: {cat}")
            
    # 获取‘小说资源’目录
    resources_dir = Path(r"c:\Users\Fa1th\Desktop\Yue\小说资源")
    if not resources_dir.exists():
        resources_dir = Path("小说资源")
        
    if not resources_dir.exists():
        print("未找到‘小说资源’文件夹！")
        return
        
    for file_name, meta in BOOKS_META.items():
        file_path = resources_dir / file_name
        if not file_path.exists():
            print(f"跳过未找到的文件: {file_name}")
            continue
            
        print(f"\n开始解析小说: 《{meta['title']}》...")
        try:
            content = read_file_with_encoding(file_path)
        except Exception as e:
            print(f"读取小说失败: {e}")
            continue
            
        lines = content.splitlines()
        
        # 分章提取
        chapters_data = []
        current_chapter_title = "前言/引子"
        current_chapter_content = []
        chapter_count = 0
        
        for line in lines:
            line_stripped = line.strip()
            # 匹配章节名
            match = CHAPTER_PATTERN.match(line)
            if match and chapter_count < meta["max_chapters"]:
                # 保存前一个章节
                if current_chapter_content:
                    chapters_data.append((
                        chapter_count,
                        current_chapter_title,
                        "\n".join(current_chapter_content)
                    ))
                
                # 开始新章节
                current_chapter_title = match.group(1).strip()
                current_chapter_content = []
                chapter_count += 1
            else:
                if line_stripped or current_chapter_content: # 避免过多空行
                    current_chapter_content.append(line)
                    
        # 别忘了保存最后一章
        if current_chapter_content and chapter_count <= meta["max_chapters"]:
            chapters_data.append((
                chapter_count,
                current_chapter_title,
                "\n".join(current_chapter_content)
            ))
            
        print(f"成功解析出 {len(chapters_data)} 个章节。")
        
        if not chapters_data:
            print(f"警告: 未能从《{meta['title']}》中匹配到章节，请检查格式。")
            continue
            
        # 写入数据库
        # 检查是否已存在同名小说
        cursor.execute("SELECT id FROM books WHERE title = ?", (meta["title"],))
        row = cursor.fetchone()
        if row:
            book_id = row[0]
            print(f"《{meta['title']}》已存在，ID 为: {book_id}。正在覆盖更新章节...")
            cursor.execute("DELETE FROM chapters WHERE book_id = ?", (book_id,))
        else:
            cursor.execute("""
                INSERT INTO books (title, author, category, views, likes, is_daily_rec, cover_img)
                VALUES (?, ?, ?, ?, ?, ?, '')
            """, (meta["title"], meta["author"], meta["category"], meta["views"], meta["likes"], meta["is_daily_rec"]))
            book_id = cursor.lastrowid
            print(f"成功创建新书《{meta['title']}》，分配 ID: {book_id}")
            
        # 批量插入章节
        inserted_chapters = []
        for idx, (ch_num, ch_title, ch_content) in enumerate(chapters_data):
            # 清洗内容：去除开头章节名重复，整理空行
            clean_lines = []
            for l in ch_content.splitlines():
                if l.strip() == ch_title:
                    continue
                clean_lines.append(l)
            ch_content_clean = "\n".join(clean_lines).strip()
            
            if not ch_content_clean:
                continue # 过滤空章节
                
            inserted_chapters.append((
                book_id,
                idx + 1, # 使用1-based连续序列索引，100%避免主键冲突
                ch_title,
                ch_content_clean
            ))
            
        cursor.executemany("""
            INSERT INTO chapters (book_id, chapter_num, title, content)
            VALUES (?, ?, ?, ?)
        """, inserted_chapters)
        print(f"成功将 {len(inserted_chapters)} 章节写入数据库！")
        conn.commit()
        
    conn.close()
    print("\n所有小说导入任务全部完成！")

if __name__ == "__main__":
    parse_and_insert_books()
