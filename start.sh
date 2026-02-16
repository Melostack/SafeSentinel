#!/bin/bash
export PYTHONPATH=.
nohup python3 api/server.py > server.log 2>&1 &
nohup python3 bot/telegram_bot.py > bot.log 2>&1 &