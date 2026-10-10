#!/usr/bin/env python3

import asyncio
from app.core.database import AsyncSessionLocal
from app.models.category import Category
from sqlalchemy import select

async def seed_uncategorized():
    async with AsyncSessionLocal() as session:
        # Check if Uncategorized category already exists
        result = await session.execute(select(Category).where(Category.name == 'Uncategorized'))
        existing_category = result.scalar_one_or_none()

        if existing_category:
            print(f'Uncategorized category already exists: id={existing_category.id}, name={existing_category.name}')
            return existing_category

        # Create Uncategorized category
        uncategorized_category = Category(name='Uncategorized')
        session.add(uncategorized_category)
        await session.commit()
        await session.refresh(uncategorized_category)

        print(f'Created Uncategorized category: id={uncategorized_category.id}, name={uncategorized_category.name}')
        return uncategorized_category

if __name__ == '__main__':
    asyncio.run(seed_uncategorized())
