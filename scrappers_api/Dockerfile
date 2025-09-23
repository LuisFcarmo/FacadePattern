FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install-deps
RUN playwright install chromium

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "80"]