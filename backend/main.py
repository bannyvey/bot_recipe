import logging
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from backend.api import api_router
from backend.models.category_model import CategoryModel
from backend.models.recipe_model import RecipeModel
from backend.models.user_model import UserModel
from config import settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def run_migrations():
    root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(root / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(root / "backend" / "migrations"))
    alembic_cfg.attributes['configure_logger'] = False
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    yield


app = FastAPI(lifespan=lifespan, debug=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(
    app,
    host=settings.host,
    port=settings.port,
)
