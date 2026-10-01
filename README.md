# twiiter bot

A Python-based Twitter bot that interacts with followers and direct messages using AI-generated responses powered by the Anthropic Claude API.

## Overview

This project consists of Twitter automation scripts that manage follower engagement by following back new followers and sending personalized welcome messages. It uses the Claude AI model to generate friendly DM replies and answers user questions about a crypto project. Additionally, there is a Telegram moderation bot for community management, which classifies messages as spam, questions, or normal chat and responds accordingly.

## Features

- Automatically follows back new Twitter followers within safe hourly limits.
- Sends AI-generated welcome direct messages to new followers.
- Streams Twitter direct message events and replies to user queries via AI.
- Uses Claude AI models via the Anthropic API for generating natural, conversational text.
- Includes a Telegram bot to moderate chat, classify messages, and reply to relevant questions.
- Handles Twitter API authentication securely using environment variables.
- Implements rate limiting and logging for reliable operation.
- Stores processed user IDs in CSV files to avoid duplicate actions.

## Tech Stack

- Python 3
- Twitter API v1.1 & v2 (OAuth1 authentication)
- Anthropic Claude API for AI-generated text
- `requests` library for HTTP requests
- `requests_oauthlib` for OAuth1 authentication
- `python-dotenv` for managing environment variables
- `telegram` and `python-telegram-bot` libraries for Telegram bot integration
- CSV files for persistent storage of processed followers and messages
- Standard logging module for logs

## Folder Structure

- `bot.py` — Main Twitter bot managing followers and sending automated welcome DMs using Claude AI.
- `reply_bot.py` — Twitter DM stream listener that replies to incoming direct messages with AI-generated answers.
- `test.py` — Telegram bot script acting as a chat moderator and AI assistant for a Telegram crypto community.
- `.env` (not included) — Environment variables storing API keys and tokens.
- CSV files (`followers.csv`, `messages.csv`) — Used to track processed users and messages.
- `bot.log` — Log file recording runtime events and errors.

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install requests requests_oauthlib python-dotenv anthropic telegram python-telegram-bot
   ```
3. Create a `.env` file in the root directory with the following variables:
   ```
   X_USER_ID=your_twitter_user_id
   CONSUMER_KEY=your_twitter_consumer_key
   CONSUMER_SECRET=REDACTED_SECRET
   ACCESS_TOKEN=REDACTED_SECRET
   ACCESS_SECRET=REDACTED_SECRET
   CLAUDE_API_KEY=REDACTED_SECRET
   COIN_NAME=your_project_coin_name
   WEBSITE=your_project_website_url
   BLOCKCHAIN=your_project_blockchain
   TELEGRAM_TOKEN=REDACTED_SECRET
   ```
4. Adjust rate limits and settings if necessary within the scripts.

## Usage

- Run the main bot to manage followers and send welcome messages:
  ```bash
  python bot.py
  ```
- Run the reply bot to stream and respond to Twitter direct messages:
  ```bash
  python reply_bot.py
  ```
- Run the Telegram moderation bot:
  ```bash
  python test.py
  ```
- Monitor logs in `bot.log` and output on the console for status and errors.

## Status

This project is under active development. Features and implementations may evolve to improve interaction capabilities and integration with Twitter and Telegram APIs.