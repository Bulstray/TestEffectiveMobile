import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api import router as api_router
from app_lifespan import lifespan
from core.config import settings

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    error = exc.errors()[0].get("msg")
    return JSONResponse(
        content={"detail": error},
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
    )
