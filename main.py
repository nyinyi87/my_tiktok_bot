import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8837141917:AAHUhSgiMLbOofGAeMrrB4qEXtAF9JLAY8Y"  # မိမိ Bot Token ကို ပြန်ထည့်ပါ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။💕TikTok Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းလုဒ်ဆွဲပေးပါမည်။P Gyi။")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "tiktok.com" in url:
        msg = await update.message.reply_text("ဗီဒီယို ရယူနေပါသည် ခဏစောင့်ပါ...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            # TikWM API ခေါ်ယူခြင်း
            api_url = f"https://www.tikwm.com/api/?url={url}"
            res = requests.get(api_url, headers=headers, timeout=15).json()
            
            if res.get("code") == 0 and "data" in res:
                video_data = res["data"]
                video_url = video_data.get("play")
                
                # Video file ကို Telegram ထံ တိုက်ရိုက် ပေးပို့ခြင်း
                await update.message.reply_video(
                    video=video_url, 
                    caption=f"🎬 {video_data.get('title', 'TikTok Video')}\n\nDownloaded by Bot"
                )
                await msg.delete() # စောင့်ခိုင်းထားသော စာကို ဖျက်ခြင်း
            else:
                await msg.edit_text("❌ ဗီဒီယို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Link မှန်မမှန် သို့မဟုတ် Public video ဟုတ်မဟုတ် ပြန်စစ်ပေးပါ။")
                
        except Exception as e:
            print(f"Error: {e}")
            await msg.edit_text("❌ Server အကူးအပြောင်းတွင် အမှားတစ်ခုဖြစ်ပေါ်နေပါသည်။ ခဏကြာမှ ပြန်စမ်းပါ။")
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
