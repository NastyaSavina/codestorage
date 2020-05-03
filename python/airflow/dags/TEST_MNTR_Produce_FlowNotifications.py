import apdaghelper
from apdaghelper import *
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models.variable import Variable
import urllib.parse

dag_config = apdaghelper.get_config(__file__, 'dev_config.yaml')

with DAG(**dag_config['dag']) as dag:
    cfg = dag_config['task_run_jar']
    bash_command_=f"java -cp {cfg['jar_path']} {cfg['main_path']} {cfg['global_config_path']}"
    task_run_jar = BashOperator(
        task_id='task_run_jar',
        on_faiure_callback=ap_task_failure_callback,
        bash_command=bash_command_,
    )

task_run_jar

