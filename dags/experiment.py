import logging

import pendulum
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import dag
from airflow.sdk import task

logger = logging.getLogger(__name__)


get_webpage_crawlers = SQLExecuteQueryOperator(
    task_id="get_webpage_crawlers",
    conn_id="bzz",
    sql="""
            SELECT
                s.url, i.instrument_id
            FROM
                scraper_webpagescraperconfiguration s
            JOIN
                scraper_instrumentconfiguration i ON s.instrument_configuration_id=i.id
            WHERE
                s.active=1
        """,
)


@dag(
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def crawl_webpage():
    @task()
    def extract(**kwargs):
        """# logger.info(
        #     inlet_events[get_webpage_crawlers][-1].source_task_instance.xcom_pull(),
        # )

        Returns:
            _type_: _description_
        """
        logger.info("Extracting data...")
        logger.info(kwargs)
        ti = kwargs["ti"]
        logger.info(ti.xcom_pull(task_ids="get_webpage_crawlers"))

        return {"test": "value"}

    get_webpage_crawlers >> extract()  # pyright: ignore[reportUnusedExpression]


crawl_webpage()


@dag(
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def crawl_webpages():
    @task()
    def get_data(data):
        logger.info("Extracting data...")
        logger.info(data)

    data = get_webpage_crawlers.execute(context={})
    logger.info("uuu %s", data)
    get_data(data=data)


crawl_webpages()
