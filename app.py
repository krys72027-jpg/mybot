import telebot

# ضع توكن البوت هنا أو استبدله بمتغير البيئة الخاص بك
BOT_TOKEN = "8606529033:AAGIpCdlt74w3kvVUyPHZ2P_aBcTxHjPzcs"
bot = telebot.TeleBot(BOT_TOKEN)

# معرف المطور المطلوب إظهاره
DEVELOPER_USERNAME = "@Murtadh_a"

# رابط صورة الترحيب (يمكنك استبداله برابط أي صورة مباشرة تريد إرسالها مع المحادثة)
WELCOME_IMAGE_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    caption = (
        f"مرحباً بك {user_name} في بوت التحميل الخاص بنا!\n"
        f"أرسل لي أي فيديو وسأقوم بتحميله لك مع معلوماتك.\n\n"
        f"👨‍💻 المطور: {DEVELOPER_USERNAME}"
    )
    # إرسال صورة مع نص الترحيب
    bot.send_photo(
        message.chat.id, 
        photo=WELCOME_IMAGE_URL, 
        caption=caption
    )

@bot.message_handler(content_types=['video'])
def handle_video(message):
    user_username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    
    caption = (
        f"📥 تم استلام الفيديو بنجاح!\n"
        f"👤 بواسطة المستخدم: {user_username}\n\n"
        f"👨‍💻 المطور: {DEVELOPER_USERNAME}"
    )
    
    # إعادة إرسال الفيديو مع اسم المستخدم ومعلومات المطور
    bot.send_video(
        message.chat.id, 
        message.video.file_id, 
        caption=caption
    )

# تشغيل البوت
bot.infinity_polling()
