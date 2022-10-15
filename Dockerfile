FROM apache/airflow:2.3.1

USER root
COPY requirements.txt .

USER airflow
RUN pip install --no-cache-dir -r requirements.txt
