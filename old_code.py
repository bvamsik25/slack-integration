
# @router.post("/slack/interactions")
# async def slack_interactions(request: Request):
#     data = await request.form()
#     slack_integration_service.slack_interaction(data)
#     return {"status": "ok"}



# def reply_message(channel_id, message):
#     """Send a message back to the Slack channel where the bot was mentioned."""
#     url = "https://slack.com/api/chat.postMessage"
#     headers = {"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
#     data = {"channel": channel_id, "text": message}
#
#     response = requests.post(url, headers=headers, json=data)
#     print("✅ Sent Reply:", response.json())
#
#
# def run_tests(test, test_number, updated_blockkit):
#     insert_index = 9 + (test_number * 2)
#     print(test, test_number)
#     capture_screenshots()
#     create_gif()
#     direct_image_url = upload_to_imgbb()
#     print('direct_image_url>>>', direct_image_url)
#
#     emulator_logs = get_emulator_logs()
#     updated_blockkit["blocks"][6]["text"]["text"] = f"```\n{emulator_logs}\n```"
#
#     if test_number == 0:
#         del updated_blockkit["blocks"][9]
#
#     updated_blockkit["blocks"].insert(insert_index, {
#         "type": "section",
#         "text": {
#             "type": "mrkdwn",
#             "text": test
#         }
#     })
#     updated_blockkit["blocks"].insert(insert_index + 1, {
#         "type": "image",
#         "image_url": direct_image_url,
#         "alt_text": "Android Emulator View"
#     })
#
#     print(updated_blockkit)
#     send_blockkit(updated_blockkit)