"""
Telegram бот для ответов по пожарной безопасности
Использует YandexGPT API и RAG систему
"""
import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
YC_API_KEY = os.getenv('YC_API_KEY')
YC_FOLDER_ID = os.getenv('YC_FOLDER_ID')
YC_MODEL_URI = os.getenv('YC_MODEL_URI', f'gpt://{YC_FOLDER_ID}/yandexgpt-lite/latest')

# Импортируем RAG движок
from rag_engine import rag_engine

# Системный промпт для бота
SYSTEM_PROMPT = """Ты - эксперт по пожарной безопасности. Твоя задача - помогать людям 
с вопросами о пожарной безопасности, используя информацию из предоставленных документов.

Правила:
1. Отвечай только на вопросы, связанные с пожарной безопасностью
2. Используй информацию из контекста для ответов
3. Если информации недостаточно в контексте, скажи об этом честно
4. Отвечай на русском языке
5. Будь краток и конкретен
6. Если вопрос не по теме пожарной безопасности, вежливо откажи в ответе"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
🔥 *Добро пожаловать в бота по пожарной безопасности!*

Я помогу вам найти информацию о:
• Правилах пожарной безопасности
• Действиях при пожаре
• Использовании огнетушителей
• Эвакуации и спасении
• Профилактике пожаров

*Как пользоваться:*
Просто задайте вопрос, и я найду ответ в базе знаний!

*Примеры вопросов:*
• Что делать при пожаре?
• Как пользоваться огнетушителем?
• Правила эвакуации из здания?
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Частые вопросы", callback_data='faq')],
        [InlineKeyboardButton("🆘 Экстренные номера", callback_data='emergency')],
        [InlineKeyboardButton("ℹ️ О боте", callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
*Помощь по использованию бота*

*Команды:*
/start - Запустить бота
/help - Показать помощь
/faq - Частые вопросы
/status - Статус системы

*Как задать вопрос:*
Просто напишите ваш вопрос текстом, например:
• "Что делать при возгорании электропроводки?"
• "Как часто нужно проверять огнетушители?"
• "Правила эвакуации из офиса?"

*Важно:*
Бот отвечает только на вопросы по пожарной безопасности.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать частые вопросы"""
    faq_text = """
*Частые вопросы по пожарной безопасности:*

1️⃣ *Что делать при обнаружении пожара?*
- Немедленно сообщите в пожарную охрану (101 или 112)
- Оповестите людей о пожаре
- Приступите к эвакуации
- При возможности ликвидируйте возгорание

2️⃣ *Как пользоваться огнетушителем?*
- Сорвите пломбу и выдерните чеку
- Направьте раструб на очаг пожара
- Нажмите на рычаг
- Тушите с расстояния 3-4 метра

3️⃣ *Правила эвакуации:*
- Двигайтесь к ближайшему выходу
- Не пользуйтесь лифтами
- При задымлении - двигайтесь ползком
- Помогите детям и пожилым людям

4️⃣ *Профилактика пожаров:*
- Не оставляйте электроприборы без присмотра
- Не перегружайте электросеть
- Храните легковоспламеняющиеся вещества отдельно
- Проверяйте исправность проводки
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(faq_text, parse_mode='Markdown', reply_markup=reply_markup)


async def emergency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Экстренные номера"""
    emergency_text = """
 *ЭКСТРЕННЫЕ НОМЕРА*

🔥 *Пожарная охрана:* 101
 *Единый номер:* 112
👮 *Полиция:* 102
🚑 *Скорая помощь:* 103
⛽ *Аварийная газовая служба:* 104

*При пожаре сообщите:*
• Точный адрес
• Что горит
• Есть ли люди в здании
• Ваша фамилия
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(emergency_text, parse_mode='Markdown', reply_markup=reply_markup)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о боте"""
    about_text = """
ℹ️ *О боте*

Этот бот создан для помощи в вопросах пожарной безопасности.

*Технологии:*
• YandexGPT - для генерации ответов
• RAG система - для работы с документами
• Telegram Bot API - для интерфейса

*База знаний:*
Бот использует информацию из загруженных PDF документов по пожарной безопасности.

*Разработчик:*
Создан с помощью AI технологий

*Версия:* 1.0
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(about_text, parse_mode='Markdown', reply_markup=reply_markup)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статус системы"""
    status_text = f"""
*Статус системы:*

✅ Бот: Работает
 База знаний: {'Загружена' if rag_engine.is_initialized else 'Не загружена'}
🤖 YandexGPT: Подключен
📄 Документов: {len(rag_engine.chunks)} блоков

*Конфигурация:*
• Folder ID: {YC_FOLDER_ID}
• Модель: yandexgpt-lite
    """
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text
    
    # Показываем что бот печатает
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # Получаем контекст из RAG системы
        context_text = rag_engine.get_context(user_message)
        
        # Формируем промпт для YandexGPT
        prompt = f"""{SYSTEM_PROMPT}

Контекст из базы знаний:
{context_text}

Вопрос пользователя: {user_message}

Ответ:"""
        
        # Отправляем запрос к YandexGPT
        response = await call_yandex_gpt(prompt)
        
        # Отправляем ответ пользователю
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
        )


async def call_yandex_gpt(prompt: str) -> str:
    """Вызов YandexGPT API"""
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YC_API_KEY}",
        "x-folder-id": YC_FOLDER_ID
    }
    
    data = {
        "modelUri": YC_MODEL_URI,
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    return result['result']['alternatives'][0]['message']['text']


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'faq':
        await faq_command(update, context)
    elif query.data == 'emergency':
        await emergency_command(update, context)
    elif query.data == 'about':
        await about_command(update, context)
    elif query.data == 'back_to_main':
        await start(update, context)


def main():
    """Запуск бота"""
    print("🚀 Запуск бота по пожарной безопасности...")
    
    # Инициализируем RAG движок
    print("📚 Инициализация базы знаний...")
    rag_engine.initialize()
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("faq", faq_command))
    application.add_handler(CommandHandler("emergency", emergency_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, button_callback))
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
