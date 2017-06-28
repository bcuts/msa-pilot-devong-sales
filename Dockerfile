FROM python:2.7
MAINTAINER Joonhyeok Scott Im <itanoss@gmail.com>
EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
