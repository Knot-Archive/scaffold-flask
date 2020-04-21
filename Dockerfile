FROM python:3.6-slim
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV FLASK_CONF docker_compose
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install pqi && pqi use aliyun && pip install -r requirements.txt
COPY . /app
EXPOSE 8001
WORKDIR /app
ENTRYPOINT ["bash","entrypoint.sh"]

