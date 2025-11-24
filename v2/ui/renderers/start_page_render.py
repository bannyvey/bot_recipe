from aiogram.types import Message

from v2.services.interfaces import (IUserService, IUserRender, IRecipeKeyboardBuilder, IRecipeFormatter,
                                    IMessageSender)


class UserRender(IUserRender):
    def __init__(
            self,
            user_service: IUserService,
            formatter: IRecipeFormatter,
            keyboard_builder: IRecipeKeyboardBuilder,
            sender: IMessageSender,
            user_builder
    ):
        self.user_service = user_service
        self.formatter = formatter
        self.keyboard_builder = keyboard_builder
        self.send = sender
        self.user_builder = user_builder

    async def user_registration(self, message: Message, is_admin: bool):
        user_dto = self.user_builder.build_from_message(message)
        await self.user_service.register_user(user_dto)
        text = self.formatter.format_welcome_message()
        keyboard = self.keyboard_builder.build_main_menu_keyboard(message, is_admin)
        await self.send.send_page(message, text, keyboard)



