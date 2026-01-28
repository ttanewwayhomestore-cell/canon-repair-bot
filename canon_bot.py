import os
import telebot
import google.generativeai as genai

# Render Environment Variables ထဲက Key တွေကို ဆွဲထုတ်ခြင်း
# အခုနက Render မှာ BOT_TOKEN နဲ့ API_KEY လို့ နာမည်ပေးခဲ့တာ သေချာပါစေ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')

genai.configure(api_key=API_KEY)

# Gemini 1.5 Flash Model ကို အသုံးပြုခြင်း
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini ဆီ စာပို့ခြင်း
        chat_prompt = f"You are a Canon Repair Expert. User question: {message.text}. Answer in Myanmar language clearly."
        response = model.generate_content(chat_prompt)
        
        # အဖြေပြန်ပို့ခြင်း
        bot.reply_to(message, response.text)
    except Exception as e:
        # Error တက်ရင် ဘာကြောင့်တက်လဲဆိုတာ User ကို တိုက်ရိုက်ပြောခိုင်းခြင်း
        print(f"Error: {e}")
        bot.reply_to(message, f"စိတ်မရှိပါနဲ့၊ Error တက်နေလို့ပါ။ Error အမျိုးအစားမှာ - {e}")

print("Bot is successfully running on Render...")
bot.polling()
