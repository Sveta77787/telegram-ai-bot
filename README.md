# telegram-ai-bot

Телеграм-бот, который отвечает на сообщения с помощью ИИ (через `g4f`).

## Настройка

Токен бота в коде не хранится — он читается из переменной окружения
`TELEGRAM_BOT_TOKEN`.

1. Получите токен у [@BotFather](https://t.me/BotFather).
2. Задайте переменную окружения:

   ```bash
   export TELEGRAM_BOT_TOKEN='ваш_токен'
   ```

   Либо скопируйте `.env.example` в `.env`, впишите туда токен и подгрузите его
   перед запуском (`set -a && . ./.env && set +a`).

3. На Render (и других хостингах) добавьте `TELEGRAM_BOT_TOKEN` в настройки
   Environment Variables сервиса.

## Запуск

```bash
pip install -r requirements.txt
python bot.py
```

Без заданной переменной `TELEGRAM_BOT_TOKEN` бот завершится с понятной ошибкой.
