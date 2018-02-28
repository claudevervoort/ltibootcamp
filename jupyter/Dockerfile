FROM python:latest

ADD ./ /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
