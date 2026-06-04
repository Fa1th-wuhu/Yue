import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db
from .seed import seed_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="简阅后端 API", version="1.0.0")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_FILE = Path(os.getenv("FRONTEND_FILE", PROJECT_ROOT / "code_artifact.html")).resolve()


@app.on_event("startup")
def on_startup() -> None:
    Path("data").mkdir(exist_ok=True)
    db = next(get_db())
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/")
def index():
    if FRONTEND_FILE.exists():
        return FileResponse(FRONTEND_FILE)
    return {"name": "简阅后端 API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/users/login", response_model=schemas.UserOut)
def login(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == payload.username,
        models.User.password == payload.password,
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码不正确")
    return user


@app.post("/api/users/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(username=payload.username.strip(), password=payload.password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="用户已存在") from None
    db.refresh(user)
    return user


@app.get("/api/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).order_by(models.Category.id.asc()).all()


@app.post("/api/categories", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def add_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = models.Category(name=payload.name.strip())
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="分类已存在") from None
    db.refresh(category)
    return category


@app.delete("/api/categories/{cat_name}")
def delete_category(cat_name: str, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.name == cat_name).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
    db.delete(category)
    db.commit()
    return {"ok": True}


@app.get("/api/admin/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    total_books = db.query(models.Book).count()
    total_chapters = db.query(models.Chapter).count()
    
    views_sum = db.query(func.sum(models.Book.views)).scalar()
    total_views = int(views_sum) if views_sum is not None else 0
    
    likes_sum = db.query(func.sum(models.Book.likes)).scalar()
    total_likes = int(likes_sum) if likes_sum is not None else 0
    
    total_comments = db.query(models.Comment).count()
    
    # 分类统计分布
    results = db.query(models.Book.category, func.count(models.Book.id)).group_by(models.Book.category).all()
    category_counts = {cat: count for cat, count in results}
    
    return {
        "total_books": total_books,
        "total_chapters": total_chapters,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "category_counts": category_counts
    }


@app.get("/api/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).order_by(models.Book.id.asc()).all()


@app.post("/api/books", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    book = models.Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/api/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    book.title = payload.title.strip()
    book.author = payload.author.strip()
    book.category = payload.category.strip()
    db.commit()
    db.refresh(book)
    return book


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    # 手动删除关联，100%安全兼容任何 SQLite 外键设置
    db.query(models.Chapter).filter(models.Chapter.book_id == book_id).delete()
    db.query(models.Bookshelf).filter(models.Bookshelf.book_id == book_id).delete()
    db.query(models.Comment).filter(models.Comment.book_id == book_id).delete()
    db.delete(book)
    db.commit()
    return {"ok": True}


@app.post("/api/books/{book_id}/like")
def like_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    book.likes += 1
    db.commit()
    return {"ok": True, "likes": book.likes}


@app.get("/api/chapters", response_model=list[schemas.ChapterOut])
def list_chapters(db: Session = Depends(get_db)):
    return db.query(models.Chapter).order_by(models.Chapter.book_id.asc(), models.Chapter.chapter_num.asc()).all()


@app.post("/api/chapters", response_model=schemas.ChapterOut, status_code=status.HTTP_201_CREATED)
def create_chapter(payload: schemas.ChapterCreate, db: Session = Depends(get_db)):
    if not db.get(models.Book, payload.book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    chapter = models.Chapter(**payload.model_dump())
    db.add(chapter)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="章节序号已存在") from None
    db.refresh(chapter)
    return chapter


@app.put("/api/chapters/{chapter_id}", response_model=schemas.ChapterOut)
def update_chapter(chapter_id: int, payload: schemas.ChapterUpdate, db: Session = Depends(get_db)):
    chapter = db.get(models.Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="章节不存在")
    chapter.title = payload.title.strip()
    chapter.content = payload.content
    db.commit()
    db.refresh(chapter)
    return chapter


@app.get("/api/bookshelf", response_model=list[schemas.BookshelfOut])
def list_bookshelf(db: Session = Depends(get_db)):
    return db.query(models.Bookshelf).order_by(models.Bookshelf.id.asc()).all()


@app.post("/api/bookshelf", response_model=schemas.BookshelfOut, status_code=status.HTTP_201_CREATED)
def add_bookshelf(payload: schemas.BookshelfCreate, db: Session = Depends(get_db)):
    if not db.get(models.User, payload.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if not db.get(models.Book, payload.book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    item = models.Bookshelf(user_id=payload.user_id, book_id=payload.book_id)
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        item = db.query(models.Bookshelf).filter(
            models.Bookshelf.user_id == payload.user_id,
            models.Bookshelf.book_id == payload.book_id,
        ).first()
        if item:
            return item
        raise
    db.refresh(item)
    return item


@app.delete("/api/bookshelf/{item_id}")
def delete_bookshelf(item_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Bookshelf, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书架记录不存在")
    db.delete(item)
    db.commit()
    return {"ok": True}


@app.get("/api/comments", response_model=list[schemas.CommentOut])
def list_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).order_by(models.Comment.id.asc()).all()


@app.post("/api/comments", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    if not db.get(models.User, payload.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if not db.get(models.Book, payload.book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="书籍不存在")
    comment = models.Comment(**payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
