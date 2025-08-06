from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import organization_repository
from app.repositories import activity_repository
from app.schemas.organization import OrganizationRead


async def get_organization_details(session: AsyncSession, org_id: int) -> OrganizationRead:
    """Получить информацию об организации по ID, вернуть в виде схемы."""
    org = await organization_repository.get_by_id(session, org_id)
    if not org:
        return None


    data = OrganizationRead.model_validate(org)
    if org.building:
        data.building_name = org.building.name
    if org.activity:
        data.activity_name = org.activity.name
    return data


async def search_organizations(session: AsyncSession, name: str = None, activity_id: int = None) -> List[
    OrganizationRead]:
    """
    Поиск организаций по названию или виду деятельности.
    Если указано name, выполняется поиск по названию (игнорируя регистр).
    Если указан activity_id, возвращаются организации указанной категории (с вложенными).
    При наличии обоих параметров можно комбинировать фильтры (например, имя внутри категории).
    """
    orgs = []
    if name:
        orgs = await organization_repository.list_by_name(session, name)
    if activity_id:
        orgs_by_activity = await activity_repository.list_by_activity(session, activity_id, include_nested=True)
        if name:

            activity_ids_set = {o.id for o in orgs_by_activity}
            orgs = [o for o in orgs if o.id in activity_ids_set]
        else:
            orgs = orgs_by_activity


    return [OrganizationRead.model_validate(o) for o in orgs]

async def search_organizations_by_location(session: AsyncSession,
                                           lat: float = None, lon: float = None, radius: float = None,
                                           lat_min: float = None, lat_max: float = None,
                                           lon_min: float = None, lon_max: float = None) -> List[OrganizationRead]:
    """Найти организации в радиусе от точки или в прямоугольной области."""
    orgs = []
    if lat is not None and lon is not None and radius is not None:
        orgs = await organization_repository.list_near_point(session, lat, lon, radius)
    elif None not in (lat_min, lat_max, lon_min, lon_max):
        orgs = await organization_repository.list_in_area(session, lat_min, lat_max, lon_min, lon_max)
    else:
        return []
    return [OrganizationRead.model_validate(o) for o in orgs]
