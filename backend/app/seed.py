from sqlalchemy.orm import Session

from . import models


def seed_data(db: Session) -> None:
    if db.query(models.User).first():
        return

    users = [
        models.User(id=1, username="admin", password="123456"),
        models.User(id=2, username="user1", password="123456"),
    ]
    categories = [
        models.Category(name="玄幻"),
        models.Category(name="都市"),
        models.Category(name="科幻"),
        models.Category(name="历史"),
    ]
    books = [
        models.Book(id=1, title="修仙从极简代码开始", author="无bug尊者", category="玄幻", views=8848, likes=231, is_daily_rec=False),
        models.Book(id=2, title="重回1998：我是系统架构师", author="键盘极客", category="都市", views=5621, likes=119),
        models.Book(id=3, title="银河战纪：全栈大帝", author="Docker船长", category="科幻", views=12053, likes=541),
        models.Book(id=4, title="大唐：我的代码能推演国运", author="极简刺客", category="历史", views=3342, likes=88),
        models.Book(id=5, title="剑来", author="烽火戏诸侯", category="玄幻", views=152000, likes=9821, is_daily_rec=True),
    ]
    chapters = [
        models.Chapter(id=1, book_id=1, chapter_num=1, title="练气期：配置环境", content="    林凡睁开眼，发现自己穿越到了修仙界。这个世界的灵气居然是按字节流传输的。\n    “天之道，损有余而补不足，配置好镜像源，成帝之路便开始了一半。”他默念祖传的极简筑基口诀：\n    docker-compose up -d --build\n    顷刻间，天空五彩祥云凝聚，筑基异象骤起！"),
        models.Chapter(id=2, book_id=1, chapter_num=2, title="筑基期：打包运行", content="    只消数息，林凡成功开辟丹田内网。由于没有多余的冗余依赖，他的法力之纯净世所罕见。\n    突然，不远处走来一位筑基期的守山弟子，高傲地喝道：“来者何人，竟敢在主峰地界私设对外端口？”\n    林凡面色沉静，反手扔出一份多阶段构建的 Dockerfile。"),
        models.Chapter(id=3, book_id=2, chapter_num=1, title="重生之夜的电脑微光", content="    1998年。林雨醒来，四周是散落的软盘和厚重的台式显示器。\n    “我真的重生了。”他看着手底尚未干涸的软盘，下定决心要用极简架构改变二十年后的互联网。"),
        models.Chapter(id=4, book_id=3, chapter_num=1, title="机械降神：终极编排", content="    太空母舰的控制室亮起刺眼的红灯。\n    全栈帝国的边缘防线被宇宙异能侵袭，“用极致的分布式逻辑，把火力容器化！”大帝咆哮着下达命令。"),
        models.Chapter(id=5, book_id=5, chapter_num=1, title="第一章：泥瓶巷的贫寒少年", content="    大千世界，无奇不有。我陈平安，唯有一剑，可搬山，倒海，降妖，镇魔，敕神，摘星，断江，摧城，开天！\n    泥瓶巷的清晨，小镇的天空有些阴沉，那个被称为陈平安的孤苦少年，正守着自己空荡荡的泥瓶，望着远方的苍穹。"),
        models.Chapter(id=6, book_id=5, chapter_num=2, title="第二章：惊蛰与藏书", content="    小镇清晨，风雨凄迷。少年默默背起柴篓，走在青石板铺就的小巷中。那些高高在上的修行仙人，终究是不懂这泥瓶巷里的市井温情与坚守，只顾夺取这片小天地的造化气运。"),
    ]
    bookshelf = [
        models.Bookshelf(id=1, user_id=1, book_id=1),
        models.Bookshelf(id=2, user_id=1, book_id=3),
    ]
    comments = [
        models.Comment(id=1, user_id=1, username="admin", book_id=1, content="实训必看！极简主义深得我心，Docker部署一次就跑通了！", created_at="2026-05-20 10:11"),
        models.Comment(id=2, user_id=2, username="user1", book_id=1, content="太真实了，原来神仙修仙也要配置镜像源。", created_at="2026-05-21 14:22"),
    ]

    db.add_all(users + categories + books + chapters + bookshelf + comments)
    db.commit()
