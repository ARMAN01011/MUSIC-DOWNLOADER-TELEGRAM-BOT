import json
import logging
from telebot import types

logger = logging.getLogger(__name__)

STYLES = {
    'star': '★',
    'arrow': '➻',
    'flower': '✿',
    'crown': '♛',
    'infinity': '∞',
    'bullet': '├──',
    'sub': '│   ├──',
    'end': '└──'
}

def style_text(text):
    replacements = {
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ',
        'E': 'ᴇ', 'G': 'ɢ', 'H': 'ʜ',
        'I': 'ɪ', 'J': 'ᴊ', 'L': 'ʟ',
        'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ',
        'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ',
        'S': 's', 'T': 'ᴛ', 'Y': 'ʏ'
    }
    return ''.join([replacements.get(c.upper(), c) for c in text])

def load_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(user_data):
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

def check_membership(bot, user_id, CHANNEL_ID):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Membership check error: {str(e)}")
        return False

def main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(f"{STYLES['flower']} Contact Admin", callback_data='contact'))
    markup.row(types.InlineKeyboardButton(f"{STYLES['crown']} Go Premium", callback_data='premium'))
    return markup