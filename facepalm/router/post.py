from fastapi import APIRouter, HTTPException

from facepalm.models.post import (
    Comments,
    CommentsIn,
    PostsWithComments,
    UserPost,
    UserPostIn,
)

router = APIRouter()

all_posts = {}
all_comments = {}

def get_post_by_id(post_id: int):
    return all_posts.get(post_id)

@router.get("/", response_model=list[UserPost])
async def get_all_posts():
    return all_posts.values()

@router.post("/", response_model=UserPost)
async def add_new_post(post: UserPostIn):
    data = post.dict()
    post_id = len(all_posts)
    new_post = {**data, "id": post_id}
    all_posts[post_id] = new_post
    return new_post

@router.post("/{post_id}/comment", response_model=Comments)
async def add_new_comment(post_id: int, comment: CommentsIn):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.dict()
    comment_id = len(all_comments)
    new_comment = {**data, "id": comment_id, "post_id": post_id}
    all_comments[comment_id] = new_comment
    return new_comment

@router.get("/{post_id}/comment", response_model=list[Comments])
async def get_all_comments_for_a_given_post_id(post_id: int):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return [comment for comment in all_comments.values() if comment["post_id"] == post_id]

@router.get("/{post_id}", response_model=PostsWithComments)
async def get_post_id(post_id: int):
    post = get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": await get_all_comments_for_a_given_post_id(post_id)
    }
