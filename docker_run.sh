 sudo docker run -it -d \
   --restart always \
   -v /mnt/matrix/zhangyuhan/models:/models \
   -v /home/zhangyuhan/python_project/llamacpp-python/configs:/configs \
   -p 38501:8501 \
   mty:v1