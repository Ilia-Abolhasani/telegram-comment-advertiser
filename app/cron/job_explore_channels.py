from app.util.DotDict import DotDict
from app.cron import job_lock
from tqdm import tqdm


def start(context, telegram_api, logger_api):
    global job_lock
    with job_lock:
        channels = context.get_all_channel()
        channels = [
            DotDict({
                "is_public": 1,
                "username": "dahom_ch",
                "chat_id": None
            })
        ]
        for channel in tqdm(channels):
            try:
                if (not channel.chat_id):
                    if (channel.is_public):
                        chat_id = telegram_api.search_public_chat(
                            channel.username)
                        if (not chat_id):
                            raise Exception(
                                f"public channel username '{channel.username}' not found!")
                        channel.chat_id = chat_id
                    else:
                        raise Exception("private channel without chat_id!")
                if (channel.is_public):
                    telegram_api.search_public_chat(channel.username)
                messages, last_message_id = telegram_api.channel_history(
                    int(channel.chat_id), 500, channel.last_id)
                print(messages)
            except Exception as error:
                logger_api.announce(
                    error, f"Job fetch new proxy erro at channel_id {channel.id}.")
