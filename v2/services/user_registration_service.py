from v2.services.interfaces import IApi, IUserRegistrationService


class UserRegistrationService():
    def __init__(self, api_client: IApi):
        self.api_client = api_client

    async def register_user(self):
        """Зарегистрировать пользователя из сообщения."""
        pass