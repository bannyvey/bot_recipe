from aiogram import Router

from .admin.admin_handler import admin_router
from .recipes.create_recipe_handler import create_router
from .recipes.detail_recipe_handler import detail_router
from .recipes.main_menu_handler import menu
from .recipes.my_recipes_handler import my_recipes_router
from .recipes.pagination_page_handler import page_router
from .start import start_router
from v2.handlers.recipes.recipe_handler import router as recipe_router



router = Router()

router.include_router(start_router)
router.include_router(recipe_router)
router.include_router(detail_router)
router.include_router(create_router)
router.include_router(my_recipes_router)
router.include_router(page_router)
router.include_router(menu)
router.include_router(admin_router)