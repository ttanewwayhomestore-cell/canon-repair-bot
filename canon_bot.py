import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Render Port Error ကို ကျော်ရန် Dummy Server ဆောက်ခြင်း
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render က ပေးတဲ့ Port သို့မဟုတ် 8080 တွင် မောင်းခြင်း
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(f"You are a Canon Repair Expert. Answer in Myanmar: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"စိတ်မရှိပါနဲ့၊ အမှားတစ်ခုရှိနေပါတယ်။ Error: {e}")

if __name__ == "__main__":
    # Flask Server ကို နောက်ကွယ်မှာ အရင်ဖွင့်ခြင်း
    t = Thread(target=run)
    t.start()
    
    print("Bot is successfully running on Cloud...")
    # Bot ကို စတင်မောင်းနှင်ခြင်း
    bot.polling(non_stop=True)
