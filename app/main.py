import uvicorn
from fastapi import FastAPI, Depends

from app.core import security
from app.routers import organization_router, building_router, activity_router

app = FastAPI(
    title="Organizations Directory API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    dependencies=[Depends(security.verify_api_key)]
)

app.include_router(organization_router.router)
app.include_router(building_router.router)
app.include_router(activity_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
