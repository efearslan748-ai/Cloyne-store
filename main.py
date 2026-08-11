import telebot
import os

# Kendi bilgilerini buraya gir
TOKEN = "8878714151:AAEeT6wXAcjI00elTEjO2VcsBcAeD4ubM7w"
CHANNEL_USERNAME = "@cloynestoree" 

bot = telebot.TeleBot(TOKEN)

def check_user_subscription(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if chat_member.status in ['left', 'kicked']:
            return False
        return True
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_user_subscription(message.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📢 Kanalımıza Katıl", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"))
        markup.add(telebot.types.InlineKeyboardButton("✅ Katıldım", callback_data="check_sub"))
        bot.send_message(message.chat.id, "Botu kullanmak için kanala katılmalısın!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hoş geldin! Bot aktif.")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_inline(call):
    if check_user_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "Onaylandı!")
        bot.send_message(call.message.chat.id, "Artık botu kullanabilirsin.")
    else:
        bot.answer_callback_query(call.id, "Hala katılmamışsın!", show_alert=True)

bot.infinity_polling()
