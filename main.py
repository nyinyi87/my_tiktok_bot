import os
import requests
import asyncio
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8837141917:AAHUhSgiMLbOofGAeMrrB4qEXtAF9JLAY8Y"  # မိမိ Bot Token ကို ပြန်ထည့်ပါ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။💕 TikTok Video သို့မဟုတ် Photo Link ပို့ပေးပါ၊ Watermark မပါဘဲ ဒေါင်းလုဒ်ဆွဲပေးပါမည်။P Gyi။")

async def show_progress(msg):
    """ 1% မှ 100% သို့ Progress Bar တက်သွားသည့် Animation """
    try:
        steps = [10, 30, 55, 80, 100]
        for percent in steps:
            await asyncio.sleep(0.4)
            blocks = "█" * (percent // 10) + "░" * (10 - (percent // 10))
            await msg.edit_text(f"⏳ ရယူနေပါသည်... {percent}%\n[{blocks}]
            🥺ပြန်မလာတဲ့သူကိုစောင့်သေးတာပဲ ခနလေးစောင့်ပါ။🥺")
    except Exception:
        pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "tiktok.com" in url:
        msg = await update.message.reply_text("⏳ ရယူနေပါသည်... 0%\n[░░░░░░░░░░]")
        
        # Progress တက်သွားရန် background task အဖြစ် Run ခြင်း
        progress_task = asyncio.create_task(show_progress(msg))
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            api_url = f"https://www.tikwm.com/api/?url={url}"
            res = requests.get(api_url, headers=headers, timeout=15).json()
            
            # Progress animation ပြီးစီးသည်အထိ ခေတ္တစောင့်ခြင်း
            await progress_task
            
            if res.get("code") == 0 and "data" in res:
                data = res["data"]
                title = data.get('title', 'TikTok Content')
                
                # ၁။ Photo Slide (Images) ဖြစ်ပါက
                if "images" in data and data["images"]:
                    images = data["images"]
                    media_group = []
                    
                    for i, img_url in enumerate(images):
                        if i == 0:
                            # ပထမဆုံး ပုံတွင် စာတန်း (Caption) ထည့်ရန်
                            media_group.append(InputMediaPhoto(media=img_url, caption=f"📸 {title}\n\nDownloaded by Bot"))
                        else:
                            media_group.append(InputMediaPhoto(media=img_url))
                    
                    await update.message.reply_media_group(media=media_group)
                
                # ၂။ Video ဖြစ်ပါက
                elif "play" in data:
                    video_url = data["play"]
                    await update.message.reply_video(
                        video=video_url, 
                        caption=f"🎬 {title}\n\nPowered by @NYINYISK"
                    )
                
                await msg.delete() # Progress စာတန်းကို ဖျက်လိုက်ခြင်း
            else:
                await msg.edit_text("❌ ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Link မှန်မမှန် သို့မဟုတ် Public ဟုတ်မဟုတ် ပြန်စစ်ပေးပါ။")
                
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
