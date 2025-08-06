import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import get_db_session
import app.services.activity_service as activity_service
import app.services.building_service as building_service
import app.services.organization_service as organization_service

@pytest.mark.asyncio
async def test_search_organizations_by_activity_with_api_key(monkeypatch):
    sample = {
        "name": "БетаКонсалт",
        "address": "пр. Мира, 5, оф.303",
        "latitude": 55.7605,
        "longitude": 37.6402,
        "building_id": 2,
        "activity_id": 2,
        "id": 2,
        "building_name": None,
        "activity_name": None
    }
    async def fake_search(session, name, activity_id):

        assert name is None
        assert activity_id == 2
        return [sample]
    monkeypatch.setattr(organization_service, "search_organizations", fake_search)

    headers = {"X-API-KEY": "SUPERSECRET123"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=headers,
        follow_redirects=True
    ) as ac:
        response = await ac.get("/organizations/", params={"activity_id": 2})
    assert response.status_code == 200
    assert response.json() == [sample]

@pytest.mark.asyncio
async def test_search_organizations_radius_with_api_key(monkeypatch):
    sample = {
        "name": "БетаКонсалт",
        "address": "пр. Мира, 5, оф.303",
        "latitude": 55.7605,
        "longitude": 37.6402,
        "building_id": 2,
        "activity_id": 2,
        "id": 2,
        "building_name": None,
        "activity_name": None
    }
    async def fake_search_loc(session, lat, lon, radius, lat_min, lat_max, lon_min, lon_max):
        assert lat == 55.7605
        assert lon == 37.6402
        assert radius == 1.0

        assert lat_min is None and lat_max is None and lon_min is None and lon_max is None
        return [sample]
    monkeypatch.setattr(organization_service, "search_organizations_by_location", fake_search_loc)

    headers = {"X-API-KEY": "SUPERSECRET123"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=headers,
        follow_redirects=True
    ) as ac:
        response = await ac.get(
            "/organizations/search",
            params={"lat": 55.7605, "lon": 37.6402, "radius": 1}
        )
    assert response.status_code == 200
    assert response.json() == [sample]

@pytest.mark.asyncio
async def test_get_organization_by_id_with_api_key(monkeypatch):
    sample = {
        "name": "АльфаСофт",
        "address": "ул. Ленина, 1, оф.101",
        "latitude": 55.7501,
        "longitude": 37.6101,
        "building_id": 1,
        "activity_id": 4,
        "id": 1,
        "building_name": "Бизнес-центр Альфа",
        "activity_name": "Веб-разработка"
    }
    async def fake_get(session, organization_id):
        assert organization_id == 1
        return sample
    monkeypatch.setattr(organization_service, "get_organization_details", fake_get)

    headers = {"X-API-KEY": "SUPERSECRET123"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=headers,
        follow_redirects=True
    ) as ac:
        response = await ac.get("/organizations/1")
    assert response.status_code == 200
    assert response.json() == sample

@pytest.mark.asyncio
async def test_list_organizations_in_building_with_api_key(monkeypatch):
    sample = {
        "name": "БетаКонсалт",
        "address": "пр. Мира, 5, оф.303",
        "latitude": 55.7605,
        "longitude": 37.6402,
        "building_id": 2,
        "activity_id": 2,
        "id": 2,
        "building_name": None,
        "activity_name": None
    }
    async def fake_list(session, building_id):
        assert building_id == 2
        return [sample]
    monkeypatch.setattr(building_service, "list_organizations_by_building", fake_list)

    headers = {"X-API-KEY": "SUPERSECRET123"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=headers,
        follow_redirects=True
    ) as ac:
        response = await ac.get("/buildings/2/organizations")
    assert response.status_code == 200
    assert response.json() == [sample]

@pytest.mark.asyncio
async def test_list_organizations_by_activity_with_api_key_for_multiple(monkeypatch):
    samples = [
        {
            "name": "АльфаСофт",
            "address": "ул. Ленина, 1, оф.101",
            "latitude": 55.7501,
            "longitude": 37.6101,
            "building_id": 1,
            "activity_id": 4,
            "id": 1,
            "building_name": None,
            "activity_name": None
        },
        {
            "name": "DeltaWeb",
            "address": "ул. Ленина, 1, оф.203",
            "latitude": 55.7503,
            "longitude": 37.6099,
            "building_id": 1,
            "activity_id": 4,
            "id": 4,
            "building_name": None,
            "activity_name": None
        }
    ]
    async def fake_list(session, activity_id):
        assert activity_id == 4
        return samples
    monkeypatch.setattr(activity_service, "list_organizations_by_activity", fake_list)

    headers = {"X-API-KEY": "SUPERSECRET123"}
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers=headers,
        follow_redirects=True
    ) as ac:
        response = await ac.get("/activities/4/organizations")
    assert response.status_code == 200
    assert response.json() == samples

@pytest.mark.asyncio
async def test_unauthorized_requests(monkeypatch):
    """
    Проверяем, что без передачи X-API-KEY все конечные точки возвращают 422 Unprocessable Entity.
    """


    async def unreachable(*args, **kwargs):
        pytest.fail("Сервис не должен быть вызван при отсутствии авторизации")

    monkeypatch.setattr(organization_service, "search_organizations", unreachable)
    monkeypatch.setattr(organization_service, "search_organizations_by_location", unreachable)
    monkeypatch.setattr(organization_service, "get_organization_details", unreachable)
    monkeypatch.setattr(building_service, "list_organizations_by_building", unreachable)
    monkeypatch.setattr(activity_service, "list_organizations_by_activity", unreachable)

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        follow_redirects=True
    ) as ac:
        endpoints = [
            ("/organizations/", {"activity_id": 2}),
            ("/organizations/search", {"lat": 55.7605, "lon": 37.6402, "radius": 1}),
            ("/organizations/1", {}),
            ("/buildings/2/organizations", {}),
            ("/activities/4/organizations", {}),
        ]
        for path, params in endpoints:
            response = await ac.get(path, params=params)
            assert response.status_code == 422