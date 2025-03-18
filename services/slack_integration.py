import asyncio
import json
import threading
import time

import blockkit_json
import config
from services import slack_service
from services import emulator_service
from services import events_store
from services.emulator_service import start_ui_test, stop_ui_test
from services.screen_record import capture_multiple_screenshots, create_gif, upload_to_imgbb


def send_homepage(blockkit=blockkit_json.BLOCKKIT_JSON):
    return slack_service.send_blockkit(payload={
        "user_id": config.SLACK_USER_ID,
        "view": json.dumps(blockkit)
    })


async def slack_interaction(payload):
    if "challenge" in payload:
        return {"challenge": payload["challenge"]}

    if "event" in payload:
        event = payload["event"]
        event_ts = event.get("ts")
        user_id = event["user"]
        channel_id = event["channel"]
        text = event["text"]
        thread_ts = event.get("thread_ts")
        bot_id = payload.get("authorizations", [{}])[0].get("user_id")

        if user_id == bot_id:
            print("Ignoring bot's own message to prevent infinite loop")
            return {"status": "bot's message in thread is ignored"}

        if event["type"] == "app_mention" and not thread_ts:
            thread_ts = event["ts"]
            await start_test_thread(channel_id, user_id, thread_ts)

        elif thread_ts:
            if event_ts in events_store.processed_events:
                print(f"Duplicate event detected: {event_ts}, ignoring it.")
                return {"status": "duplicate ignored"}

            events_store.processed_events.add(event_ts)
            events_store.save_processed_events()
            text_list = text.strip().split("\n")
            await process_test_steps(text_list, channel_id, thread_ts)

    return {"status": "ok"}


async def process_test_steps(text_list, channel_id, thread_ts):
    for text in text_list:
        # Create threads
        ui_thread = threading.Thread(target=run_ui_automation)
        screenshot_thread = threading.Thread(target=run_screenshot_capture)

        # Start both threads
        ui_thread.start()
        screenshot_thread.start()

        # Wait for both to complete
        ui_thread.join()
        screenshot_thread.join()
        emulator_logs = emulator_service.get_emulator_logs()
        await reply_in_thread(channel_id, thread_ts, f"✅ Executed: {text}", config.IMAGE_URL, emulator_logs)
        await asyncio.sleep(1.5)


def run_ui_automation():
    print("Starting UI Automation...")
    start_ui_test()
    time.sleep(config.NUM_SCREENSHOTS * config.INTERVAL + 5)
    stop_ui_test()
    print("UI Automation Completed.")


def run_screenshot_capture():
    print("Starting Screenshot Capture...")
    screenshot_files = capture_multiple_screenshots(config.NUM_SCREENSHOTS, config.INTERVAL)
    if screenshot_files:
        create_gif(screenshot_files, config.GIF_OUTPUT_PATH)
    upload_to_imgbb()
    print("Screenshot Capture & GIF Creation Completed.")


async def start_test_thread(channel_id, user_id, thread_ts):
    await slack_service.post_slack_message(data={
        "channel": channel_id,
        "thread_ts": thread_ts,
        "text": f"👋 Hey <@{user_id}>, let's start testing! \n\n"
                f"📝 Send steps one by one or multiple in a message (new lines). \n\n"
                f"🔄 I'll execute them in order & share results!"
    })


async def reply_in_thread(channel_id, thread_ts, message, direct_image_url, emulator_logs):
    data = {
        "channel": channel_id,
        "thread_ts": thread_ts,
        "text": message,
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{message}*"}
            },
            {
                "type": "image",
                "image_url": direct_image_url,
                "alt_text": "Automation Test Result"
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "📜 *Execution Logs:*"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"```\n{emulator_logs}\n```"}
            },
        ]
    }
    await slack_service.post_slack_message(data)
