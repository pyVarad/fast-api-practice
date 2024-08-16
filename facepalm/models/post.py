from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str

class UserPost(UserPostIn):
    id: int

class CommentsIn(BaseModel):
    body: str

class Comments(CommentsIn):
    id: int

class PostsWithComments(BaseModel):
    post: UserPost
    comments: list[Comments]