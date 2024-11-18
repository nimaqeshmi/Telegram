import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# تنظیمات توکن‌ها
TELEGRAM_TOKEN = "8016928931:AAF3ZIZRAMOnt_8JulXWru1ZTJlMmexMsos"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# فقط برای کاربر خاص (آیدی شما)
ALLOWED_USER = "@Mrnimarad7"

# منوی اصلی
def start(update: Update, context: CallbackContext):
    if update.effective_user.username != ALLOWED_USER.strip('@'):
        update.message.reply_text("دسترسی ندارید.")
        return

    keyboard = [
        [InlineKeyboardButton("ChatGPT 3", callback_data="chatgpt_3"),
         InlineKeyboardButton("ChatGPT 4", callback_data="chatgpt_4")],
        [InlineKeyboardButton("DALL·E", callback_data="dalle"),
         InlineKeyboardButton("آمار استفاده", callback_data="usage")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("به ربات خوش آمدید! نسخه مورد نظر خود را انتخاب کنید:", reply_markup=reply_markup)

# هندلر انتخاب نسخه‌ها
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "chatgpt_3":
        query.edit_message_text("در حال استفاده از ChatGPT 3...")
    elif query.data == "chatgpt_4":
        query.edit_message_text("در حال استفاده از ChatGPT 4...")
    elif query.data == "dalle":
        query.edit_message_text("در حال تولید تصویر با DALL·E...")
    elif query.data == "usage":
        usage = calculate_usage()
        query.edit_message_text(f"آمار استفاده:\n{usage}")
    else:
        query.edit_message_text("دستور نامعتبر.")

# محاسبه آمار استفاده
def calculate_usage():
    # نمونه محاسبه مصرف (جایگزین کنید با داده واقعی)
    return "شما 50% از کلید خود استفاده کرده‌اید."

# هندلر پیام‌ها
def echo(update: Update, context: CallbackContext):
    if update.effective_user.username != ALLOWED_USER.strip('@'):
        update.message.reply_text("دسترسی ندارید.")
        return

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=update.message.text,
        max_tokens=100
    )
    update.message.reply_text(response.choices[0].text.strip())

# تنظیمات اصلی
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
