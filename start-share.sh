#!/usr/bin/env bash
PORT=5500
# start python server in background
python3 serve.py $PORT &
PY_PID=$!
# give it a second
sleep 0.7
# start ngrok (user must have ngrok installed and authenticated)
ngrok http $PORT
# when ngrok exits, kill python server
kill $PY_PID 2>/dev/null || true
