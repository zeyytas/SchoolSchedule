FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
CMD celery -A app worker --loglevel=info
ADD school /app/
