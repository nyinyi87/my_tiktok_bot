import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# မိမိ Bot Token ကို ဒီနေရာမှာ တိုက်ရိုက်ထည့်ပါ
TOKEN = "8837141917:AAHUhSgiMLbOofGAeMrrB4qEXtAF9JLAY8Y"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။💕 TikTok Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းလုဒ်ဆွဲပေးပါမည်။P Gyi။")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "tiktok.com" in url:
        await update.message.reply_text("ဗီဒီယို ရယူနေပါသည် ခဏစောင့်ပါ...")
        
        api_url = f"https://www.tikwm.com/api/?url={url}"
        try:
            res = requests.get(api_url).json()
            if res.get("code") == 0:
                video_url = res["data"]["play"]
                await update.message.reply_video(video=video_url, caption="Downloaded by TikTok Bot")
            else:
                await update.message.reply_text("ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Link မှန်မမှန် ပြန်စစ်ပေးပါ။")
        except Exception as e:
            await update.message.reply_text("Error ဖြစ်ပေါ်နေပါသည်။ ခဏကြာမှ ပြန်စမ်းပါ။")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော TikTok Link ကို ပို့ပေးပါ။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
