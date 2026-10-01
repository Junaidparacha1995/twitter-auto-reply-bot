import os
import json
import requests
from dotenv import load_dotenv
from anthropic import Anthropic
from requests_oauthlib import OAuth1

load_dotenv()

# ===============================
# OAuth1 Setup
# ===============================
auth = OAuth1(
    os.getenv("CONSUMER_KEY"),
    os.getenv("CONSUMER_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_SECRET")
)

# ===============================
# Claude Setup
# ===============================
anthropic = Anthropic(api_key=REDACTED_SECRET

X_USER_ID = os.getenv("X_USER_ID")

# ===============================
# Send DM Function
# ===============================
def send_dm(recipient_id, text):
    url = "https://api.twitter.com/1.1/direct_messages/events/new.json"

    safe_text = text.encode("utf-8", "ignore").decode("utf-8")

    payload = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": recipient_id},
                "message_data": {"text": safe_text}
            }
        }
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=auth
    )

    print("Reply Status:", response.status_code)
    print("Reply Body:", response.text)


# ===============================
# Claude Reply Generator
# ===============================
def generate_reply(user_message):

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=REDACTED_SECRET
        messages=[{
            "role": "user",
            "content": f"""
You are the official AI assistant for DarkPino.

Website: https://darkpino.xyz/

Answer the user question clearly and confidently.
If they ask how to buy, give step-by-step instructions.

User message:
{user_message}
"""
        }]
    )

    return response.content[0].text


# ===============================
# STREAM DM EVENTS
# ===============================
def stream_dms():

    url = "https://api.twitter.com/2/dm_events/stream"

    print("🚀 Starting DM stream...")

    with requests.get(url, auth=auth, stream=True) as response:
        if response.status_code != 200:
            print("Stream error:", response.status_code)
            print(response.text)
            return

        for line in response.iter_lines():
            if line:
                decoded = json.loads(line.decode("utf-8"))
                print("Incoming:", decoded)

                if "data" in decoded:
                    event = decoded["data"]

                    if event.get("sender_id") != X_USER_ID:

                        user_message = event.get("text")

                        if user_message:
                            print("Message:", user_message)

                            reply = generate_reply(user_message)
                            send_dm(event["sender_id"], reply)


# ===============================
# RUN STREAM
# ===============================
if __name__ == "__main__":
    stream_dms()