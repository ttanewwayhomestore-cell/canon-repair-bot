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

# အခု Error တက်နေတဲ့ နေရာကို ဒီလိုပြင်လိုက်ပါ
# 'gemini-1.5-flash' ဆိုတာကို အတိအကျ ခေါ်ယူခြင်း
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini သို့ စာပို့ခြင်း
        # generate_content မှာ content တစ်ခုတည်း ပို့ကြည့်ပါ
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        # Error အပြည့်အစုံကို Telegram မှာ ပြခိုင်းခြင်း
        bot.reply_to(message, ထပ်မံကြိုးစားနေပါတယ်။ f"System Message: {e}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot is successfully starting...")
    bot.polling(non_stop=True)
