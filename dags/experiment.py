import logging
import os
from _scproxy import _get_proxy_settings

import pendulum
import requests
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import DAG
from airflow.sdk import Asset
from airflow.sdk import AssetAlias
from airflow.sdk import Metadata
from airflow.sdk import task

os.environ["NO_PROXY"] = "*"

logger = logging.getLogger(__name__)

_get_proxy_settings()


asset_page_price = "asset-page-price"
asset_page_holdings = "asset-page-holdings"


with DAG(
    dag_display_name="Crawl instrument pages",
    dag_id="crawl_pages",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
):
    instrument_urls = SQLExecuteQueryOperator(
        task_id="instrument_urls",
        conn_id="bzz",
        sql="""
                SELECT
                    s.url, ic.instrument_id, i.code, st.scrapertype_id
                FROM
                    scraper_webpagescraperconfiguration s
                JOIN
                    scraper_instrumentconfiguration ic ON s.instrument_configuration_id=ic.id
                JOIN
                    mangle_instrument i ON ic.instrument_id=i.id
                JOIN scraper_webpagescraperconfiguration_scraper_types st
                    ON s.id=st.webpagescraperconfiguration_id
                WHERE
                    s.active=1
            """,
    )

    @task(outlets=[AssetAlias(asset_page_price), AssetAlias(asset_page_holdings)])
    def crawl_page(page, outlet_events=None):
        session = requests.Session()
        session.trust_env = False
        response = session.get(page["url"], timeout=10)
        yield Metadata(
            asset=Asset(f"asset_crawling_star-{page['instrument_id']}"),
            extra={
                "instrument_id": page["instrument_id"],
                "scrapertype_id": page["scrapertype_id"],
                "data": response.text,
            },  # extra has to be provided, can be {}
            alias=AssetAlias(f"asset-page-{page['scrapertype_id']}"),
        )

    crawl_page.expand(page=instrument_urls.output)  # pyright: ignore[reportUnusedExpression]


with DAG(
    dag_display_name="Parse page for holding data",
    dag_id="crawl_for_holding_data",
    schedule=[AssetAlias(asset_page_holdings)],
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
):

    @task
    def print_triggering_asset_events(triggering_asset_events=None):
        logger.info(triggering_asset_events)
        for asset, asset_list in triggering_asset_events.items():
            logger.info(asset_list[0].extra)
            logger.info(asset, asset_list)
            logger.info(asset_list[0].source_dag_run.dag_id)

    print_triggering_asset_events()  # pyright: ignore[reportUnusedExpression]


with DAG(
    dag_display_name="Parse page for price data",
    dag_id="crawl_for_price_data",
    schedule=[AssetAlias(asset_page_price)],
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
):

    @task
    def print_triggering_price_events(triggering_asset_events=None):
        logger.info(triggering_asset_events)
        for asset, asset_list in triggering_asset_events.items():
            logger.info(asset_list[0].extra)
            logger.info(asset, asset_list)
            logger.info(asset_list[0].source_dag_run.dag_id)

    print_triggering_price_events()  # pyright: ignore[reportUnusedExpression]
