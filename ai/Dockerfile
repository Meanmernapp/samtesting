FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# PyTorch 2.8 avoids torchcodec; pin transformers for coqui-tts compatibility.
RUN pip install --no-cache-dir "torch>=2.8,<2.9" "torchaudio>=2.8,<2.9" \
    --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "transformers>=4.57.5,<5.1"

COPY app ./app
COPY run.py .

ENV COQUI_TOS_AGREED=1
ENV VOICEAI_DATA_DIR=/data
ENV VOICEAI_HOST=0.0.0.0

RUN mkdir -p /data/voices /data/generated

EXPOSE 8000

CMD ["python", "run.py"]
