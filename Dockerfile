FROM python:3.8.0-alpine
WORKDIR /sayhello

RUN    apk update -f \
    && apk upgrade \
    && apk --no-cache add -f tzdata \
    && rm -rf /var/cache/apk/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]