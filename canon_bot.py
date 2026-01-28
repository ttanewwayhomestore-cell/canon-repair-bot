import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Render အတွက် Port ပေးခြင်း
app = Flask('')
@app.route('/')
def home():
    return "Bot is active!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Key များ ခေါ်ယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)

# Model နာမည်ကို အတိအကျ ပြင်ဆင်ခြင်း
model = genai.GenerativeModel('models/gemini-3-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini သို့ စာပို့ခြင်း
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Error အပြည့်အစုံကို User ထံ ပြန်ပို့ခိုင်းခြင်း
        error_msg = str(e)
        bot.reply_to(message, f"Error Detected: {error_msg}")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(non_stop=True)

