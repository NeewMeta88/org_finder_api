from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import activity_repository
from app.schemas.organization import OrganizationRead

async def list_organizations_by_activity(session: AsyncSession, activity_id: int) -> List[OrganizationRead]:
    """Вернуть список организаций для данного вида деятельности (включая вложенные подкатегории)."""
    orgs = await activity_repository.list_by_activity(session, activity_id, include_nested=True)
    return [OrganizationRead.model_validate(o) for o in orgs]