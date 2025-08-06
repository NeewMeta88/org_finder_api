import asyncio
from app.core.database import AsyncSessionLocal, engine
from app.models import building, activity, organization

async def seed():
    async with AsyncSessionLocal() as session:

        b1 = building.Building(name="Бизнес-центр Альфа", address="ул. Ленина, 1", latitude=55.75, longitude=37.61)
        b2 = building.Building(name="ТЦ Бета", address="пр. Мира, 5", latitude=55.76, longitude=37.64)
        session.add_all([b1, b2])
        await session.flush()


        activity_it = activity.Activity(name="IT", parent_id=None)
        activity_dev = activity.Activity(name="Разработка ПО", parent=activity_it)
        activity_web = activity.Activity(name="Веб-разработка", parent=activity_dev)
        activity_consult = activity.Activity(name="Консалтинг", parent_id=None)
        session.add_all([activity_it, activity_dev, activity_web, activity_consult])
        await session.flush()

        org1 = organization.Organization(name="АльфаСофт", address="ул. Ленина, 1, оф.101", building=b1, activity=activity_web, latitude=55.7501, longitude=37.6101)
        org2 = organization.Organization(name="БетаКонсалт", address="пр. Мира, 5, оф.303", building=b2, activity=activity_consult, latitude=55.7605, longitude=37.6402)
        org3 = organization.Organization(name="GammaDev", address="ул. Ленина, 1, оф.202", building=b1, activity=activity_dev, latitude=55.7502, longitude=37.6102)
        org4 = organization.Organization(name="DeltaWeb", address="ул. Ленина, 1, оф.203", building=b1, activity=activity_web, latitude=55.7503, longitude=37.6099)

        session.add_all([org1, org2, org3, org4])


        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())