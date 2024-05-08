#!/bin/bash

echo "Starting my service..."
# 运行 Python 脚本
cd /app/src
streamlit run ./main.py --server.port=8501
