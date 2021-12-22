FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY service_to_yml .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
