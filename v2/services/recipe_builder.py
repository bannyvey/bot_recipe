from v2.schemas.recipe_dto import RecipeReview, RecipeCreate, RecipeUpdate


class RecipeBuilder:
    """Отвечает только за сборку DTO из FSM state"""

    @staticmethod
    async def build_for_view(state):
        """Собирает валидированный DTO из state"""
        data = await state.get_data()
        return RecipeReview.model_validate(data)

    @staticmethod
    async def build_for_create(state, telegram_id: int):
        await state.update_data(telegram_id=telegram_id)
        data = await state.get_data()
        return RecipeCreate.model_validate(data)

    @staticmethod
    async def build_for_update_status(*, admin_approved: bool | None = None, user_approved: bool | None = None):
        return RecipeUpdate(
            admin_approved=admin_approved,
            user_approved=user_approved
        )
