from fastapi import APIRouter, HTTPException
import logging
from facepalm.database import comments_table, database, post_table
from facepalm.models.post import (
    Comments,
    CommentsIn,
    PostsWithComments,
    UserPost,
    UserPostIn,
)

router = APIRouter()
logger = logging.getLogger(__name__)


async def get_post_by_id(post_id: int):
    logger.info(f"Getting posts for a given {post_id}")
    query = post_table.select().where(post_table.c.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)


@router.get("/", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


@router.post("/", response_model=UserPost, status_code=201)
async def add_new_post(post: UserPostIn):
    logger.info(f"Add a new post")
    logger.debug(post)
    data = post.model_dump()
    query = post_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.post("/{post_id}/comment", response_model=Comments, status_code=201)
async def add_new_comment(post_id: int, comment: CommentsIn):
    logger.info(f"Adding comment to a post {post_id}")
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.model_dump()
    query = comments_table.insert().values({**data, "post_id": post_id})
    logger.debug(comment)
    logger.debug(query)
    last_comment_id = await database.execute(query)
    return {**data, "id": last_comment_id, "post_id": post_id}


@router.get("/{post_id}/comment", response_model=list[Comments])
async def get_all_comments_for_a_given_post_id(post_id: int):
    logger.info(f"Fetch all comments for the post_id {post_id} with comments.")
    query = comments_table.select().where(comments_table.c.post_id == post_id)
    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/{post_id}", response_model=PostsWithComments)
async def get_post_id(post_id: int):
    logger.info(f"Fetch all posts along with comments for the given post_id {post_id}")
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": await get_all_comments_for_a_given_post_id(post_id)
    }
