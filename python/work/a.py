from datetime import datetime, timedelta

import boto3
import base64
from botocore.exceptions import ClientError
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.hooks.aws_hook import AwsHook
import urllib.parse

default_args = {
    'owner': 'azaparozhtsa',
    'email': 'aliaksandr_zaparozhtsau@epam.com',
    'dependsOnPast': False,
    'start_date': datetime(2020, 2, 13, 6, 0, 0),
    'end_date': datetime(2020, 2, 13, 10, 0, 0),
    'email_on_failure': True,
    'email_on_retry': False,
    'email_on_success': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'aws_conn_id': 'AWS_dev',
    'provide_context': True}


def start_task__print_info(**context):
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


def start_task__get_secrets(**context):

    secret_name = "ftp_medallia"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = AwsHook(aws_conn_id=context['aws_conn_id']).get_session(region_name)
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the
    # 'GetSecretValue' API. See
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(e.response['Error'])
        return 1
    else:
        # Decrypts secret using the associated KMS CMK. Depending on
        # whether the secret is a string or binary, one of these fields
        # will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            print(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(decoded_binary_secret)

def start_task__first_try(**context):
    print("it message from first python task in my life")


def on_failure_function(context):
    print("there was failure... Sorry...")


with DAG("azaparozhtsa_bash_games",
          concurrency=1,
          catchup=True,
          schedule_interval="5 * * * *",
          default_args=default_args,
          on_failure_callback=on_failure_function) as dag:

    task_print_info = PythonOperator(
        task_id="print_info_task",
        python_callable=start_task__print_info,
        on_failure_callback=on_failure_function,
    )

    task_get_secrets = PythonOperator(
	task_id="get_secret_key",
	python_callable=start_task__get_secrets,
	on_failure_callback=on_failure_function
    )


task_get_secrets