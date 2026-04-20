FROM python:3.11.9-slim

WORKDIR /mostrador

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]