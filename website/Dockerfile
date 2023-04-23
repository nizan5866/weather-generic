#syntax=docker/dockerfile:1
FROM python:3.10.10-alpine3.17

RUN pip install --upgrade pip
RUN adduser -D newuser
USER newuser
WORKDIR /home/newuser
COPY --chown=newuser:newuser requirements.txt requirements.txt
ENV PATH="/home/newuser/.local/bin:${PATH}"
RUN pip install --no-cache-dir --upgrade --user -r requirements.txt
COPY --chown=newuser:newuser . .
EXPOSE 5000
CMD ["gunicorn","-w","3","-b","0.0.0.0:5000","wsgi:app"]
