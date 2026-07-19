import logging
import os
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    await context.bot.approve_chat_join_request(
        chat_id=chat.id,
        user_id=user.id
    )
    logger.info(f"Одобрен: {user.full_name} (@{user.username}) → {chat.title}")

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                "✅ Заявка одобрена!\n\n"
                "🎧 Добро пожаловать в архив Audio.Lib!\n"
                "Здесь собраны аудиокниги по жанрам:\n"
                "Фантастика · Фэнтези · LitRPG · Попаданцы · Этногенез и многое другое\n\n"
                "📚 Приятного прослушивания!"
            )
        )
    except Exception as e:
        logger.warning(f"Не удалось отправить приветствие {user.full_name}: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(approve_join_request))
    logger.info("Бот запущен и ждёт заявки...")
    app.run_polling(allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    main()