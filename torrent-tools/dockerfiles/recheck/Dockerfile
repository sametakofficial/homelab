FROM python:3.10-slim

WORKDIR /app

COPY recheck.py /app/recheck.py
COPY ../../.env /app/.env  # .env dosyasını kopyala (opsiyonel)

RUN pip install requests python-dotenv

CMD ["python", "recheck.py"]
