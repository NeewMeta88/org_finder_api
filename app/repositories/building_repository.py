from sqlalchemy.future import select
from app.models.organization import Organization

async def list_by_building(session, building_id: int):
    """Получить все организации в указанном здании."""
    result = await session.execute(
        select(Organization).where(Organization.building_id == building_id)
    )
    return result.scalars().all()