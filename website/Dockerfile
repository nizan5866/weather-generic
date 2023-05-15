#syntax=docker/dockerfile:1
FROM python:3.10.10-alpine3.17

RUN pip install --upgrade pip
COPY . .
RUN pip install flask gunicorn requests
EXPOSE 5000
CMD ["gunicorn","-w","3","-b","0.0.0.0:5000","wsgi:app"]

