Telegram бот для учёта личных расходов и ведения бюджета.

Для запуска бота в переменных окружения надо подставить API токен бота и ID телеграм аккаунта.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируютя)

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile, а также в команде запуска укажите локальную директорию с проектом вместо `Project_telegram_finance_bot`. SQLite база данных будет лежать в папке проекта `db/finance_bot.db`.

```
docker build -t tgfinancebot ./
docker run -d --name tg -v /Project_telegram_finance_bot/db:/home/db tgfinancebot
```

Чтобы войти в работающий контейнер:

```
docker exec -ti tg bash
```

Войти в контейнере в SQL шелл:

```
docker exec -ti tg bash
sqlite3 /home/db/finance_bot.db
```

Проект выполнен на:
* Python - используемый язык.
* Sqlite - используемая база данных.
* Aiogram - фреймворк для [Telegram Bot API.](https://core.telegram.org/bots/api)
* Docker - для развёртывания бота.


