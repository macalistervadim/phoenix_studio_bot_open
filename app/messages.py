import os

START_MESSAGE = f"""
👋 <b>Приветствуем тебя в нашей студии!</b>

♻️ Наши ресурсы:

<b>Группа ВК:</b> {os.getenv("VK_GROUP_URL", "https://vk.com/phoenixstudio_off")}
<b>Телеграм канал:</b> {os.getenv("TG_CHANNEL_URL", "https://t.me/pwebstudio")}
<b>Беседа клиентов:</b> {os.getenv("TG_CHAT_URL", "https://t.me/+dORLMnQCEO0xMTBi")}
<b>Сайт:</b> в разработке

Подписывайся на паблик ВКонтакте и вступай в наш телеграм канал чтобы не пропустить важные новости
"""

CONTACTS_MESSAGE = f"""
♻️ Наши ресурсы:

<b>Группа ВК:</b> {os.getenv("VK_GROUP_URL", "https://vk.com/phoenixstudio_off")}
<b>Телеграм канал:</b> {os.getenv("TG_CHANNEL_URL", "https://t.me/pwebstudio")}
<b>Беседа клиентов:</b> {os.getenv("TG_CHAT_URL", "https://t.me/+dORLMnQCEO0xMTBi")}
<b>Сайт:</b> в разработке

Не забывай проставлять уведомления в наших пабликах чтобы не пропустить новую важную информацию!
"""

SUBSCRIPTION_MESSAGE = f"""
✅ <b>Перед использованием нашего бота, необходимо подписаться на наш канал</b>

Канал: {os.getenv("TG_CHANNEL_URL", "https://t.me/pwebstudio")}

После того, как вы подпишитесь - не забудьте нажать кнопку <b>"✅ Подписался"</b>, чтобы продолжить общение с ботом
"""

SUBSCRIPTION_SUCC_MESSAGE = """
🔓 <b>Подписка проверена, можете продолжать пользоваться ботом</b>

Также не забывайте включать уведомления в канале, ведь там часто выходят важные новости и готовые проекты

💚 <i>С любовью, команда PHOENIX STUDIO</i>
"""
