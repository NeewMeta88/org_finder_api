from sqlalchemy.future import select
from app.models.organization import Organization
from app.models.activity import Activity


async def list_by_activity(session, activity_id: int, include_nested: bool = True):
    """
    Получить организации по виду деятельности.
    Если include_nested=True, включает организации из дочерних категорий (до 3 уровней).
    """
    if not include_nested:
        result = await session.execute(
            select(Organization).where(Organization.activity_id == activity_id)
        )
        return result.scalars().all()


    activity_ids = {activity_id}

    result1 = await session.execute(select(Activity.id).where(Activity.parent_id == activity_id))
    level1_ids = set(result1.scalars().all())
    activity_ids |= level1_ids
    if level1_ids:

        result2 = await session.execute(select(Activity.id).where(Activity.parent_id.in_(level1_ids)))
        level2_ids = set(result2.scalars().all())
        activity_ids |= level2_ids
        if level2_ids:

            result3 = await session.execute(select(Activity.id).where(Activity.parent_id.in_(level2_ids)))
            level3_ids = set(result3.scalars().all())
            activity_ids |= level3_ids

    result = await session.execute(select(Organization).where(Organization.activity_id.in_(activity_ids)))
    return result.scalars().all()
