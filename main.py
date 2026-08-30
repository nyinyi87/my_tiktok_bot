import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Railway Variables ထဲမှ BOT_TOKEN ကို ဖတ်ယူခြင်း
TOKEN = os.getenv("8837141917:AAHUhSgiMLbOofGAeMrrB4qEXtAF9JLAY8Y")

# /start Command အတွက်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။💕 TikTok Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းလုဒ်ဆွဲပေးပါမည်။P Gyi။")

# TikTok Link များကို လက်ခံဆောင်ရွက်ပေးမည့် Function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "tiktok.com" in url:
        await update.message.reply_text("ဗီဒီယို ရယူနေပါသည် ခဏစောင့်ပါ...")
        
        # TikWM API အသုံးပြု၍ Watermark မပါသော Link ယူခြင်း
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            # ဗီဒီယိုကို Telegram သို့ ပြန်လည်ပေးပို့ခြင်း
            await update.message.reply_video(video=video_url, caption="Downloaded by TikTok Bot")
        else:
            await update.message.reply_text("ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Link မှန်မမှန် ပြန်စစ်ပေးပါ။")
    else:
        await update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော TikTok Link ကို ပို့ပေးပါ။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
