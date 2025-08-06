import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.activity_service as activity_service
import app.services.building_service as building_service
import app.services.organization_service as organization_service
from app.repositories import activity_repository, building_repository, organization_repository
from app.schemas.organization import OrganizationRead

class DummyOrg:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.building = None
        self.activity = None

@pytest.mark.asyncio
async def test_list_organizations_by_activity(monkeypatch):
    dummy = DummyOrg(
        id=5, name="OrgA", address="Addr A", latitude=10.0, longitude=20.0,
        building_id=2, activity_id=3
    )
    async def fake_list_by_activity(session, activity_id, include_nested):
        assert isinstance(session, AsyncSession) or session is None
        assert activity_id == 3
        assert include_nested is True
        return [dummy]

    monkeypatch.setattr(activity_repository, "list_by_activity", fake_list_by_activity)
    result = await activity_service.list_organizations_by_activity(None, 3)

    assert isinstance(result, list)
    assert len(result) == 1
    org = result[0]
    assert isinstance(org, OrganizationRead)
    assert org.id == 5
    assert org.name == "OrgA"

@pytest.mark.asyncio
async def test_list_organizations_by_building(monkeypatch):
    dummy = DummyOrg(
        id=7, name="OrgB", address="Addr B", latitude=11.1, longitude=22.2,
        building_id=4, activity_id=6
    )
    async def fake_list_by_building(session, building_id):
        assert building_id == 4
        return [dummy]

    monkeypatch.setattr(building_repository, "list_by_building", fake_list_by_building)
    result = await building_service.list_organizations_by_building(None, 4)

    assert isinstance(result, list)
    assert len(result) == 1
    org = result[0]
    assert org.building_id == 4
    assert org.id == 7

@pytest.mark.asyncio
async def test_get_organization_details_with_relations(monkeypatch):
    dummy = DummyOrg(
        id=9, name="OrgC", address="Addr C", latitude=12.2, longitude=23.3,
        building_id=5, activity_id=8
    )

    dummy.building = DummyOrg(name="BuildingX")
    dummy.activity = DummyOrg(name="ActivityY")

    async def fake_get_by_id(session, org_id):
        assert org_id == 9
        return dummy

    monkeypatch.setattr(organization_repository, "get_by_id", fake_get_by_id)
    result = await organization_service.get_organization_details(None, 9)

    assert isinstance(result, OrganizationRead)
    assert result.id == 9
    assert result.building_name == "BuildingX"
    assert result.activity_name == "ActivityY"

@pytest.mark.asyncio
async def test_search_organizations_filters(monkeypatch):

    a = DummyOrg(id=1, name="Alpha", address="A", latitude=0, longitude=0, building_id=1, activity_id=1)
    b = DummyOrg(id=2, name="Beta", address="B", latitude=0, longitude=0, building_id=1, activity_id=2)

    async def fake_list_by_name(session, name):
        assert name.lower() == "alpha"
        return [a]

    async def fake_list_by_activity(session, activity_id, include_nested):
        assert activity_id == 2
        assert include_nested is True
        return [b]

    monkeypatch.setattr(organization_repository, "list_by_name", fake_list_by_name)
    monkeypatch.setattr(activity_repository, "list_by_activity", fake_list_by_activity)

    res_name = await organization_service.search_organizations(None, name="Alpha")
    assert len(res_name) == 1 and res_name[0].id == 1

    res_act = await organization_service.search_organizations(None, activity_id=2)
    assert len(res_act) == 1 and res_act[0].id == 2

    res_both = await organization_service.search_organizations(None, name="Alpha", activity_id=2)
    assert res_both == []

@pytest.mark.asyncio
async def test_search_organizations_by_location_radius_and_bbox(monkeypatch):
    dummy_point = DummyOrg(id=3, name="PointOrg", address="P", latitude=1, longitude=1, building_id=0, activity_id=0)
    dummy_area = DummyOrg(id=4, name="AreaOrg", address="Q", latitude=2, longitude=2, building_id=0, activity_id=0)

    async def fake_near_point(session, lat, lon, radius):
        assert lat == 1.0
        assert lon == 1.0
        assert radius == 5.0
        return [dummy_point]

    async def fake_in_area(session, lat_min, lat_max, lon_min, lon_max):
        assert lat_min == 0.0
        assert lat_max == 3.0
        assert lon_min == 0.0
        assert lon_max == 3.0
        return [dummy_area]

    monkeypatch.setattr(organization_repository, "list_near_point", fake_near_point)
    monkeypatch.setattr(organization_repository, "list_in_area", fake_in_area)

    res_point = await organization_service.search_organizations_by_location(None, lat=1.0, lon=1.0, radius=5.0)
    assert len(res_point) == 1 and res_point[0].id == 3

    res_area = await organization_service.search_organizations_by_location(
        None, lat_min=0.0, lat_max=3.0, lon_min=0.0, lon_max=3.0
    )
    assert len(res_area) == 1 and res_area[0].id == 4
