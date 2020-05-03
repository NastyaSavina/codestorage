from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models.variable import Variable
import urllib.parse

default_args = {
    'owner': 'azaparozhtsa',
    'email': 'aliaksandr_zaparozhtsau@epam.com',
    'dependsOnPast': False,
    'start_date': datetime(2020, 3, 16, 8, 50, 0, tzinfo=timezone.utc),
    'end_date': datetime(2050, 3, 16, 8, 50, 0, tzinfo=timezone.utc),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'provide_context': True}


def tf__print_info(**context):
    task_id = context['task'].task_id
    dag_id = context['dag'].dag_id
    start_date = context['task'].start_date
    execution_date = context['ti'].execution_date

    log_url_params = {'execution_date': execution_date,
                      'task_id': task_id,
                      'dag_id': dag_id}

    log_usl = f"http://34.248.48.227:8080/admin/airflow/log?{urllib.parse.urlencode(log_url_params)}"

    print(f"     dag: {dag_id}")
    print(f"    task: {task_id}")
    print(f" log url: {log_usl}")
    print(f"      ts: {start_date}")


def on_failure_function(**context):
    print(f"[DAG][{context['dag_id']}] Is on beta development stage now... \n"
          f"If you found this failure repeats few times, please, notify aliaksandr_zaparozhtsau@epam.com\n\n\n")


with DAG(dag_id="Testing_MNTR_FlowNotification",
         concurrency=1,
         catchup=False,
         schedule_interval="0 */2 * * *",
         default_args=default_args,
         on_failure_callback=on_failure_function) as dag:

    task_print_info = PythonOperator(
        task_id="print_info",
        python_callable=tf__print_info,
        on_failure_callback=on_failure_function,
    )

    cfg = Variable.get("MNTR_Config", deserialize_json=True)
    task_run_jar = BashOperator(
        task_id="mntr_run",
        bash_command=f"java -cp {cfg['jar_path']} {cfg['main_class']} {cfg['global_config_path']}"
    )

task_print_info >> task_run_jar

