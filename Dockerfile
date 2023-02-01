FROM python:3.8
RUN apt update
RUN apt install python3-pip -y
RUN pip install flask
COPY . .
ENV FLASK_APP=flaskProject.py
ENV FLASK_ENV=development
# Expose the port on which the app will run
EXPOSE 5000
CMD ["flask", "run"]
