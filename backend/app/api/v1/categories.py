from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.api.deps import get_db
from app.models.category import Category
from app.models.keyword import Keyword
from app.schemas.category import CategoryCreate, CategoryRead, KeywordCreate, KeywordRead

router = APIRouter()


@router.get('', response_model=List[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.id))
    return result.scalars().all()


@router.post('', response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Category).where(Category.name == category_in.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Category already exists')
    category = Category(name=category_in.name)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    if category.name == 'Uncategorized':
        raise HTTPException(status_code=400, detail='Cannot delete Uncategorized category')
    await db.delete(category)
    await db.commit()


@router.get('/{category_id}/keywords', response_model=List[KeywordRead])
async def list_keywords(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    result = await db.execute(select(Keyword).where(Keyword.category_id == category_id))
    return result.scalars().all()


@router.post('/{category_id}/keywords', response_model=KeywordRead, status_code=status.HTTP_201_CREATED)
async def add_keyword(category_id: int, keyword_in: KeywordCreate, db: AsyncSession = Depends(get_db)):
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    existing = await db.execute(
        select(Keyword).where(
            Keyword.category_id == category_id,
            func.lower(Keyword.keyword) == keyword_in.keyword.lower()
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Keyword already exists for this category')
    keyword = Keyword(category_id=category_id, keyword=keyword_in.keyword.strip())
    db.add(keyword)
    await db.commit()
    await db.refresh(keyword)
    return keyword
