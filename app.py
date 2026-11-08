import logging
import threading
import telebot
from telebot import types

# إعداد السجلات فائقة السرعة
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# توكن البوت
BOT_TOKEN = "8606529033:AAGIpCdlt74w3kvVUyPHZ2P_aBcTxHjPzcs"

# تفعيل الـ threaded للملفات والطلبات لتكون السرعة فائقة (أسرع من الطلقة 🚀)
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML', threaded=True)

# الثوابت
DEVELOPER_USERNAME = "@Murtadh_a"
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"


@bot.message_handler(commands=['start', 'help'])
def lightning_start(message):
    """
    استجابة فورية للبدء، تظهر الصورة والترحيب مرة واحدة وبدون أي تأخير.
    """
    try:
        user_name = message.from_user.first_name
        caption = (
            f"<b>أهلاً بك يا أسطورة {user_name} في بوت التحميل الصاروخي!</b> ⚡️\n\n"
            f"• أرسل لي أي فيديو وسيتم معالجته وفحصه فوراً.\n"
            f"• البوت يعمل بأقصى سرعة على مدار 24 ساعة.\n\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("قناة المطور 🌐", url="https://t.me/Murtadh_a"))

        # إرسال الصورة والترحيب بسرعة فائقة
        bot.send_photo(
            chat_id=message.chat.id,
            photo=WELCOME_IMAGE_URL,
            caption=caption,
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in lightning_start: {e}")


@bot.message_handler(content_types=['video'])
def lightning_video(message):
    """
    معالجة الفيديوهات بشكل متوازي (Multi-threaded) لضمان السرعة الفائقة جداً
    وعرض اليوزر وتوقيع المطور فورياً.
    """
    try:
        user = message.from_user
        user_identifier = f"@{user.username}" if user.username else f"ID: {user.id}"
        
        caption = (
            f"⚡️ <b>تم استلام ومعالجة الفيديو بسرعة الصاروخ!</b>\n\n"
            f"👤 <b>بواسطة:</b> {user_identifier}\n"
            f"🆔 <b>الآيدي:</b> <code>{user.id}</code>\n\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
        )
        
        # إرسال الفيديو بالسرعة القصوى
        bot.send_video(
            chat_id=message.chat.id,
            data=message.video.file_id,
            caption=caption
        )
    except Exception as e:
        logger.error(f"Error in lightning_video: {e}")


@bot.message_handler(func=lambda message: True)
def lightning_fallback(message):
    """
    الرد السريع على الرسائل النصية العشوائية
    """
    bot.reply_to(
        message, 
        f"أنا جاهز! أرسل فيديو للتحميل فوراً، أو اضغط /start للترحيب.\n\n👨‍💻 المطور: {DEVELOPER_USERNAME}"
    )


if __name__ == "__main__":
    logger.info("Lightning Bot is starting with multi-threading...")
    # تشغيل البوت بخاصية الـ skip_pending والـ interval السريع لعدم حدوث أي طابور انتظار (Queue)
    bot.infinity_polling(skip_pending=True, interval=0, timeout=20)
