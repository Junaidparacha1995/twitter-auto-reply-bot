import requests
import time
import os
import csv
import logging
import random
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
from anthropic import Anthropic

# ================= LOAD ENV =================
load_dotenv()

X_USER_ID = os.getenv("X_USER_ID").strip()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET =REDACTED_SECRET
ACCESS_TOKEN =REDACTED_SECRET
ACCESS_SECRET =REDACTED_SECRET
CLAUDE_API_KEY =REDACTED_SECRET

COIN_NAME = os.getenv("COIN_NAME")
WEBSITE = os.getenv("WEBSITE")
BLOCKCHAIN = os.getenv("BLOCKCHAIN")

# ================= AUTH =================
auth = OAuth1(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET
)

client = Anthropic(api_key=REDACTED_SECRET

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# ================= SAFE SETTINGS =================
MAX_DMS_PER_HOUR = 12
MAX_FOLLOWS_PER_HOUR = 15
MIN_DELAY = 30
MAX_DELAY = 75

dm_count = 0
follow_count = 0
hour_start = time.time()

# ================= CSV HELPERS =================
def load_ids(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        return {row[list(row.keys())[0]] for row in reader}

def save_id(filename, fieldname, value):
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[fieldname])
        if not file_exists:
            writer.writeheader()
        writer.writerow({fieldname: value})

# ================= SAFE REQUEST =================
def safe_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, auth=auth, timeout=20, **kwargs)
        if response.status_code >= 400:
            logging.warning(f"{method} {url} failed: {response.status_code} - {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None

# ================= X FUNCTIONS =================
def get_followers():
    url = f"https://api.twitter.com/2/users/{X_USER_ID}/followers"
    r = safe_request("GET", url)
    if r and r.status_code == 200:
        return r.json().get("data", [])
    return []

def follow_user(user_id):
    url = f"https://api.twitter.com/2/users/{X_USER_ID}/following"
    payload = {"target_user_id": user_id}
    safe_request("POST", url, json=payload)

def send_dm(user_id, text):
    text = text.replace("@", "")
    url = f"https://api.twitter.com/2/dm_conversations/with/{user_id}/messages"
    payload = {"text": text}
    safe_request("POST", url, json=payload)

def get_dms():
    url = "https://api.twitter.com/2/dm_events"
    r = safe_request("GET", url)
    if r and r.status_code == 200:
        return r.json().get("data", [])
    return []

# ================= CLAUDE =================
def generate_welcome():
    try:
        prompt = f"""
You are the official AI assistant for {COIN_NAME}.
Website: {WEBSITE}

Write a short friendly welcome message in plain text.
Do not use bullet points.
Do not use markdown.
Do not use special characters like *, -, or •.
Do not include usernames.
Do not include @mentions.
Do not sound promotional.
Keep it natural and conversational.
Encourage them to ask about the project and how to buy.
Never give financial advice.
Keep it under 60 words.
"""
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=REDACTED_SECRET
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        logging.error(f"Claude welcome error: {e}")
        return "Thanks for following. You can visit our website to learn more about the project."

def generate_coin_reply(question):
    try:
        prompt = f"""
You are the official AI assistant for {COIN_NAME}.
Website: {WEBSITE}
Blockchain: {BLOCKCHAIN}

Answer in plain conversational text.

Do not use bullet points.
Do not use markdown formatting.
Do not use special characters like *, -, or •.
Write in normal paragraphs.

Explain clearly what the project is, what it does, and how someone can buy it step by step in simple language.

Never give financial advice.
Never predict price.
If asked about profits respond with:
We do not provide financial advice. Please conduct your own research.

User question:
{question}
"""
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=REDACTED_SECRET
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        logging.error(f"Claude reply error: {e}")
        return "You can visit our official website for detailed information about the project."

# ================= MAIN LOOP =================
logging.info("Bot started with Safe Mode enabled.")

while True:
    try:
        if time.time() - hour_start > 3600:
            dm_count = 0
            follow_count = 0
            hour_start = time.time()
            logging.info("Hourly limits reset.")

        processed_followers = load_ids("followers.csv")
        processed_messages = load_ids("messages.csv")

        followers = get_followers()

        for user in followers:
            if follow_count >= MAX_FOLLOWS_PER_HOUR:
                logging.info("Follow hourly limit reached.")
                break

            user_id = user["id"]

            if user_id in processed_followers:
                continue

            logging.info("New follower detected.")

            follow_user(user_id)
            follow_count += 1

            if dm_count < MAX_DMS_PER_HOUR:
                welcome_msg = generate_welcome()
                send_dm(user_id, welcome_msg)
                dm_count += 1

            save_id("followers.csv", "user_id", user_id)

            delay = random.randint(MIN_DELAY, MAX_DELAY)
            logging.info(f"Sleeping {delay} seconds.")
            time.sleep(delay)

        dms = get_dms()

        for msg in dms:
            if dm_count >= MAX_DMS_PER_HOUR:
                logging.info("DM hourly limit reached.")
                break

            message_id = msg.get("id")
            if message_id in processed_messages:
                continue

            sender_id = msg.get("sender_id")
            text = msg.get("text")

            if not text:
                continue

            logging.info("Incoming DM detected.")

            reply = generate_coin_reply(text)
            send_dm(sender_id, reply)

            dm_count += 1
            save_id("messages.csv", "message_id", message_id)

            delay = random.randint(MIN_DELAY, MAX_DELAY)
            logging.info(f"Sleeping {delay} seconds.")
            time.sleep(delay)

        time.sleep(120)

    except Exception as e:
        logging.error(f"Main loop error: {e}")
        logging.info("Cooling down for 5 minutes.")
        time.sleep(300)