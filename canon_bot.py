import os
import telebot
import google.generativeai as genai

# Render Environment Variables မှ Key များကို ဆွဲယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_prompt = f"You are a Canon Repair Expert. User question: {message.text}. Answer in Myanmar language clearly."
        response = model.generate_content(chat_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ခဏလေးစောင့်ပေးပါ၊ System ပြန်တက်လာအောင် လုပ်နေပါတယ်။")

print("Bot is running on Cloud...")
bot.polling()
