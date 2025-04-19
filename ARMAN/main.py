import telebot
import os
from CREDITS import credit
import logging
from dotenv import load_dotenv
from music import handle_download_choice
from helper import load_data, check_membership, style_text, main_markup, STYLES
from premium import show_premium_info
from all import handle_broadcast, list_users, approve_user, remove_premium
from threading import Lock

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
DAILY_FREE_LIMIT = int(os.getenv("DAILY_FREE_LIMIT"))
PREMIUM_PRICE = os.getenv("PREMIUM_PRICE")

bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
data_lock = Lock()

user_data = load_data()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        send_authorized_welcome(message)
        return
    if not check_membership(bot, user_id, CHANNEL_ID):
        bot.send_message(
            message.chat.id,
            f"{STYLES['star']} {style_text('PRIVATE CHANNEL REQUIRED')}\n"
            f"{STYLES['arrow']} Join our private channel\n"
            f"{STYLES['arrow']} Contact admin for access",
            reply_markup=main_markup()
        )
        return
    send_authorized_welcome(message)

def send_authorized_welcome(message):
    welcome_msg = f"""
{STYLES['crown']} {style_text('MUSIC & VIDEO DOWNLOADER')} {STYLES['crown']}

{STYLES['bullet']} {STYLES['star']} {style_text('FEATURES')}
{STYLES['sub']} MP3 & MP4 Downloads
{STYLES['sub']} High Quality Media
{STYLES['sub']} Fast Processing

{STYLES['bullet']} {STYLES['star']} {style_text('USAGE')}
{STYLES['sub']} Send song/video name
{STYLES['end']} Choose audio or video
    """
    bot.send_message(message.chat.id, welcome_msg, reply_markup=main_markup())

@bot.message_handler(commands=['help'])
def send_help(message):
    help_msg = f"""
{STYLES['crown']} {style_text('HELP - MUSIC & VIDEO DOWNLOADER')} {STYLES['crown']}

{STYLES['bullet']} {STYLES['star']} {style_text('ABOUT')}
{STYLES['sub']} This bot allows you to download music (MP3) and videos (MP4) from YouTube.
{STYLES['sub']} Exclusive access for private channel members.
{STYLES['sub']} Free users: {DAILY_FREE_LIMIT} downloads/day. Premium: Unlimited!

{STYLES['bullet']} {STYLES['star']} {style_text('HOW TO USE')}
{STYLES['sub']} Send a song or video name (e.g., "Shape of You").
{STYLES['sub']} Choose "Audio" or "Video" from the options.
{STYLES['sub']} Wait for the bot to process and send your file.
{STYLES['sub']} Videos are limited to ~45 MB (480p) for free users.

{STYLES['bullet']} {STYLES['star']} {style_text('COMMANDS')}
{STYLES['sub']} /start - Start the bot and see features.
{STYLES['sub']} /help - Show this help message.
{STYLES['sub']} Admin-only: /broadcast, /users, /approve, /remove.

{STYLES['bullet']} {STYLES['star']} {style_text('PREMIUM BENEFITS')}
{STYLES['sub']} Unlimited daily downloads.
{STYLES['sub']} Priority support and faster processing.
{STYLES['sub']} Contact admin (@PB_X01) to upgrade for {PREMIUM_PRICE}.

{STYLES['end']} {style_text('NEED HELP?')} Use the buttons below!
    """
    bot.send_message(message.chat.id, help_msg, reply_markup=main_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'contact':
        bot.answer_callback_query(call.id, "Contact @PB_X01")
    elif call.data == 'premium':
        show_premium_info(bot, call.message)
    elif call.data.startswith('download_'):
        _, media_type, query = call.data.split('_', 2)
        handle_download_choice(bot, call, media_type, query, user_data, data_lock, ADMIN_IDS, DAILY_FREE_LIMIT)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if not check_membership(bot, user_id, CHANNEL_ID):
        send_welcome(message)
        return

    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🎵 Audio", callback_data=f"download_audio_{message.text}"),
        telebot.types.InlineKeyboardButton("🎥 Video", callback_data=f"download_video_{message.text}")
    )
    bot.send_message(
        message.chat.id,
        f"{STYLES['star']} {style_text('CHOOSE FORMAT')}: {message.text}",
        reply_markup=markup
    )

print ("\n======================================\n\nBᴏᴛ Is Rᴜɴɴɪɴɢ 😎")
if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    bot.infinity_polling()