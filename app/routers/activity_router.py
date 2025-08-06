from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.services import activity_service

router = APIRouter(
    prefix="/activities",
    tags=["activities"],
)


@router.get("/{activity_id}/organizations", response_model=list[activity_service.OrganizationRead])
async def list_organizations_by_activity(
        activity_id: int = Path(..., description="ID вида деятельности"),
        session: AsyncSession = Depends(get_db_session)
):
    """
    Получить список организаций по указанному виду деятельности.
    Включает организации подчиненных (вложенных) категорий до 3 уровня.
    """
    orgs = await activity_service.list_organizations_by_activity(session, activity_id)
    return orgs
