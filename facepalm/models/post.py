from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str

class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CommentsIn(BaseModel):
    body: str

class Comments(CommentsIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class PostsWithComments(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    post: UserPost
    comments: list[Comments]