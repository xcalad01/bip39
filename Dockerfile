FROM python:3.8

COPY backend_trezor /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "api.py"]