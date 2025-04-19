from helper import style_text, STYLES, save_data
import logging

logger = logging.getLogger(__name__)

def is_admin(user_id, ADMIN_IDS):
    return user_id in ADMIN_IDS

def handle_broadcast(bot, message, user_data, data_lock, ADMIN_IDS):
    if not is_admin(message.from_user.id, ADMIN_IDS):
        return

    msg = message.text.replace('/broadcast', '').strip()
    if not msg:
        bot.reply_to(message, f"{STYLES['arrow']} Usage: /broadcast message")
        return

    with data_lock:
        users = user_data.keys()
        total = len(users)
        success = 0

    for user_id in users:
        try:
            bot.send_message(user_id, f"{STYLES['star']} {style_text('ANNOUNCEMENT')}\n{msg}")
            success += 1
        except Exception as e:
            logger.error(f"Broadcast failed to {user_id}: {e}")

    bot.reply_to(message,
        f"{STYLES['star']} Broadcast Results\n"
        f"{STYLES['sub']} Total users: {total}\n"
        f"{STYLES['end']} Successfully sent: {success}")

def list_users(bot, message, user_data, data_lock, ADMIN_IDS):
    if not is_admin(message.from_user.id, ADMIN_IDS):
        return

    with data_lock:
        free_users = [u for u in user_data.values() if not u['premium']]
        premium_users = [u for u in user_data.values() if u['premium']]

    response = (f"{STYLES['crown']} {style_text('USER STATISTICS')}\n"
                f"{STYLES['bullet']} Total Users: {len(user_data)}\n"
                f"{STYLES['sub']} Free Users: {len(free_users)}\n"
                f"{STYLES['sub']} Premium Users: {len(premium_users)}\n"
                f"{STYLES['end']} Daily Limit: {DAILY_FREE_LIMIT}")
    
    bot.reply_to(message, response)

def approve_user(bot, message, user_data, data_lock, ADMIN_IDS):
    if not is_admin(message.from_user.id, ADMIN_IDS):
        return

    try:
        target_id = int(message.text.split()[1])
        with data_lock:
            if str(target_id) in user_data:
                user_data[str(target_id)]['premium'] = True
                save_data(user_data)
                bot.send_message(target_id,
                    f"{STYLES['crown']} {style_text('PREMIUM ACCESS GRANTED')}\n"
                    f"You now have unlimited downloads!")
                bot.reply_to(message, f"{STYLES['star']} User approved")
            else:
                bot.reply_to(message, f"{STYLES['star']} User not found")
    except:
        bot.reply_to(message, f"{STYLES['arrow']} Usage: /approve user_id")

def remove_premium(bot, message, user_data, data_lock, ADMIN_IDS):
    if not is_admin(message.from_user.id, ADMIN_IDS):
        return

    try:
        target_id = int(message.text.split()[1])
        with data_lock:
            if str(target_id) in user_data:
                user_data[str(target_id)]['premium'] = False
                save_data(user_data)
                bot.send_message(target_id,
                    f"{STYLES['star']} {style_text('PREMIUM ACCESS REMOVED')}\n"
                    f"You are now on free plan")
                bot.reply_to(message, f"{STYLES['star']} Premium removed")
            else:
                bot.reply_to(message, f"{STYLES['star']} User not found")
    except:
        bot.reply_to(message, f"{STYLES['arrow']} Usage: /remove user_id")