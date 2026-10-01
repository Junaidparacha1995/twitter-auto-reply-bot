import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

# ===== CONFIG =====
TELEGRAM_REDACTED_SECRET_ASSIGNMENT =REDACTED_SECRET
CLAUDE_REDACTED_SECRET_ASSIGNMENT =REDACTED_SECRET

client = Anthropic(api_key=REDACTED_SECRET

# Track warnings
user_warnings = {}

# ===== CLAUDE CLASSIFIER =====
async def classify_message(text):

    prompt = f"""
You are a Telegram moderator for the Dark Pino crypto community.

Classify the message into ONE category:

SPAM - promoting other coins, scam links, referral links, fake investments, suspicious URLs, repeated emojis, aggressive shilling.
QUESTION - asking about Dark Pino, roadmap, buying, tokenomics, ecosystem.
NORMAL - casual conversation not related to Dark Pino.

Respond with ONLY one word:
SPAM
QUESTION
NORMAL

Message:
{text}
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=REDACTED_SECRET
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


# ===== CLAUDE REPLY GENERATOR =====
async def generate_reply(text):

    prompt = f"""
You are the official AI assistant for Dark Pino.

Dark Pino is a Solana-based ecosystem including wallet, AI automation, fitness app, casino, ShareFi, and real-world integrations.

Answer clearly and confidently in paragraph form.
Never give financial advice.
If asked about profits say:
We do not provide financial advice.

User question:
{text}
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=REDACTED_SECRET
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


# ===== MAIN HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    user_id = message.from_user.id
    text = message.text

    if not text:
        return

    result = await classify_message(text)

    if result == "SPAM":

        # Delete message
        await message.delete()

        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

        if user_warnings[user_id] >= 2:
            await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Spam detected. Please follow community rules."
            )

    elif result == "QUESTION":

        reply = await generate_reply(text)
        await message.reply_text(reply)

    else:
        pass  # ignore normal chat


# ===== RUN BOT =====
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Dark Pino Claude Moderator Running...")
app.run_polling()