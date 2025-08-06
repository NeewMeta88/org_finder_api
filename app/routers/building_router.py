from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.services import building_service

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
)


@router.get("/{building_id}/organizations", response_model=list[building_service.OrganizationRead])
async def list_organizations_in_building(
        building_id: int = Path(..., description="ID здания"),
        session: AsyncSession = Depends(get_db_session)
):
    """Получить список всех организаций, находящихся в данном здании."""
    orgs = await building_service.list_organizations_by_building(session, building_id)
    return orgs
