import telebot
from telebot import types

# توكن البوت الخاص بك
BOT_TOKEN = "8606529033:AAGIpCdlt74w3kvVUyPHZ2P_aBcTxHjPzcs"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# معلومات المطور والقناة الجديدة الخاصة بك
DEVELOPER_USERNAME = "@Murtadh_a"
CHANNEL_URL = "https://t.me/mortd8"

# رابط الصورة الترحيبية
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    caption = (
        f"<b>أهلاً بك يا أسطورة {user_name} في بوت التحميل!</b> 🚀\n\n"
        f"• أرسل لي أي رابط فيديو وسأقوم بتحميله لك بنجاح.\n"
        f"• البوت يعمل بأقصى سرعة على مدار 24 ساعة.\n\n"
        f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
    )
    
    # زر قناة المطور الجديدة
    markup = types.InlineKeyboardMarkup()
    btn_channel = types.InlineKeyboardButton("قناة المطور 🌐", url=CHANNEL_URL)
    markup.add(btn_channel)

    bot.send_photo(
        chat_id=message.chat.id,
        photo=WELCOME_IMAGE_URL,
        caption=caption,
        reply_markup=markup
    )

@bot.message_handler(content_types=['video'])
def handle_video(message):
    user = message.from_user
    user_identifier = f"@{user.username}" if user.username else f"ID: {user.id}"
    
    caption = (
        f"✨ <b>تم التحميل بنجاح بواسطة البوت!</b>\n\n"
        f"👤 <b>بواسطة:</b> {user_identifier}\n"
        f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
    )
    
    bot.send_video(
        chat_id=message.chat.id,
        data=message.video.file_id,
        caption=caption
    )

@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.reply_to(
        message, 
        f"أهلاً بك! يرجى إرسال فيديو للتحميل، أو اضغط على /start للبدء.\n\n👨‍💻 المطور: {DEVELOPER_USERNAME}"
    )

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
