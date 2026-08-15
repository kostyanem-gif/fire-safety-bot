# 🔥 Бот по пожарной безопасности

Telegram бот для ответов на вопросы по пожарной безопасности с использованием YandexGPT и RAG системы.

## 📋 Возможности

- ✅ Ответы на вопросы по пожарной безопасности
- ✅ Работа с PDF документами (RAG система)
- ✅ Интеграция с YandexGPT API
- ✅ Кнопки с частыми вопросами
- ✅ Экстренные номера
- ✅ Работает 24/7 на Render.com

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Загрузка PDF документов

Поместите ваши PDF документы по пожарной безопасности в папку `documents/`:

```bash
fire-safety-bot/
└── documents/
    ├── документ1.pdf
    ├── документ2.pdf
    └── ...
```

### 3. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и убедитесь что все значения правильные:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
YC_API_KEY=ваш_api_ключ_yandex_cloud
YC_FOLDER_ID=ваш_folder_id
YC_SERVICE_ACCOUNT_ID=ваш_service_account_id
YC_MODEL_URI=gpt://ваш_folder_id/yandexgpt-lite/latest
```

### 4. Запуск бота

```bash
python main.py
```

## 🌐 Деплой на Render.com

### Шаг 1: Создание аккаунта

1. Перейдите на https://render.com
2. Зарегистрируйтесь (можно через GitHub)

### Шаг 2: Создание сервиса

1. Нажмите **"New +"** → **"Web Service"**
2. Подключите ваш GitHub репозиторий с ботом
3. Настройте сервис:
   - **Name:** `fire-safety-bot`
   - **Region:** `Frankfurt` (ближе к России)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

### Шаг 3: Добавление переменных окружения

В разделе **"Environment"** добавьте:

```
TELEGRAM_BOT_TOKEN = 8878230117:AAFUgeUBJLkAWVPRekI1XVce7sjFkbqEAA4
YC_API_KEY = AQVN0C5Lpsmk89b7Z4VziHFPWJA5VzwsQK-tm-rT
YC_FOLDER_ID = b1g47ois806lr9o1sip
YC_SERVICE_ACCOUNT_ID = aje6k8j0t9mcdj1ifjjs7
YC_MODEL_URI = gpt://b1g47ois806lr9o1sip/yandexgpt-lite/latest
```

### Шаг 4: Загрузка PDF документов

**Вариант A: Через Git**
1. Добавьте PDF файлы в папку `documents/`
2. Закоммитьте и запушьте в репозиторий

**Вариант B: Через Render Dashboard**
1. Перейдите в консоль сервиса на Render
2. Используйте файловый менеджер для загрузки PDF

### Шаг 5: Запуск

Нажмите **"Create Web Service"** и дождитесь деплоя.

## 📱 Использование бота

### Команды:
- `/start` - Запустить бота
- `/help` - Помощь
- `/faq` - Частые вопросы
- `/emergency` - Экстренные номера
- `/about` - О боте
- `/status` - Статус системы

### Примеры вопросов:
- "Что делать при пожаре?"
- "Как пользоваться огнетушителем?"
- "Правила эвакуации из здания?"
- "Как часто проверять огнетушители?"

##  Структура проекта

```
fire-safety-bot/
├── main.py              # Основной файл бота
├── rag_engine.py        # RAG система для работы с PDF
── requirements.txt     # Зависимости Python
├── .env.example         # Шаблон переменных окружения
── .env                 # Переменные окружения (не коммитить!)
├── documents/           # Папка для PDF документов
── README.md           # Этот файл
```

## 🛠 Технологии

- **Python 3.10+**
- **python-telegram-bot** - Telegram Bot API
- **YandexGPT** - AI модель для генерации ответов
- **pdfplumber** - Извлечение текста из PDF
- **scikit-learn** - Векторизация и поиск
- **Render.com** - Хостинг

## 📝 Лицензия

MIT License

## 🤝 Поддержка

Если у вас есть вопросы или проблемы, создайте Issue в репозитории.

---

**Создано с ❤️ для безопасности людей**
