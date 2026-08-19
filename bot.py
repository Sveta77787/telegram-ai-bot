import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import g4f

# Токен от BotFather. Берётся из переменной окружения TELEGRAM_BOT_TOKEN,
# чтобы не хранить секрет в коде.
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот с ИИ. Напиши мне что-нибудь, и я отвечу с помощью искусственного интеллекта!")

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения от пользователя
    user_message = update.message.text
    
    # Отправляем запрос в g4f
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",  # Попробуем эту модель
            messages=[{"role": "user", "content": user_message}]
        )
        # Отправляем ответ пользователю
        await update.message.reply_text(response)
    except Exception as e:
        # Если что-то пошло не так, отправляем сообщение об ошибке
        await update.message.reply_text(f"Ошибка: {str(e)}")

# Основная функция для запуска бота
if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "Не задана переменная окружения TELEGRAM_BOT_TOKEN. "
            "Получите токен у @BotFather и укажите его, например: "
            "export TELEGRAM_BOT_TOKEN='...'"
        )

    # Создаём приложение
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Отладочный вывод
    print("Бот запущен и готов к работе!")
    
    # Запускаем бота
    app.run_polling()
