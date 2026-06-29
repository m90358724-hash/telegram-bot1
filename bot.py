import logging
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ===== ТАНЗИМОТ =====
BOT_TOKEN = "8881370181:AAECIJGdYbAPmfcQCUhv14tbVBwHzLIzA8Q"
GROQ_API_KEY = "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"

# Groq танзим
client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== МАТНҲОИ 3 ЗАБОН =====
TEXTS = {
    "tj": {
        "welcome": "🤖 *Хуш омадед ба DevHelper Bot!*\nЗабони худро интихоб кунед:",
        "main_menu": "🏠 *Менюи асосӣ*\nБахши заруриро интихоб кунед:",
        "ai_menu": "🤖 *AI Ёрдамчӣ*",
        "coding_menu": "💻 *Коднависӣ* — Забон интихоб кунед:",
        "tools_menu": "🛠 *Асбобҳо*",
        "web_menu": "🌐 *Вебсозӣ*",
        "learn_menu": "📚 *Омӯзиш*",
        "git_menu": "🐙 *Git & Deploy*",
        "project_menu": "🚀 *Сохтани Проект*",
        "api_menu": "⚙️ *API ва Database*",
        "profile_menu": "👤 *Профил*",
        "settings_menu": "⚙️ *Танзимот*",
        "help_menu": "❓ *Кӯмак*",
        "type_message": "✍️ Паёми худро нависед, AI ҷавоб медиҳад:",
        "back": "🔙 Бозгашт",
        "change_lang": "🌍 Иваз кардани забон",
    },
    "ru": {
        "welcome": "🤖 *Добро пожаловать в DevHelper Bot!*\nВыберите язык:",
        "main_menu": "🏠 *Главное меню*\nВыберите нужный раздел:",
        "ai_menu": "🤖 *ИИ Ассистент*",
        "coding_menu": "💻 *Кодинг* — Выберите язык:",
        "tools_menu": "🛠 *Инструменты*",
        "web_menu": "🌐 *Веб-разработка*",
        "learn_menu": "📚 *Обучение*",
        "git_menu": "🐙 *Git & Deploy*",
        "project_menu": "🚀 *Создание проекта*",
        "api_menu": "⚙️ *API и База данных*",
        "profile_menu": "👤 *Профиль*",
        "settings_menu": "⚙️ *Настройки*",
        "help_menu": "❓ *Помощь*",
        "type_message": "✍️ Напишите ваш вопрос, ИИ ответит:",
        "back": "🔙 Назад",
        "change_lang": "🌍 Сменить язык",
    },
    "en": {
        "welcome": "🤖 *Welcome to DevHelper Bot!*\nChoose your language:",
        "main_menu": "🏠 *Main Menu*\nChoose a section:",
        "ai_menu": "🤖 *AI Assistant*",
        "coding_menu": "💻 *Coding* — Choose a language:",
        "tools_menu": "🛠 *Tools*",
        "web_menu": "🌐 *Web Development*",
        "learn_menu": "📚 *Learning*",
        "git_menu": "🐙 *Git & Deploy*",
        "project_menu": "🚀 *Project Builder*",
        "api_menu": "⚙️ *API & Database*",
        "profile_menu": "👤 *Profile*",
        "settings_menu": "⚙️ *Settings*",
        "help_menu": "❓ *Help*",
        "type_message": "✍️ Type your question, AI will respond:",
        "back": "🔙 Back",
        "change_lang": "🌍 Change Language",
    }
}

user_languages = {}

def get_lang(user_id):
    return user_languages.get(user_id, "tj")

def t(user_id, key):
    lang = get_lang(user_id)
    return TEXTS[lang].get(key, key)

# ===== КЛАВИАТУРАҲО =====

def lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj"),
         InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
    ])

def main_menu_keyboard(uid):
    lang = get_lang(uid)
    if lang == "tj":
        buttons = [
            [InlineKeyboardButton("🤖 AI Ёрдамчӣ", callback_data="menu_ai"),
             InlineKeyboardButton("💻 Коднависӣ", callback_data="menu_coding")],
            [InlineKeyboardButton("🐞 Ислоҳи хато", callback_data="menu_bugfix"),
             InlineKeyboardButton("🚀 Сохтани проект", callback_data="menu_project")],
            [InlineKeyboardButton("🌐 Вебсозӣ", callback_data="menu_web"),
             InlineKeyboardButton("📱 Мобилсозӣ", callback_data="menu_mobile")],
            [InlineKeyboardButton("⚙️ API & Database", callback_data="menu_api"),
             InlineKeyboardButton("🛠 Асбобҳо", callback_data="menu_tools")],
            [InlineKeyboardButton("📚 Омӯзиш", callback_data="menu_learn"),
             InlineKeyboardButton("🐙 Git & Deploy", callback_data="menu_git")],
            [InlineKeyboardButton("👤 Профил", callback_data="menu_profile"),
             InlineKeyboardButton("⚙️ Танзимот", callback_data="menu_settings")],
            [InlineKeyboardButton("❓ Кӯмак", callback_data="menu_help")],
        ]
    elif lang == "ru":
        buttons = [
            [InlineKeyboardButton("🤖 ИИ Ассистент", callback_data="menu_ai"),
             InlineKeyboardButton("💻 Кодинг", callback_data="menu_coding")],
            [InlineKeyboardButton("🐞 Исправить ошибку", callback_data="menu_bugfix"),
             InlineKeyboardButton("🚀 Создать проект", callback_data="menu_project")],
            [InlineKeyboardButton("🌐 Веб-разработка", callback_data="menu_web"),
             InlineKeyboardButton("📱 Мобильная разработка", callback_data="menu_mobile")],
            [InlineKeyboardButton("⚙️ API & Database", callback_data="menu_api"),
             InlineKeyboardButton("🛠 Инструменты", callback_data="menu_tools")],
            [InlineKeyboardButton("📚 Обучение", callback_data="menu_learn"),
             InlineKeyboardButton("🐙 Git & Deploy", callback_data="menu_git")],
            [InlineKeyboardButton("👤 Профиль", callback_data="menu_profile"),
             InlineKeyboardButton("⚙️ Настройки", callback_data="menu_settings")],
            [InlineKeyboardButton("❓ Помощь", callback_data="menu_help")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("🤖 AI Assistant", callback_data="menu_ai"),
             InlineKeyboardButton("💻 Coding Tools", callback_data="menu_coding")],
            [InlineKeyboardButton("🐞 Bug Fix", callback_data="menu_bugfix"),
             InlineKeyboardButton("🚀 Project Builder", callback_data="menu_project")],
            [InlineKeyboardButton("🌐 Web Dev", callback_data="menu_web"),
             InlineKeyboardButton("📱 Mobile Dev", callback_data="menu_mobile")],
            [InlineKeyboardButton("⚙️ API & Database", callback_data="menu_api"),
             InlineKeyboardButton("🛠 Tools", callback_data="menu_tools")],
            [InlineKeyboardButton("📚 Learning", callback_data="menu_learn"),
             InlineKeyboardButton("🐙 Git & Deploy", callback_data="menu_git")],
            [InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
             InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")],
            [InlineKeyboardButton("❓ Help", callback_data="menu_help")],
        ]
    return InlineKeyboardMarkup(buttons)

def back_keyboard(uid):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ])

def ai_menu_keyboard(uid):
    lang = get_lang(uid)
    labels = {
        "tj": ["💬 Чат бо AI", "📝 Навиштани код", "📖 Фаҳмондани код",
               "🐞 Ислоҳи код", "⚡ Беҳтар кардани код", "🔍 Таҳлили код"],
        "ru": ["💬 Чат с ИИ", "📝 Написать код", "📖 Объяснить код",
               "🐞 Исправить код", "⚡ Улучшить код", "🔍 Анализ кода"],
        "en": ["💬 Chat with AI", "📝 Write Code", "📖 Explain Code",
               "🐞 Fix Code", "⚡ Improve Code", "🔍 Analyze Code"]
    }
    lbl = labels[lang]
    buttons = [
        [InlineKeyboardButton(lbl[0], callback_data="ai_chat"),
         InlineKeyboardButton(lbl[1], callback_data="ai_write")],
        [InlineKeyboardButton(lbl[2], callback_data="ai_explain"),
         InlineKeyboardButton(lbl[3], callback_data="ai_fix")],
        [InlineKeyboardButton(lbl[4], callback_data="ai_improve"),
         InlineKeyboardButton(lbl[5], callback_data="ai_analyze")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def coding_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("🐍 Python", callback_data="code_python"),
         InlineKeyboardButton("🌐 JavaScript", callback_data="code_js")],
        [InlineKeyboardButton("⚛️ React", callback_data="code_react"),
         InlineKeyboardButton("🎨 HTML/CSS", callback_data="code_html")],
        [InlineKeyboardButton("☕ Java", callback_data="code_java"),
         InlineKeyboardButton("⚙️ C++", callback_data="code_cpp")],
        [InlineKeyboardButton("🐘 PHP", callback_data="code_php"),
         InlineKeyboardButton("🦀 Rust", callback_data="code_rust")],
        [InlineKeyboardButton("🐹 Go", callback_data="code_go"),
         InlineKeyboardButton("🎯 Dart", callback_data="code_dart")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def tools_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("🔑 Password Generator", callback_data="tool_password"),
         InlineKeyboardButton("🆔 UUID Generator", callback_data="tool_uuid")],
        [InlineKeyboardButton("📱 QR Code", callback_data="tool_qr"),
         InlineKeyboardButton("🔐 JWT Decoder", callback_data="tool_jwt")],
        [InlineKeyboardButton("📦 Base64 Encode/Decode", callback_data="tool_base64"),
         InlineKeyboardButton("🔧 Regex Builder", callback_data="tool_regex")],
        [InlineKeyboardButton("📄 README Generator", callback_data="tool_readme"),
         InlineKeyboardButton("🌿 .env Generator", callback_data="tool_env")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def git_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("📋 Git Commands", callback_data="git_commands"),
         InlineKeyboardButton("🐙 GitHub Help", callback_data="git_github")],
        [InlineKeyboardButton("🐳 Docker", callback_data="git_docker"),
         InlineKeyboardButton("🖥 VPS Deploy", callback_data="git_vps")],
        [InlineKeyboardButton("🐧 Linux Commands", callback_data="git_linux"),
         InlineKeyboardButton("🌍 Hosting Guide", callback_data="git_hosting")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def web_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("📄 HTML Generator", callback_data="web_html"),
         InlineKeyboardButton("🎨 CSS Generator", callback_data="web_css")],
        [InlineKeyboardButton("⚡ JS Generator", callback_data="web_js"),
         InlineKeyboardButton("🚀 Landing Page", callback_data="web_landing")],
        [InlineKeyboardButton("💼 Portfolio", callback_data="web_portfolio"),
         InlineKeyboardButton("🔧 Admin Panel", callback_data="web_admin")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def project_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("🤖 Telegram Bot", callback_data="proj_tgbot"),
         InlineKeyboardButton("🌐 Website", callback_data="proj_website")],
        [InlineKeyboardButton("📱 Mobile App", callback_data="proj_mobile"),
         InlineKeyboardButton("⚙️ REST API", callback_data="proj_api")],
        [InlineKeyboardButton("📊 Dashboard", callback_data="proj_dashboard"),
         InlineKeyboardButton("🤖 AI Project", callback_data="proj_ai")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

def learn_keyboard(uid):
    buttons = [
        [InlineKeyboardButton("🐍 Python", callback_data="learn_python"),
         InlineKeyboardButton("🌐 JavaScript", callback_data="learn_js")],
        [InlineKeyboardButton("🎨 HTML/CSS", callback_data="learn_html"),
         InlineKeyboardButton("🧮 Algorithms", callback_data="learn_algo")],
        [InlineKeyboardButton("🏗 Data Structure", callback_data="learn_ds"),
         InlineKeyboardButton("🗄 SQL", callback_data="learn_sql")],
        [InlineKeyboardButton("🗺 Roadmap", callback_data="learn_roadmap"),
         InlineKeyboardButton("📝 Tasks", callback_data="learn_tasks")],
        [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(buttons)

# ===== AI КОНТЕКСТҲО =====
AI_CONTEXTS = {
    "ai_chat": "Ту DevHelper Bot — ёрдамчии барномасозӣ ҳастӣ.",
    "ai_write": "Ту коднавис ҳастӣ. Коди хуб бинавис. Код дар ``` блок деҳ.",
    "ai_explain": "Кодро хатт ба хатт шарҳ деҳ. Содда тавзеҳ деҳ.",
    "ai_fix": "Хатоҳоро пайдо кун ва ислоҳ кун.",
    "ai_improve": "Кодро беҳтар кун: суръат ва хонданпазирӣ.",
    "ai_analyze": "Кодро таҳлил кун ва тавсияҳо деҳ.",
    "code_python": "Ту Python эксперт ҳастӣ.",
    "code_js": "Ту JavaScript эксперт ҳастӣ.",
    "code_react": "Ту React.js эксперт ҳастӣ.",
    "code_html": "Ту HTML/CSS эксперт ҳастӣ.",
    "code_java": "Ту Java эксперт ҳастӣ.",
    "code_cpp": "Ту C++ эксперт ҳастӣ.",
    "code_php": "Ту PHP эксперт ҳастӣ.",
    "code_rust": "Ту Rust эксперт ҳастӣ.",
    "code_go": "Ту Go эксперт ҳастӣ.",
    "code_dart": "Ту Dart/Flutter эксперт ҳастӣ.",
    "menu_bugfix": "Ту debug эксперт ҳастӣ. Хатоҳоро ислоҳ кун.",
    "menu_mobile": "Ту mobile dev эксперт ҳастӣ.",
    "menu_api": "Ту API эксперт ҳастӣ.",
    "web_html": "Ту HTML эксперт ҳастӣ.",
    "web_css": "Ту CSS эксперт ҳастӣ.",
    "web_js": "Ту JavaScript эксперт ҳастӣ.",
    "web_landing": "Ту Landing Page эксперт ҳастӣ.",
    "web_portfolio": "Ту Portfolio сайт эксперт ҳастӣ.",
    "web_admin": "Ту Admin Panel эксперт ҳастӣ.",
    "proj_tgbot": "Ту Telegram Bot эксперт ҳастӣ.",
    "proj_website": "Ту веб-сайт эксперт ҳастӣ.",
    "proj_api": "Ту REST API эксперт ҳастӣ.",
    "proj_mobile": "Ту mobile app эксперт ҳастӣ.",
    "proj_dashboard": "Ту dashboard эксперт ҳастӣ.",
    "proj_ai": "Ту AI project эксперт ҳастӣ.",
    "tool_password": "Генератори парол бо Python нишон деҳ.",
    "tool_uuid": "UUID генератор бо Python нишон деҳ.",
    "tool_readme": "README.md мукаммал тайёр кун.",
    "tool_env": ".env файл намуна тайёр кун.",
    "tool_qr": "QR code генератор бо Python нишон деҳ.",
    "tool_jwt": "JWT decoder бо Python нишон деҳ.",
    "tool_base64": "Base64 encode/decode бо Python нишон деҳ.",
    "tool_regex": "Regex builder тавзеҳ деҳ.",
    "git_commands": "Фармонҳои Git бо мисолҳо тавзеҳ деҳ.",
    "git_github": "GitHub истифода тавзеҳ деҳ.",
    "git_docker": "Docker ва docker-compose тавзеҳ деҳ.",
    "git_vps": "VPS deploy тавзеҳ деҳ.",
    "git_linux": "Фармонҳои Linux нишон деҳ.",
    "git_hosting": "Hosting guide деҳ.",
    "learn_python": "Дарси Python барои мубтадиён деҳ.",
    "learn_js": "Дарси JavaScript барои мубтадиён деҳ.",
    "learn_html": "Дарси HTML/CSS барои мубтадиён деҳ.",
    "learn_algo": "Алгоритмҳоро бо мисолҳо тавзеҳ деҳ.",
    "learn_ds": "Data structure тавзеҳ деҳ.",
    "learn_sql": "SQL дарс деҳ.",
    "learn_roadmap": "Roadmap барои барномасоз деҳ.",
    "learn_tasks": "Вазифаҳои амалӣ барои омӯзиш деҳ.",
}

user_sessions = {}

async def ask_groq(prompt: str, context: str = "", lang: str = "tj") -> str:
    lang_instruction = {
        "tj": "Ҳамеша ба забони тоҷикӣ ҷавоб деҳ.",
        "ru": "Всегда отвечай на русском языке.",
        "en": "Always respond in English."
    }.get(lang, "")

    system_prompt = f"{context}\n{lang_instruction}"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return "❌ Хатогӣ рӯй дод. Лутфан дубора кӯшиш кунед."

# ===== ХАНДЛЕРҲО =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(
        t(uid, "welcome"),
        parse_mode="Markdown",
        reply_markup=lang_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        user_languages[uid] = lang
        await query.edit_message_text(t(uid, "main_menu"), parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

    elif data == "back_main":
        user_sessions.pop(uid, None)
        await query.edit_message_text(t(uid, "main_menu"), parse_mode="Markdown", reply_markup=main_menu_keyboard(uid))

    elif data == "menu_ai":
        await query.edit_message_text(t(uid, "ai_menu"), parse_mode="Markdown", reply_markup=ai_menu_keyboard(uid))

    elif data in ["ai_chat", "ai_write", "ai_explain", "ai_fix", "ai_improve", "ai_analyze"]:
        user_sessions[uid] = data
        labels = {
            "ai_chat": {"tj": "💬 Чат бо AI", "ru": "💬 Чат с ИИ", "en": "💬 AI Chat"},
            "ai_write": {"tj": "📝 Навиштани код", "ru": "📝 Написать код", "en": "📝 Write Code"},
            "ai_explain": {"tj": "📖 Фаҳмондани код", "ru": "📖 Объяснить код", "en": "📖 Explain Code"},
            "ai_fix": {"tj": "🐞 Ислоҳи код", "ru": "🐞 Исправить код", "en": "🐞 Fix Code"},
            "ai_improve": {"tj": "⚡ Беҳтар кардан", "ru": "⚡ Улучшить код", "en": "⚡ Improve Code"},
            "ai_analyze": {"tj": "🔍 Таҳлили код", "ru": "🔍 Анализ кода", "en": "🔍 Analyze Code"},
        }
        title = labels[data][get_lang(uid)]
        await query.edit_message_text(f"*{title}*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_coding":
        await query.edit_message_text(t(uid, "coding_menu"), parse_mode="Markdown", reply_markup=coding_keyboard(uid))

    elif data.startswith("code_"):
        user_sessions[uid] = data
        names = {"code_python": "🐍 Python", "code_js": "🌐 JavaScript", "code_react": "⚛️ React",
                 "code_html": "🎨 HTML/CSS", "code_java": "☕ Java", "code_cpp": "⚙️ C++",
                 "code_php": "🐘 PHP", "code_rust": "🦀 Rust", "code_go": "🐹 Go", "code_dart": "🎯 Dart"}
        await query.edit_message_text(f"*{names.get(data, data)}*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_bugfix":
        user_sessions[uid] = data
        title = {"tj": "🐞 Ислоҳи хато", "ru": "🐞 Исправление ошибок", "en": "🐞 Bug Fix"}[get_lang(uid)]
        await query.edit_message_text(f"*{title}*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_web":
        await query.edit_message_text(t(uid, "web_menu"), parse_mode="Markdown", reply_markup=web_keyboard(uid))

    elif data.startswith("web_"):
        user_sessions[uid] = data
        await query.edit_message_text(f"*🌐 Web*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_project":
        await query.edit_message_text(t(uid, "project_menu"), parse_mode="Markdown", reply_markup=project_keyboard(uid))

    elif data.startswith("proj_"):
        user_sessions[uid] = data
        await query.edit_message_text(f"*🚀 Project*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_tools":
        await query.edit_message_text(t(uid, "tools_menu"), parse_mode="Markdown", reply_markup=tools_keyboard(uid))

    elif data.startswith("tool_"):
        user_sessions[uid] = data
        await query.edit_message_text(f"*🛠 Tool*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_git":
        await query.edit_message_text(t(uid, "git_menu"), parse_mode="Markdown", reply_markup=git_keyboard(uid))

    elif data.startswith("git_"):
        user_sessions[uid] = data
        await query.edit_message_text(f"*🐙 Git & Deploy*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_learn":
        await query.edit_message_text(t(uid, "learn_menu"), parse_mode="Markdown", reply_markup=learn_keyboard(uid))

    elif data.startswith("learn_"):
        user_sessions[uid] = data
        await query.edit_message_text(f"*📚 Learning*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_settings":
        await query.edit_message_text(t(uid, "settings_menu"), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid, "change_lang"), callback_data="change_lang")],
                [InlineKeyboardButton(t(uid, "back"), callback_data="back_main")]
            ]))

    elif data == "change_lang":
        await query.edit_message_text(t(uid, "welcome"), parse_mode="Markdown", reply_markup=lang_keyboard())

    elif data == "menu_profile":
        name = query.from_user.first_name
        lang = get_lang(uid)
        msg = {"tj": f"👤 *Профил*\n\n🧑 Ном: {name}\n🌍 Забон: Тоҷикӣ",
               "ru": f"👤 *Профиль*\n\n🧑 Имя: {name}\n🌍 Язык: Русский",
               "en": f"👤 *Profile*\n\n🧑 Name: {name}\n🌍 Language: English"}[lang]
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data == "menu_help":
        lang = get_lang(uid)
        msg = {"tj": "❓ *Кӯмак*\n\n📖 Бот ба шумо дар навиштани код, ислоҳи хато ва омӯзиш кӯмак мекунад!\n\n📩 @YourSupport",
               "ru": "❓ *Помощь*\n\n📖 Бот помогает писать код, исправлять ошибки и учиться!\n\n📩 @YourSupport",
               "en": "❓ *Help*\n\n📖 Bot helps with coding, bug fixing and learning!\n\n📩 @YourSupport"}[lang]
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=back_keyboard(uid))

    elif data in ["menu_mobile", "menu_api"]:
        user_sessions[uid] = data
        await query.edit_message_text(f"*{data}*\n\n{t(uid, 'type_message')}", parse_mode="Markdown", reply_markup=back_keyboard(uid))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    lang = get_lang(uid)
    session = user_sessions.get(uid, "ai_chat")

    wait_msg = {"tj": "⏳ AI фикр мекунад...", "ru": "⏳ ИИ думает...", "en": "⏳ AI is thinking..."}
    msg = await update.message.reply_text(wait_msg[lang])

    ai_context = AI_CONTEXTS.get(session, AI_CONTEXTS["ai_chat"])
    response = await ask_groq(text, ai_context, lang)

    if len(response) > 4000:
        response = response[:4000] + "\n\n..."

    try:
        await msg.edit_text(response, parse_mode="Markdown")
    except Exception:
        await msg.edit_text(response)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🤖 DevHelper Bot оғоз ёфт!")
    app.run_polling()

if __name__ == "__main__":
    main()