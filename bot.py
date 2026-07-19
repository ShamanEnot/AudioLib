import logging
import os
import asyncio
import httpx
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

# Функция-будильник, которая не дает боту уснуть
async def keep_alive():
    await asyncio.sleep(30)  # Даем боту 30 секунд на запуск при старте
    while True:
        try:
            # ⚠️ ОБЯЗАТЕЛЬНО ЗАМЕНИТЕ ЭТУ ССЫЛКУ НА СВОЮ ИЗ ПАНЕЛИ RENDER!
            url = "https://onrender.com" 
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            logger.info(f"⏰ Будильник сработал. Статус ответа сервера: {response.status_code}")
        except Exception as e:
            logger.warning(f"⏰ Ошибка самопинга: {e}")
        
        await asyncio.sleep(600)  # Повторяем пинг каждые 10 минут (600 секунд)

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
    
    # Запускаем фоновую задачу будильника параллельно с ботом
    app.job_queue.run_once(lambda context: asyncio.create_task(keep_alive()), when=0)
    
    logger.info("Бот запущен и ждёт заявки...")
    app.run_polling(allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    main()