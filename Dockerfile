FROM python:3.10
COPY . /bitforecast
WORKDIR /bitforecast/deployment
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --preload --bind 0.0.0.0:$PORT --pythonpath deployment app:app
