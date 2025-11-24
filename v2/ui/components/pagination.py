from aiogram.fsm.context import FSMContext

from v2.services.interfaces import IPageStateManager


class PageStateManager(IPageStateManager):
    """Менеджер состояния пагинации."""

    @staticmethod
    async def get_page(state: FSMContext, key: str, default: int = 1) -> int:
        """Получить номер страницы из состояния."""
        data = await state.get_data()
        return data.get(key, default)

    @staticmethod
    async def save_page(state: FSMContext, key: str, page: int) -> None:
        """Сохранить номер страницы в состояние."""
        data = await state.update_data({key: page})
        print("save page", data)

