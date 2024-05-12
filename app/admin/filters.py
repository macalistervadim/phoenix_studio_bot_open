import aiogram


class IsAdmin(aiogram.filters.BaseFilter):
    def __init__(self, admin_id):
        self.admin_ids = admin_id

    async def __call__(self, message: aiogram.types.Message):
        return str(message.from_user.id) in self.admin_ids
