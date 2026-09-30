from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import Base
from app.deps import engine
from app.features.alerts.router import router as alerts_router
from app.features.identity.router import router as identity_router
from app.features.probes.router import router as probes_router
from app.features.routing.router import router as routing_router
from app.features.status.router import router as status_router
from app.kernel.errors import DomainError
app = FastAPI(title="Failover Pulse", version="0.1.0", redirect_slashes=False)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
@app.exception_handler(DomainError)
async def domain_error(_, exc: DomainError):
    return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.status)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(identity_router)
app.include_router(probes_router)
app.include_router(routing_router)
app.include_router(alerts_router)
app.include_router(status_router)
