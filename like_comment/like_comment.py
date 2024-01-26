from datetime import datetime
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, exists, delete
from auth.utils import verify_token
from database import get_async_session
from like_comment.schema import Like, Liked_products, Comment
from models.models import like, comment

like_comment = APIRouter()


@like_comment.post('/like')
async def like_post(like_model: Like, session: AsyncSession = Depends(get_async_session),
                    token: dict = Depends(verify_token)):
    if token is not None:
        user_id = token.get('user_id')

        # Check if the product has already been liked
        query_1 = select(exists().where(like.c.product_id == like_model.product_id))
        is_liked = await session.execute(query_1)
        if is_liked.scalar():
            return {'success': False, 'message': 'Product already liked'}

        # Insert the like record
        current_datetime = datetime.now()
        query = insert(like).values(**dict(like_model), user_id=user_id, created_at=current_datetime)
        await session.execute(query)
        await session.commit()

        return {'success': True, 'message': 'Product liked'}
    else:
        return {'success': False, 'message': 'Invalid token'}


@like_comment.post('/dislike')
async def like_post(like_model: Like, session: AsyncSession = Depends(get_async_session),
                    token: dict = Depends(verify_token)):
    if token is not None:
        user_id = token.get('user_id')

        query_1 = select(exists().where(like.c.product_id == like_model.product_id))
        is_liked = await session.execute(query_1)
        if is_liked.scalar():
            # Delete the existing like record
            delete_query = delete(like).where(
                (like.c.product_id == like_model.product_id) &
                (like.c.user_id == user_id)
            )
            await session.execute(delete_query)
            await session.commit()
            return {'success': True, 'message': 'Product disliked'}


@like_comment.get('/liked_products', response_model=List[Liked_products])
async def list_liked_products(session: AsyncSession = Depends(get_async_session),
                              token: dict = Depends(verify_token)):
    if token is not None:
        user_id = token.get('user_id')
        query = select(like).where(like.c.user_id == user_id)
        result = await session.execute(query)
        liked_products = result.all()

        # Check if the user has liked any products
        if liked_products:
            return liked_products
        else:
            return {'success': False, 'message': 'No liked products found'}
    else:
        return {'success': False, 'message': 'Invalid token'}


@like_comment.post('/comment')
async def like_post(like_model: Comment, session: AsyncSession = Depends(get_async_session),
                    token: dict = Depends(verify_token)):
    if token is not None:
        user_id = token.get('user_id')
        current_datetime = datetime.now()
        query = insert(comment).values(**dict(like_model), user_id=user_id, created_at=current_datetime)
        await session.execute(query)
        await session.commit()

        return {'success': True, 'message': 'Comment added'}
    else:
        return {'success': False, 'message': 'Invalid token'}