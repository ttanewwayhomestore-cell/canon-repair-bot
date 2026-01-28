import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# ၁။ Render Port Timeout ကို ကျော်ရန် Flask Server သေးသေးလေး ဆောက်ခြင်း
app = Flask('')
@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    # Render က ပေးတဲ့ Port သို့မဟုတ် 8080 ကို သုံးခြင်း
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ၂။ Bot Configuration (Environment Variables မှ Key များကို ယူခြင်း)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)
# Model နာမည်ကို အမှန်အတိုင်း ပြင်ဆင်ခြင်း
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini သို့ စာပို့ခြင်း
        chat_prompt = f"You are a Canon Repair Expert. User question: {message.text}. Answer in Myanmar language clearly."
        response = model.generate_content(chat_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"စိတ်မရှိပါနဲ့၊ အခက်အခဲလေး ရှိနေလို့ပါ။ Error: {e}")

if __name__ == "__main__":
    # Flask Server ကို နောက်ကွယ် (Thread) မှာ မောင်းထားခြင်း
    t = Thread(target=run)
    t.start()
    
    print("Bot is successfully running on Render...")
    # Bot ကို အမြဲတမ်း ပွင့်နေအောင် လုပ်ခြင်း
    bot.polling(non_stop=True)
