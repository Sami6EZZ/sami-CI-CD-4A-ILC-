FROM python:3.8
RUN apt update
RUN apt install python3-pip -y
RUN pip install flask
COPY . .
ENV FLASK_APP=flask.py
ENV FLASK_ENV=development
# le port de l'execution du flask
EXPOSE 5000
CMD ["flask", "run"]
