import telebot
import threading
import os

# =====================
# PHẦN BOT TELEGRAM
# =====================
BOT_TOKEN = "8431435178:AAEKjUBu4DUD9-CpF8XIz9sHqzIIlZiPbP8"
bot = telebot.TeleBot(BOT_TOKEN)

# =====================
# PHẦN CODE GỐC (giữ nguyên)
# =====================
import requests, time

def get_token(input_file):
    tokens = []
    for cookie in input_file:
        header_ = {"cookie": cookie}
        try:
            home_business = requests.get(
                'https://business.facebook.com/content_management',
                headers=header_
            ).text
            token = home_business.split('EAAG')[1].split('","')[0]
            cookie_token = f'{cookie}|EAAG{token}'
            tokens.append(cookie_token)
        except:
            pass
    return tokens

def share(tach, id_share):
    cookie, token = tach.split('|')
    try:
        requests.post(
            f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published=0&access_token={token}',
            headers={'cookie': cookie}
        )
    except:
        pass

def main_share(cookies, id_share, delay, total_share, chat_id=None):
    all_tokens = get_token(cookies)
    stt = 0
    for tach in all_tokens:
        if stt >= total_share:
            break
        stt += 1
        threading.Thread(target=share, args=(tach, id_share)).start()
        if chat_id:
            bot.send_message(chat_id, f"[{stt}] SHARE thành công → ID {id_share}")
        time.sleep(delay)
    if chat_id:
        bot.send_message(chat_id, "✅ Đã hoàn tất share!")

# =====================
# PHẦN BOT GỌI CODE
# =====================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Xin chào! Gõ lệnh /share để bắt đầu.\n\nCú pháp:\n/share <id_share> <delay> <total_share>")

@bot.message_handler(commands=['share'])
def handle_share(message):
    try:
        args = message.text.split()
        if len(args) < 4:
            bot.reply_to(message, "❌ Sai cú pháp!\nVí dụ: /share 123456 5 10")
            return
        id_share = args[1]
        delay = int(args[2])
        total_share = int(args[3])

        if not os.path.exists("cookies.txt"):
            bot.reply_to(message, "❌ Không tìm thấy file cookies.txt")
            return
        cookies = open("cookies.txt").read().split("\n")

        threading.Thread(target=main_share, args=(cookies, id_share, delay, total_share, message.chat.id)).start()
        bot.reply_to(message, f"🚀 Bắt đầu share ID {id_share} (delay {delay}s, tổng {total_share})")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi: {str(e)}")

print("🤖 Bot Telegram đang chạy...")
bot.polling(non_stop=True)
