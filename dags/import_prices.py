import json
import logging

import pendulum
from airflow.sdk import asset
from airflow.sdk import dag
from airflow.sdk import task

logger = logging.getLogger(__name__)


@asset(schedule="*/1 * * * *")
def export_alpha_vantage_prices():
    return {"price": 101}


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def tutorial_taskflow_api():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """

    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        return json.loads(data_string)

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        logger.info("Total order value is: %s", total_order_value)

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


tutorial_taskflow_api()


@dag(
    schedule=[export_alpha_vantage_prices],
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def load_price_data():
    @task(inlets=[export_alpha_vantage_prices])
    def extract(*, inlet_events=None):
        logger.info("Extracting data...")
        logger.info(
            inlet_events[export_alpha_vantage_prices][-1].source_task_instance.xcom_pull(),
        )
        return {"test": "value"}

    @task()
    def dupa(*, inlet_events=None):
        logger.info("Dupa task...")
        logger.info(inlet_events)

    dupa()
    extract()


load_price_data()
