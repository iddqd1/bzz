import logging
import os

import contracts
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
                    st.reporttype_id,
                    ic.id as instrument_configuration_id,
                    ic.auto_approve
                FROM
                    scraper_webpagescraperconfiguration s
                JOIN
                    scraper_instrumentconfiguration ic ON s.instrument_configuration_id=ic.id
                JOIN
                    mangle_instrument i ON ic.instrument_id=i.id
                JOIN scraper_webpagescraperconfiguration_report_types st
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
                "instrument_configuration_id": page["instrument_configuration_id"],
                "instrument_id": page["instrument_id"],
                "reporttype_id": page["reporttype_id"],
                "auto_approve": page["auto_approve"],
                "data": response.text,
            },  # extra has to be provided, can be {}
            alias=AssetAlias(f"asset-page-{page['reporttype_id']}"),
        )
        return page["url"]

    crawl_page.expand(
        page=instrument_urls.output,
    )  # pyright: ignore[reportUnusedExpression]


@dag(
    dag_display_name="Parse holdings page for holding data and save it",
    dag_id="parse_holding_data",
    schedule=AssetAlias(asset_page_holdings),
)
def extract_and_save_holding_data():
    save_scraped_data = SQLExecuteQueryOperator.partial(
        task_id="save_scraped_data",
        conn_id="bzz",
        max_active_tis_per_dagrun=3,
        sql="sql/save_scraped_data.sql",
    )

    @task(inlets=[AssetAlias(asset_page_holdings)])
    def extract_holding_data(*, inlet_events=None):
        page = inlet_events[AssetAlias(asset_page_holdings)][-1].extra
        response = get_gemini_analyzer(
            "holdings",
            os.getenv("GEMINI_API_KEY", ""),
        ).start_analyze(page["data"])
        return {
            "instrument_configuration_id": page["instrument_configuration_id"],
            "instrument_id": page["instrument_id"],
            "report_type_id": page["reporttype_id"],
            "approved": page["auto_approve"],
            "data": response,
            "raw_data": response,
            "data_hash": contracts.HoldingList.model_validate_json(response).data_hash,
        }

    data = extract_holding_data()  # pyright: ignore[reportUnusedExpression]
    save_scraped_data.expand(
        parameters=[data],
    )  # pyright: ignore[reportUnusedExpression]


extract_and_save_holding_data()


@dag(
    dag_display_name="Parse price page for price data and save it",
    dag_id="parse_price_data",
    schedule=AssetAlias(asset_page_price),
)
def extract_and_save_price_data():
    save_price_data = SQLExecuteQueryOperator.partial(
        task_id="save_price_data",
        conn_id="bzz",
        max_active_tis_per_dagrun=3,
        sql="sql/save_scraped_data.sql",
    )

    @task(inlets=[AssetAlias(asset_page_price)])
    def extract_price_data(*, inlet_events=None):
        page = inlet_events[AssetAlias(asset_page_price)][-1].extra
        response = get_gemini_analyzer(
            "price",
            os.getenv("GEMINI_API_KEY", ""),
        ).start_analyze(page["data"])
        if response is None:
            msg = (
                f"Failed to extract price data for "
                f"instrument_configuration_id={page['instrument_configuration_id']}, "
                f"instrument_id={page['instrument_id']}, "
                f"report_type_id={page['reporttype_id']}"
            )
            raise ValueError(msg)
        contracts.Price.model_validate_json(response)  # validate response
        return {
            "instrument_configuration_id": page["instrument_configuration_id"],
            "instrument_id": page["instrument_id"],
            "report_type_id": page["reporttype_id"],
            "data": response,
            "approved": page["auto_approve"],
            "raw_data": response,
            "data_hash": None,
        }

    data = extract_price_data()  # pyright: ignore[reportUnusedExpression]
    save_price_data.expand(parameters=[data])  # pyright: ignore[reportUnusedExpression]


extract_and_save_price_data()


@dag(
    dag_display_name="Load data to mangle",
    dag_id="load_data_to_mangle",
    schedule="*/5 * * * *",
)
def load_data_to_mangle():
    select_scraped_data = SQLExecuteQueryOperator(
        task_id="select_scraped_data",
        conn_id="bzz",
        max_active_tis_per_dagrun=3,
        sql="sql/select_scraped_data.sql",
    )

    @task
    def extract_data(row):
        logger.info(row)

    extract_data.expand(
        row=select_scraped_data.output,
    )  # pyright: ignore[reportUnusedExpression]


load_data_to_mangle()
