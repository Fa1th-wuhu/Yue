from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    author: str = Field(min_length=1, max_length=128)
    category: str = Field(min_length=1, max_length=64)
    views: int = 0
    likes: int = 0
    is_daily_rec: bool = False
    cover_img: str = ""


class BookUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    author: str = Field(min_length=1, max_length=128)
    category: str = Field(min_length=1, max_length=64)


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    category: str
    views: int
    likes: int
    is_daily_rec: bool
    cover_img: str = ""

    class Config:
        from_attributes = True


class ChapterCreate(BaseModel):
    book_id: int
    chapter_num: int
    title: str = Field(min_length=1, max_length=128)
    content: str = Field(min_length=1)


class ChapterUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    content: str = Field(min_length=1)


class ChapterOut(BaseModel):
    id: int
    book_id: int
    chapter_num: int
    title: str
    content: str

    class Config:
        from_attributes = True


class BookshelfCreate(BaseModel):
    user_id: int
    book_id: int


class BookshelfOut(BaseModel):
    id: int
    user_id: int
    book_id: int

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    user_id: int
    username: str = Field(min_length=1, max_length=64)
    book_id: int
    content: str = Field(min_length=1)
    created_at: str = Field(min_length=1, max_length=32)


class CommentOut(BaseModel):
    id: int
    user_id: int
    username: str
    book_id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True
