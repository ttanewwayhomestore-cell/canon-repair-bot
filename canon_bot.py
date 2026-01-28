import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# ၁။ Render Port Timeout ကျော်ရန် Flask Server
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ၂။ Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)

# Model နာမည်ကို အောက်ပါအတိုင်း အတိအကျ ပြောင်းပါ
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini သို့ စာပို့ခြင်း
        chat_prompt = f"You are a Canon Repair Expert. Answer in Myanmar: {message.text}"
        response = model.generate_content(chat_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        # Error အမျိုးအစားကို User သိအောင် ပြန်ပို့ခြင်း
        bot.reply_to(message, f"System Error ဖြစ်နေပါတယ်ခင်ဗျာ။\nError Type: {e}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot is successfully running on Render...")
    bot.polling(non_stop=True)
