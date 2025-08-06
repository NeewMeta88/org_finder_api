from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.organization import Organization


async def get_by_id(session, org_id: int):
    """Получить организацию по ID, включая связанное здание и вид деятельности."""
    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building), selectinload(Organization.activity))
        .where(Organization.id == org_id)
    )
    return result.scalar_one_or_none()


async def list_by_name(session, name_query: str):
    """Найти организации по подстроке в названии (case-insensitive)."""
    query = select(Organization).where(Organization.name.ilike(f"%{name_query}%"))
    result = await session.execute(query)
    return result.scalars().all()


async def list_in_area(session, lat_min: float, lat_max: float, lon_min: float, lon_max: float):
    """Найти организации, попадающие в прямоугольную область по координатам."""
    result = await session.execute(
        select(Organization).where(
            Organization.latitude.between(lat_min, lat_max),
            Organization.longitude.between(lon_min, lon_max)
        )
    )
    return result.scalars().all()


async def list_near_point(session, lat: float, lon: float, radius_km: float):
    """
    Найти организации в заданном радиусе (км) от точки (lat, lon).
    Предполагается, что координаты в градусах, используется приближенный расчет по формуле haversine.
    """


    deg_lat = radius_km / 111.0
    deg_lon = radius_km / 111.0
    lat_min = lat - deg_lat
    lat_max = lat + deg_lat
    lon_min = lon - deg_lon
    lon_max = lon + deg_lon

    result = await session.execute(
        select(Organization).where(
            Organization.latitude.between(lat_min, lat_max),
            Organization.longitude.between(lon_min, lon_max)
        )
    )
    candidates = result.scalars().all()

    orgs_in_radius = []
    import math
    for org in candidates:
        if org.latitude is None or org.longitude is None:
            continue

        dlat = math.radians(org.latitude - lat)
        dlon = math.radians(org.longitude - lon)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat)) * math.cos(math.radians(org.latitude)) * math.sin(
            dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = 6371 * c
        if distance <= radius_km:
            orgs_in_radius.append(org)
    return orgs_in_radius
