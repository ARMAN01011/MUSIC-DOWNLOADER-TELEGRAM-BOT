import yt_dlp
import os
import re
import logging
from telebot import types
from helper import style_text, STYLES, save_data
from threading import Thread
import requests
import telebot
import time

logger = logging.getLogger(__name__)

def download_media(query, user_id, media_type):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", query).strip()
    ext = "mp3" if media_type == "audio" else "mp4"
    output_file = f"downloads/{safe_title}.{ext}"

    ydl_opts = {
        'outtmpl': f"downloads/{safe_title}.%(ext)s",
        'noplaylist': True,
        'quiet': True,
    }

    if media_type == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[height<=480][filesize<45M]+bestaudio/best[height<=480][filesize<45M]',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if not info:
                return None
            for file in os.listdir("downloads"):
                if file.startswith(safe_title) and file.endswith(f".{ext}"):
                    return f"downloads/{file}"
        return None
    except Exception as e:
        logger.error(f"Download error for {query}: {str(e)}")
        return None

def handle_download_choice(bot, call, media_type, query, user_data, data_lock, ADMIN_IDS, DAILY_FREE_LIMIT):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)

    with data_lock:
        user_entry = user_data.setdefault(str(user_id), {
            'downloads': 0,
            'premium': False,
            'last_reset': time.time(),
            'username': call.from_user.username
        })

        if time.time() - user_entry['last_reset'] > 86400:
            user_entry['downloads'] = 0
            user_entry['last_reset'] = time.time()
            save_data(user_data)

        if not user_entry['premium'] and user_entry['downloads'] >= DAILY_FREE_LIMIT and user_id not in ADMIN_IDS:
            bot.send_message(
                call.message.chat.id,
                f"{STYLES['star']} {style_text('DAILY LIMIT REACHED')}\n"
                f"{STYLES['arrow']} Free users: {DAILY_FREE_LIMIT} downloads/day\n"
                f"{STYLES['arrow']} Upgrade to premium",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(f"{STYLES['crown']} Go Premium", callback_data='premium')
                )
            )
            return

    search_msg = bot.send_message(
        call.message.chat.id,
        f"{STYLES['star']} {style_text('PROCESSING')}: {query} ({media_type.upper()})..."
    )

    def process_download():
        filename = None
        try:
            os.makedirs("downloads", exist_ok=True)
            filename = download_media(query, user_id, media_type)
            if not filename or not os.path.exists(filename):
                raise Exception("Download failed")

            file_size_mb = os.path.getsize(filename) / (1024 * 1024)
            logger.info(f"File {filename} size: {file_size_mb:.2f} MB")
            if file_size_mb > 18:
                raise Exception(f"File too large ({file_size_mb:.2f} MB). Max: 18 MB.")

            with open(filename, 'rb') as file:
                bot.delete_message(call.message.chat.id, search_msg.message_id)
                if media_type == "audio":
                    bot.send_audio(
                        call.message.chat.id,
                        file,
                        title=query,
                        performer="@Music_Downloader_HBF_Bot",
                        reply_to_message_id=call.message.message_id,
                        timeout=120
                    )
                else:
                    bot.send_video(
                        call.message.chat.id,
                        file,
                        caption=query,
                        reply_to_message_id=call.message.message_id,
                        timeout=120
                    )

            with data_lock:
                user_entry['downloads'] += 1
                save_data(user_data)

        except requests.exceptions.ConnectionError as ce:
            logger.error(f"Upload timeout for {query}: {str(ce)}")
            try:
                bot.edit_message_text(
                    f"{STYLES['star']} {style_text('UPLOAD FAILED')}\nConnection timed out. Try a smaller video or check your network.",
                    call.message.chat.id,
                    search_msg.message_id
                )
            except telebot.apihelper.ApiTelegramException as te:
                logger.warning(f"Failed to edit message: {str(te)}")
                bot.send_message(
                    call.message.chat.id,
                    f"{STYLES['star']} {style_text('UPLOAD FAILED')}\nConnection timed out. Try a smaller video or check your network."
                )
        except Exception as e:
            logger.error(f"Error for {query}: {str(e)}")
            try:
                bot.edit_message_text(
                    f"{STYLES['star']} {style_text('DOWNLOAD FAILED')}\n{str(e)}",
                    call.message.chat.id,
                    search_msg.message_id
                )
            except telebot.apihelper.ApiTelegramException as te:
                logger.warning(f"Failed to edit message: {str(te)}")
                bot.send_message(
                    call.message.chat.id,
                    f"{STYLES['star']} {style_text('DOWNLOAD FAILED')}\n{str(e)}"
                )
        finally:
            if filename and os.path.exists(filename):
                try:
                    os.remove(filename)
                    logger.info(f"Deleted temporary file: {filename}")
                except Exception as e:
                    logger.error(f"Failed to delete {filename}: {str(e)}")

    Thread(target=process_download).start()