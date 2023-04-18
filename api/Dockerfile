FROM python:3.10

RUN echo '开始构建.............'

# 设置容器内的工作目录
WORKDIR /code


# 拷贝项目文件到容器目录
COPY . /code

# 设置时区
RUN rm -f /etc/localtime
RUN  ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8899

RUN echo '构建完成.............'

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port", "5006"]