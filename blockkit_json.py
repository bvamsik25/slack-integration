BLOCKKIT_JSON = {
    "type": "home",
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📱 Mobile Automation Tester",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Automate your mobile testing workflow directly from Slack with Drizz AI."
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "📜 *Live Logs*"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Logs will appear here."
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "block_id": "log_output",
            "text": {
                "type": "mrkdwn",
                "text": "```\nWaiting for logs...\n```"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🤖 *Android Emulator*"
            }
        },
        {
            "type": "image",
            "image_url": "https://media.geeksforgeeks.org/wp-content/uploads/20230225190834/android-emulator.png",
            "alt_text": "Android Emulator View"
        },
        {
            "type": "input",
            "block_id": "test_script_input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "script_input",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Type your test script here..."
                }
            },
            "label": {
                "type": "plain_text",
                "text": "📝 Enter Test Script"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "▶ Run Test"
                    },
                    "style": "primary",
                    "action_id": "run_test"
                }
            ]
        }
    ]
}
