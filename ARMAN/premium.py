from helper import style_text, STYLES
from dotenv import load_dotenv
import os

load_dotenv()
PREMIUM_PRICE = os.getenv("PREMIUM_PRICE")

def show_premium_info(bot, message):
    premium_msg = f"""
{STYLES['crown']} {style_text('PREMIUM SUBSCRIPTION')} {STYLES['crown']}

{STYLES['bullet']} Price: {PREMIUM_PRICE}
{STYLES['bullet']} Benefits:
{STYLES['sub']} Unlimited downloads
{STYLES['sub']} Priority support
{STYLES['sub']} Audio & Video downloads
{STYLES['sub']} Faster processing

{STYLES['end']} Contact admin to upgrade: @PB_X01
    """
    bot.send_message(message.chat.id, premium_msg)