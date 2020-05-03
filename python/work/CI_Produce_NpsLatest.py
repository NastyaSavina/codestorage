import apdaghelper
from apdaghelper import *

from airflow import dag
from airflow.contrib.operators.databricks_operator import DatabricksSubmitRunOperator
from airflow.operators.python_operator import PythonOperator

dag_config = apdaghelper.get_config(__file__, "config.yaml")


def task_create_done_flag(context):
    done_dir = dag_config['done_dir'] + context['ds_nodash']
    apdaghelper.create_done_flag_by_key(done_dir)
    

with DAG(**dag_config['defauit_args']) as dag:
    check_done_flags = DatabricksSubmitRunOperator(
        task_id='check_done_flags',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_check_done_flags']
    )

    cl_produce_latest_view = DatabricksSubmitRunOperator(
        task_id='cl_produce_latest_view',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_cl_produce_latest_view']
    )

    cl_append_comments = DatabricksSubmitRunOperator(
        task_id='cl_append_comment',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_append_closed_loop_comments']
    )

    oo_produce_latest_view = DatabricksSubmitRunOperator(
        task_id='oo_produce_latest_view',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_oo_produce_latest_view']
    )

    oo_append_comments = DatabricksSubmitRunOperator(
        task_id='oo_append_comments',
        databrkcis_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_append_opt_out_comments']
    )

    id_produce_latest_view = DatabricksSubmitRunOperator(
        task_id='id_produce_latest_view',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_id_produce_latest_view']
    )

    id_append_comments = DatabricksSubmitRunOperator(
        task_id='id_append_comments',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=['notebook_append_invite_data_comment']
    )

    sd_produce_latest_view = DatabricksSubmitRunOperator(
        task_id='sd_produce_latest_view',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_sd_produce_latest_view']
    )

    sd_append_comment = DatabricksSubmitRunOperator(
        task_id='sd_append_comments',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=['notebook_append_survey_data_comment']
    )

    ta_produce_latest_view = DatabricksSubmitRunOperator(
        task_id='ta_produce_latest_view',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=dag_config['notebook_ta_produce_latest_view']
    )

    ta_append_comment = DatabricksSubmitRunOperator(
        task_id='ta_append_comment',
        databricks_conn_id=dag_config['databricks_conn_id'],
        on_failure_callback=ap_task_failure_callback,
        json=['notebook_appen_text_analytics_comment']
    )

    create_done_flag = PythonOperator( 
        task_id='create_done_flag',
        python_callable=task_create_done_flag,
        on_failure_callback=ap_task_failure_callback,
    )
