from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func, select, update
from app.auth import get_current_seller, get_current_user, get_current_admin
from app.db_depends import get_db, get_async_db
from sqlalchemy.ext.asyncio import AsyncSession 
from app.auth import hash_password, verify_password, create_access_token, create_refresh_token
import jwt
from app.models import reviews
from app.schemas import ReviewCreate,ReviewRespond
from app.models import Review as ReviewModel, User as UserModel, Product as ProductModel



router = APIRouter(prefix='/reviews', tags=['reviews'])

@router.get('/', response_model=list[ReviewRespond])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)): 
    rev_result = await db.scalars(select(ReviewModel))
    return rev_result.all() 

@router.get('/products/{product_id}/reviews/', response_model=list[ReviewRespond])
async def get_product_reviews(product_id: int,
                              db: AsyncSession = Depends(get_async_db), 
                              ):
    
    rev_result = await db.scalars(select(ReviewModel).where(
        ReviewModel.product_id == product_id, 
        ReviewModel.is_active == True, 
    ))
    
    review = rev_result.all()
    if not review: 
        raise HTTPException(status_code=404)
    
    return review                      

async def change_rating(prod_id, db): 
    """Изменяет рейтинг товара на актуальный по его id"""
    res_avg_grade = await db.scalars(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == prod_id,
            ReviewModel.is_active == True
        )
    )

    avg_grade = res_avg_grade.first()
    
    await db.execute(update(ProductModel)
               .where(
                ProductModel.id == prod_id, 
                ProductModel.is_active == True,
                )
                .values(
                    rating = float(f'{avg_grade:.2f}') if avg_grade else 0.00
                ))
    

@router.post('/', response_model=ReviewRespond)
async def create_review(review_data: ReviewCreate,
                       db: AsyncSession = Depends(get_async_db), 
                       current_user: UserModel = Depends(get_current_user),
                       ): 
    """
    Позволяет написать отзыв к товару, влияющий его на рейтинг. 
    Требует авторизации. """

    if not current_user.email: 
        raise HTTPException(status_code=403)
    
    user_res = await db.scalars(select(UserModel).where(UserModel.id == current_user.id))
    if not user_res.first(): 
        raise HTTPException(status_code=404)

    review_result = await db.scalars(select(ReviewModel).where(
        ReviewModel.product_id == review_data.product_id,
        ReviewModel.user_id == current_user.id,
        ReviewModel.is_active == True, 
        ))
    
    review = review_result.first()

    review_model = ReviewModel(**review_data.model_dump(), user_id=current_user.id)
    db.add(review_model)     


    await change_rating(prod_id=review_data.product_id, db=db)
    
    await db.commit()
    await db.refresh(review)

    return review

@router.delete('/{review_id}')
async def delete_review(review_id: int, 
                        db: AsyncSession = Depends(get_async_db), 
                        current_user: UserModel = Depends(get_current_admin)
                        ): 
    '''Выполняет мягкое удаление отзыва по review_id, устанавливая is_active = False. 
    После удаления пересчитывает рейтинг товара (rating в таблице products) на основе оставшихся активных отзывов.
    '''
    if current_user.role != 'admin': 
        raise HTTPException(status_code=403)
    
    res_review = await db.scalars(select(ReviewModel)
                                  .where(ReviewModel.id == review_id))
    review = res_review.first()

    if not review: 
        raise HTTPException(status_code=404)
    
    await db.execute(update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False))

    # res_product_id = await db.scalars(select(ProductModel)
    #                               .where(ProductModel.id == review.id)) 
    # product_id = res_product_id.first() 

    await change_rating(prod_id=review.product_id, db=db)
    await db.commit()
    
    return {"message": "Review deleted"}