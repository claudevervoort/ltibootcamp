FROM python:latest

ADD ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
