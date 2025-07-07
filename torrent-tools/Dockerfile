# /homelab/torrent-tools/dockerfiles/recheck/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Build context'i olan /torrent-tools dizinine göre doğru yolu ver
COPY dockerfiles/recheck/recheck.py /app/recheck.py

# Build context'i olan /torrent-tools dizinine göre doğru yolu ver
COPY .env /app/.env

RUN pip install requests python-dotenv

CMD ["python", "recheck.py"]