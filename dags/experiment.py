import logging
import os

import pendulum
import requests
from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import DAG
from airflow.sdk import Asset
from airflow.sdk import AssetAlias
from airflow.sdk import Metadata
from airflow.sdk import task
from gemini import get_gemini_analyzer

os.environ["NO_PROXY"] = "*"

logger = logging.getLogger(__name__)

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
                    s.url, ic.instrument_id,
                    i.code,
                    st.scrapertype_id,
                    ic.id as instrumentconfiguration_id
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
    def crawl_page(page):
        session = requests.Session()
        session.trust_env = False
        response = session.get(page["url"], timeout=10)
        yield Metadata(
            asset=Asset(f"asset-crawling-{page['code']}"),
            extra={
                "instrument_id": page["instrument_id"],
                "scrapertype_id": page["scrapertype_id"],
                "data": response.text,
            },  # extra has to be provided, can be {}
            alias=AssetAlias(f"asset-page-{page['scrapertype_id']}"),
        )
        return page["url"]

    crawl_page.expand(page=instrument_urls.output)  # pyright: ignore[reportUnusedExpression]


@dag(
    dag_display_name="Parse page for holding data",
    dag_id="parse_holding_data",
    schedule=AssetAlias(asset_page_holdings),
)
def parse_holding_events():
    @task(inlets=[AssetAlias(asset_page_holdings)])
    def extract_holding_events(*, inlet_events=None):
        page = inlet_events[AssetAlias(asset_page_holdings)][-1].extra
        logger.info("Using Gemini to parse the page")
        response = get_gemini_analyzer("holdings", os.getenv("GEMINI_API_KEY", "")).start_analyze(page["data"])
        logger.info("Gemini response: %s", response)
        logger.info("*" * 20)

    extract_holding_events()  # pyright: ignore[reportUnusedExpression]


parse_holding_events()

with DAG(
    dag_display_name="Parse page for price data",
    dag_id="crawl_for_price_data",
    schedule=AssetAlias(asset_page_price),
):

    @task(inlets=[AssetAlias(asset_page_price)])
    def print_triggering_price_events(*, inlet_events=None):
        page = inlet_events[AssetAlias(asset_page_price)][-1].extra
        logger.info("Using Gemini to parse the page")
        response = get_gemini_analyzer("price", os.getenv("GEMINI_API_KEY", "")).start_analyze(page["data"])
        logger.info("Gemini response: %s", response)
        logger.info("*" * 20)

    print_triggering_price_events()  # pyright: ignore[reportUnusedExpression]
