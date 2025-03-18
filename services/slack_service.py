import ssl

import aiohttp
import certifi
import requests
import config

HEADERS = {"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
ssl_context = ssl.create_default_context(cafile=certifi.where())


async def post_slack_message(data):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.post(config.SLACK_POST_MSG, headers=HEADERS, json=data) as response:
            await response.json()


def send_blockkit(payload):
    headers = {"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}", "Content-Type": "application/json; charset=utf-8"}
    response = requests.post(config.SLACK_WEBHOOK_URL, headers=headers, json=payload)
    return response
