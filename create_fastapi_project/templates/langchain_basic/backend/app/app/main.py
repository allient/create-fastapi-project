from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings
from app.templates.chat import chat_html
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("startup fastapi")
    yield
    # shutdown
    print("shutdown fastapi")


# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    # if oso.is_allowed(user, "read", message):
    return {"message": "Hello World"}


@app.get("/chat", response_class=HTMLResponse)
async def chat():
    if not settings.OPENAI_API_KEY.startswith("sk-"):
        raise HTTPException(
            status_code=500, detail="OPENAI_API_KEY is not set or not start with sk-"
        )

    return chat_html


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
