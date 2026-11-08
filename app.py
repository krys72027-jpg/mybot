import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = "8606529033:AAGIpCdlt74w3kvVUyPHZ2P_aBcTxHjPzcs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! 🚀\nأرسل لي أي رابط فيديو (من يوتيوب، تيك توك، انستغرام، فيسبوك، تويتر...) وسأقوم بتحميله لك بأعلى جودة فوراً 📥")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "⚠️ يرجى إرسال رابط صحيح يبدأ بـ http أو https.")
        return
    
    msg = bot.reply_to(message, "⏳ جاري معالجة وفحص الرابط والتحميل، انتظر ثواني...")
    
    # إعدادات ذكية تدعم كل المنصات وتختار أفضل وأسرع صيغة مدمجة
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_media.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    file_path = None
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        # التحقق من نوع الملف وإرساله بالطريقة المناسبة
        file_size = os.path.getsize(file_path)
        # حماية ضد الملفات الكبيرة جداً التي قد تفشل في إرسال التليجرام (أكثر من 50 ميجابايت في الحسابات المجانية)
        if file_size > 50 * 1024 * 1024:
            bot.edit_message_text("⚠️ حجم الفيديو كبير جداً ولا يمكن إرساله عبر التليجرام.", message.chat.id, msg.message_id)
        else:
            with open(file_path, 'rb') as media_file:
                # فحص امتداد الملف لإرساله كفيديو أو مستند إذا لزم الأمر
                if file_path.endswith(('.mp4', '.mkv', '.webm', '.mov')):
                    bot.send_video(message.chat.id, media_file, caption="✨ تم التحميل بنجاح بواسطة البوت!")
                else:
                    bot.send_document(message.chat.id, media_file, caption="✨ تم التحميل بنجاح!")
            bot.delete_message(message.chat.id, msg.message_id)
            
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        bot.edit_message_text(f"❌ عذراً، حدث خطأ أثناء التحميل:\n`{str(e)}`", message.chat.id, msg.message_id, parse_mode="Markdown")
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

print("البوت الخارق يعمل الآن بكفاءة عالية...")
bot.infinity_polling()

