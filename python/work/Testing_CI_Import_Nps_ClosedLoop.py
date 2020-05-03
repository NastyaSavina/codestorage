from apdaghelper import *
import json

from airflow import DAG
from airflow.contrib.operators.databricks_operator import DatabricksSubmitRunOperator
from airflow.contrib.hooks.aws_hook import AwsHook

dag_config = apdaghelper.get_config(__file__, "config.yaml")

def create_done_flag(context):
    done_path = dag_config['done_dir'] + context['ds']
    creaet_done_flag_by_key(done_path)
    print("Done flag created: " + done_path)


def get_secret_string(aws_conn_id_, service_name_, region_name_, SecretId_):
    session = AwsHook(aws_conn_id=aws_conn_id_).get_session()

    cli = session.client(
        service_name=service_name_,
        region_name=region_name_,
    )

    secret_responce = cli.get_secret_value(
        SecretId=SecretId_
    )

    if 'SecretString' in secret_responce:
        secret_string = secret_responce['SecretString']
    else:
        secret_string = base64.b64decode(secret_responce['SecretBinary'])

    return secret


with DAG(**dag_config['dag']) as dag:
    secret_string = get_secret_string(**dag_config['aws'])
    secret = json.loads(secret_string)
    prepare_directory = DatabricksSubmitRunOperator(
        task_id = 'prepare_directory',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_prepare_directory']
    )
    
    get_files_from_ftp = DatabricksSubmitRunOperator(
        task_id = 'get_files_from_ftp',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json={**dag_config['notebook_get_files_from_ftp'], **secret}
    )

    process_data = DatabricksSubmitRunOperator(
        task_id = 'process_data',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        on_success_callback=create_done_flag,
        json=dag_config['notebook_process_data']
    )


prepare_directory >> get_files_from_ftp >> process_data
