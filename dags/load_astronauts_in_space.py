from datetime import datetime, timedelta
import os
from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.http.operators.http import SimpleHttpOperator


ENV = os.getenv("ENV", "dev")
DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": "2022-10-13",
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
}
with DAG(
    dag_id=f"{ENV}-astronauts_in_space-v1.0",
    description="This job fetches information of astronauts in space",
    default_args=DEFAULT_ARGS,
    schedule_interval="*/30 * * * *",
    max_active_runs=1,
    catchup=False,
    tags=["apis"],
) as dag:
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")
    run_endpoint = SimpleHttpOperator(
        task_id="run_endpoint",
        endpoint="astros.json",
        # base url is http://api.open-notify.org/
        method="GET",
        http_conn_id=f'http_{ENV}',
        log_response=True,
    )

    start >> run_endpoint >> end
