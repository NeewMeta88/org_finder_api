from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.services import organization_service

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


@router.get("/", response_model=list[organization_service.OrganizationRead])
async def search_organizations(
        name: str = Query(None, description="Подстрока для поиска по названию организации"),
        activity_id: int = Query(None, description="ID вида деятельности для фильтра"),
        session: AsyncSession = Depends(get_db_session)
):
    """
    Получить список организаций, отфильтрованных по названию и/или виду деятельности.
    Если параметры не заданы, вернется пустой список или все организации (в зависимости от реализации сервиса).
    """
    orgs = await organization_service.search_organizations(session, name=name, activity_id=activity_id)
    return orgs


@router.get("/search", response_model=list[organization_service.OrganizationRead])
async def search_orgs_by_location(
        lat: float = Query(None, description="Широта центральной точки"),
        lon: float = Query(None, description="Долгота центральной точки"),
        radius: float = Query(None, description="Радиус поиска в км"),
        lat_min: float = Query(None, description="Минимальная широта области"),
        lat_max: float = Query(None, description="Максимальная широта области"),
        lon_min: float = Query(None, description="Минимальная долгота области"),
        lon_max: float = Query(None, description="Максимальная долгота области"),
        session: AsyncSession = Depends(get_db_session)
):
    """
    Найти организации по географическому положению.
    Можно указать либо центр и радиус (lat, lon, radius), либо прямоугольную область (lat_min, lat_max, lon_min, lon_max).
    """
    orgs = await organization_service.search_organizations_by_location(
        session, lat=lat, lon=lon, radius=radius,
        lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max
    )
    return orgs


@router.get("/{organization_id}", response_model=organization_service.OrganizationRead)
async def get_organization_by_id(
        organization_id: int = Path(..., description="ID организации"),
        session: AsyncSession = Depends(get_db_session)
):
    """Получить подробную информацию об организации по её ID."""
    org = await organization_service.get_organization_details(session, organization_id)
    if not org:

        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
