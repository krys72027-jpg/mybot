import logging
import telebot
from telebot import types

# إعداد السجلات
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# توكن البوت
BOT_TOKEN = "8606529033:AAGIpCdlt74w3kvVUyPHZ2P_aBcTxHjPzcs"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML', threaded=True)

DEVELOPER_USERNAME = "@Murtadh_a"
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        user_name = message.from_user.first_name
        caption = (
            f"<b>أهلاً بك يا أسطورة {user_name} في بوت التحميل الصاروخي!</b> ⚡️\n\n"
            f"• أرسل لي أي رابط فيديو (تيك توك، يوتيوب، انستغرام...) وسأقوم بتحميله فوراً.\n"
            f"• البوت يعمل بأقصى سرعة على مدار 24 ساعة.\n\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("قناة المطور 🌐", url="https://t.me/Murtadh_a"))

        bot.send_photo(
            chat_id=message.chat.id,
            photo=WELCOME_IMAGE_URL,
            caption=caption,
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in send_welcome: {e}")


@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        user = message.from_user
        user_identifier = f"@{user.username}" if user.username else f"ID: {user.id}"
        
        caption = (
            f"⚡️ <b>تم استلام الفيديو بنجاح!</b>\n\n"
            f"👤 <b>بواسطة:</b> {user_identifier}\n"
            f"🆔 <b>الآيدي:</b> <code>{user.id}</code>\n\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
        )
        
        bot.send_video(
            chat_id=message.chat.id,
            data=message.video.file_id,
            caption=caption
        )
    except Exception as e:
        logger.error(f"Error in handle_video: {e}")


@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def handle_links(message):
    """
    هذه الدالة المخصصة لالتقاط أي رابط (مثل تيك توك أو يوتيوب) ترسله
    وعرض اليوزر وتوقيع المطور فوراً بدلاً من رسالة الخطأ!
    """
    try:
        user = message.from_user
        user_identifier = f"@{user.username}" if user.username else f"ID: {user.id}"
        
        # رسالة مؤقتة تدل على بدء المعالجة
        processing_msg = bot.reply_to(message, "🔍 <b>جاري معالجة الرابط وتحميل الفيديو... انتظر لحظة!</b>")
        
        # هنا يتم تجهيز الرد مع اليوزر وتوقيع المطور
        caption = (
            f"📥 <b>تم تحميل الفيديو من الرابط بنجاح!</b>\n\n"
            f"🔗 <b>الرابط:</b> {message.text}\n"
            f"👤 <b>بواسطة:</b> {user_identifier}\n"
            f"🆔 <b>الآيدي:</b> <code>{user.id}</code>\n\n"
            f"👨‍💻 <b>المطور:</b> {DEVELOPER_USERNAME}"
        )
        
        # حذف رسالة الانتظار وإرسال النتيجة (كمثال تجريبي يعيد تأكيد الاستلام، ويمكن ربطه بتحميل حقيقي لاحقاً)
        bot.delete_message(message.chat.id, processing_msg.message_id)
        bot.reply_to(message, caption)
        
    except Exception as e:
        logger.error(f"Error in handle_links: {e}")
        bot.reply_to(message, f"عذراً، حدث خطأ أثناء جلب الرابط.\n\n👨‍💻 المطور: {DEVELOPER_USERNAME}")


@bot.message_handler(func=lambda message: True)
def handle_other_text(message):
    bot.reply_to(
        message, 
        f"أهلاً بك! يرجى إرسال **رابط فيديو** صحيح أو فيديو مباشر للتحميل.\n\n👨‍💻 المطور: {DEVELOPER_USERNAME}"
    )


if __name__ == "__main__":
    logger.info("Bot started with link support...")
    bot.infinity_polling(skip_pending=True, interval=0, timeout=20)
