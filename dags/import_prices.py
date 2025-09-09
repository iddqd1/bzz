import json

import pendulum
from airflow.sdk import DAG
from airflow.sdk import asset
from airflow.sdk import dag
from airflow.sdk import task

# from alpha_vantage.timeseries import TimeSeries


@asset(schedule="*/1 * * * *")
def export_alpha_vantage_prices():

    # ts = TimeSeries(key="B6QSCN4N0QQBY91M")
    # # Get json object with the intraday data and another with  the call's metadata
    # data, meta_data = ts.get_daily("GOOGL")
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

        order_data_dict = json.loads(data_string)
        return order_data_dict

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

        print(f"Total order value is: {total_order_value:.2f}")

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
        print("Extracting data...")
        print(
            inlet_events[export_alpha_vantage_prices][
                -1
            ].source_task_instance.xcom_pull()
        )
        return {"test": "value"}

    @task()
    def dupa(*, inlet_events=None):
        print("Dupa task...")
        print(inlet_events)

    dupa()
    extract()


load_price_data()
