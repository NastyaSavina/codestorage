import urllib.parse
import json
import yaml
import boto3
import base64

from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from pathlib import Path
from zipfile import ZipFile
from airflow.exceptions import AirflowException
from airflow.hooks.activemq_hook import ActiveMQWebHook
from airflow.contrib.hooks.aws_hook import AwsHook
from botocore.exceptions import ClientError

aws_connection_id = 'AWS_dev'
amq_connection_id = 'ActiveMQConnection'
airflow_log_url = 'https://airflow-dev.ap.burberry.com:8080/admin/airflow/log?'


def get_config(dag_zip, yaml_filename):
    zip = Path(dag_zip).parent
    contents = ZipFile(zip).read(yaml_filename)
    config_json = yaml.safe_load(contents)
    return json.loads(json.dumps(config_json, default=str))


def create_done_flag(s3_bucket, target_dir, date):
    print("Creating done flag in bucket: {0}, dir: {1} for date: {2} ".format(s3_bucket, target_dir, date))
    s3_hook = S3Hook(aws_conn_id=aws_connection_id)
    print("Using S3 connection: ", s3_hook.aws_conn_id)
    s3_hook.load_string(
        string_data="",
        bucket_name=s3_bucket,
        key=target_dir + "/" + date,
        replace=True)
    print("Done flag created!")


def create_done_flag_by_key(done_key):
    print("Creating done flag by key: ", done_key)
    s3_hook = S3Hook(aws_conn_id=aws_connection_id)
    print("Using S3 connection: ", s3_hook.aws_conn_id)
    s3_hook.load_string(string_data="", key=done_key, replace=True)
    print("Done flag created!")


def print_failure_trace(context):
    print('ts: ' + context['ts'])
    print('dag: ' + context['dag'].dag_id)
    print('task: ' + context['task'].task_id)
    print('owner' + context['dag'].owner)
    print('operator: ' + context['task_instance'].operator)
    print('run_id: ' + context['run_id'])
    params = {'execution_date': context['ts'],
              'task_id': context['task'].task_id,
              'dag_id': context['dag'].dag_id}
    print('log url: ' + airflow_log_url + urllib.parse.urlencode(params))


def ap_task_failure_callback(context):
    err_info = 'Not available'
    if 'exception' in context:
        ex = context['exception']
        err_info = '{0}.{1}: {2}'.format(ex.__class__.__module__, ex.__class__.__name__, str(ex))

    print_failure_trace(context)

    ex = context['exception']
    if ex is not None:
        print('exception: {0}.{1}: {2}'.format(ex.__class__.__module__, ex.__class__.__name__, str(ex)))
        jms_hook = ActiveMQWebHook(http_conn_id=amq_connection_id,
                                   dag_id=context['dag'].dag_id,
                                   task_id=context['task'].task_id,
                                   execution_date=context['ts'],
                                   owner=context['dag'].owner,
                                   email=context['task'].email,
                                   error_details=err_info)
    jms_hook.execute()
    print('Custom failure callback: finished')


def get_secret(secret_name, region_name):
    global secret_json
    print('Preparing to extract ', secret_name)

    session = AwsHook(aws_conn_id=aws_connection_id).get_session(region_name)
    print('AWS session established ', session)

    client = session.client(
        service_name='secretsmanager',
    )
    print('Secrets manager client initialized ', client)
    print('Trying to access secret via client')
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    print('Received secret response result: ', get_secret_value_response)
    secret = ''
    if 'SecretString' in get_secret_value_response:
        secret_json = get_secret_value_response['SecretString']
        print('SECRET_JSON:', secret_json)
    else:
        secret_json = base64.b64decode(get_secret_value_response['SecretBinary'])
        print('SECRET_JSON:', secret_json)
    secret = json.loads(secret_json)

    print('Extracted secret: ', secret)
    return secret
