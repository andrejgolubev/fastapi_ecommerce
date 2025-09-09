from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func, select, update
from app.auth import get_current_seller, get_current_user
from app.db_depends import get_db, get_async_db
from sqlalchemy.ext.asyncio import AsyncSession 
from app.auth import hash_password, verify_password, create_access_token, create_refresh_token
import jwt
from app.models import reviews
from app.schemas import ReviewCreate,ReviewRespond
from models import Review as ReviewModel, User as UserModel, Product as ProductModel



router = APIRouter(prefix='/reviews', tags=['reviews'])

@router.get('/', response_model=list[ReviewRespond])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)): 
    rev_result = await db.scalars(select(ReviewModel))
    return rev_result.all() 

@router.get('/products/{product_id}/reviews/', response_model=ReviewRespond)
async def get_product_reviews(product_id: int,
                              db: AsyncSession = Depends(get_async_db), 
                              ):
    
    rev_result = await db.scalars(select(ReviewModel).where(
        ReviewModel.product_id == product_id, 
        ReviewModel.is_active == True, 
    ))
    
    review = rev_result.first()
    if not review: 
        return HTTPException(status_code=404)
    return review                      

@router.post('/reviews')
async def leave_review(review: ReviewCreate,
                       db: AsyncSession = Depends(get_async_db), 
                       current_user: UserModel = Depends(get_current_user),
                       ): 
    
    if not current_user.email or not current_user.role: 
        raise HTTPException(status_code=403)
    
    user_res = await db.scalars(select(UserModel).where(UserModel.id == current_user.id))
    if not user_res.first(): 
        raise HTTPException(status_code=404)


    avg_grade_result = await db.scalars(select(func.avg(ReviewModel)).where(
        ReviewModel.product_id == review.product_id))
    avg_grade = avg_grade_result.first()
    
    db.execute(update(ProductModel)
               .where(
                ProductModel.id == review.product_id, 
                ProductModel.is_active == True,
                )
                .values(
                    rating = avg_grade
                ))

    reviews_result = await db.scalars(select(ReviewModel).where(
        ReviewModel.is_active == True, 
        ReviewModel.id == review.id
        ))
    
    review = reviews_result.first()