FROM python:3.10.4

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
EXPOSE 8000
CMD ["python", "run.py"]