import telebot
import google.generativeai as genai

# --- သင့်ရဲ့ Key များကို ဒီမှာ သေချာထည့်ပါ ---
BOT_TOKEN = "8243177684:AAFbkyJTmWN6_jnyHfaVMBLLWYO12LuEzSA"
API_KEY = "AIzaSyAkIZpSWYSJdepB37rqfRYuMSw0UXy3y-0"

# Gemini Configuration
genai.configure(api_key=API_KEY)

# Model နာမည်ကို 'gemini-1.5-flash' လို့ပဲ တိုက်ရိုက်ပေးကြည့်ပါမယ်
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Canon Repair Expert အဖြစ် instruction ထည့်သွင်းခြင်း
        chat_prompt = f"You are a Canon Repair Expert. User question: {message.text}. Answer in Myanmar language clearly."
        response = model.generate_content(chat_prompt)
        
        # အဖြေကို ပြန်ပို့ခြင်း
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error log: {e}")
        bot.reply_to(message, "ခဏလေးစောင့်ပေးပါ၊ System ပြန်တက်လာအောင် လုပ်နေပါတယ်။")

print("Canon Repair Bot is online and waiting for messages...")
bot.polling()