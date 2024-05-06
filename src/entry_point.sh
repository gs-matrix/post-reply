#!/bin/bash
# 运行 Python 脚本
streamlit run ./main.py --server.port=8501

# 启动 bash 会话
exec "$@"
