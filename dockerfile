FROM ubuntu:22.04

#设置非交互式环境变量以避免某些警告消息
ENV DEBIAN FRONTEND=noninteractive

#更新软件包列表
RUN apt-get update && \
    #安装build-essential包，包含gcc/g++和make等工具
    apt-get install -y build-essential && \
    #安装其他可能需要的C++库，比如libboost-all-dev(Boost库)
    apt-get install -y libboost-all-dev && \
    # 添加Python PPA
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    # 安装Python 3.10
    apt-get install -y python3.10 && \
    # 安装pip
    apt-get install -y python3-pip && \
    # 使用pip config命令设置镜像源
    python3.10 -m pip install --upgrade pip && \
    python3.10 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    # 使用pip安装Python包
    python3.10 -m pip install llama-cpp-python && \
    python3.10 -m pip install streamlit==1.32.2 && \
    python3.10 -m pip install streamlit_chatbox && \
    python3.10 -m pip install streamlit_option_menu && \
    python3.10 -m pip install pyyaml && \
    #清理不再需要的文件，减少镜像大小
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
#设置工作目录
WORKDIR /app

#将 C++源代码添加到容器中
COPY ./llama.cpp /app/llama.cpp
COPY ./src /app/src

RUN make -C /app/llama.cpp
RUN chmod +x /app/src/entry_point.sh


ENTRYPOINT [ "/app/src/entry_point.sh" ]

CMD ["bash"]