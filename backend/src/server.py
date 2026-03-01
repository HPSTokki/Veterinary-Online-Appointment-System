from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exception import DomainException
from src.routes import user_route, client_route

app = FastAPI()

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

@app.get("/")
async def get_root():
    return {
        "ok": True
    }