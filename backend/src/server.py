from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.routes import appointment_route
from src.exception import DomainException
from src.routes import user_route, client_route, pet_route

app = FastAPI()

ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(DomainException)
async def handle_exception(req: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
        },
        headers=exc.header
    )
    
app.include_router(user_route.router)
app.include_router(client_route.router)
app.include_router(pet_route.router)
app.include_router(appointment_route.router)

@app.get("/")
async def get_root():
    return {
        "ok": True
    }