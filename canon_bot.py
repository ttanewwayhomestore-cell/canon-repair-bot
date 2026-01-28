import os
import telebot
import google.generativeai as genai

# Render တွင်ဖြည့်ခဲ့သော Environment Variables ကို ဤနေရာတွင် လှမ်းခေါ်ခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

# Gemini ကို ချိတ်ဆက်ခြင်း
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # User ပို့လိုက်သောစာကို Gemini ထံ ပို့ခြင်း
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # Error အစစ်အမှန်ကို Render Log ထဲမှာ မြင်ရအောင် print ထုတ်ခြင်း
        print(f"Error occurred: {e}")
        bot.reply_to(message, f"Error တက်နေပါတယ်ခင်ဗျာ။ Error အမျိုးအစားမှာ - {e}")

print("Bot is starting on Cloud...")
bot.polling()
