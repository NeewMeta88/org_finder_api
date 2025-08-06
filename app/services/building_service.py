from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import building_repository
from app.schemas.organization import OrganizationRead

async def list_organizations_by_building(session: AsyncSession, building_id: int) -> List[OrganizationRead]:
    """Вернуть список организаций в здании (список схем)."""
    orgs = await building_repository.list_by_building(session, building_id)
    return [OrganizationRead.model_validate(o) for o in orgs]