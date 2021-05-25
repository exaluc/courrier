from fastapi import APIRouter

from endpoints import index, mail, healthcheck, docs, redoc

theRouter = APIRouter()

theRouter.include_router(index.router)
theRouter.include_router(mail.router, prefix="/mail", tags=["send mail"])
theRouter.include_router(healthcheck.router, prefix="/healthcheck", tags=["health check"])
theRouter.include_router(docs.router, prefix="/docs", tags=["swagger doc"])
theRouter.include_router(redoc.router, prefix="/redoc", tags=["redoc doc"])
