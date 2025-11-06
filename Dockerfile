FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app /app/app

EXPOSE 5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "app/main.py"]

