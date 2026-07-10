# ── Stage 1: Builder ──────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ── Stage 2: Runner ───────────────────────────────────────
FROM python:3.12-slim AS runner

WORKDIR /app

# builder에서 설치된 패키지만 복사 (빌드 도구 제외)
COPY --from=builder /root/.local /root/.local
COPY ./app ./app
COPY ./static ./static

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
