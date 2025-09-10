import datetime
import logging
from typing import Any

from airflow.sdk import DAG
from airflow.sdk import Asset
from airflow.sdk import asset
from airflow.sdk import task

logger = logging.getLogger(__name__)


@asset(schedule=None)
def get_alpha_vantage_instruments() -> list[str]:
    """
    Fetch instrument list.
    """
    return ["AAPL", "GOOGL", "MSFT"]


@asset(schedule=None)
def get_raw_alpha_vantage_prices(symbol: str) -> dict[str, Any]:
    """
    Fetch historical stock prices from Alpha Vantage API.
    """
    return {"price": 101, "symbol": symbol}


with DAG(
    dag_id="transform_alpha_vantage_prices",
    schedule=None,
    start_date=datetime.datetime(2022, 3, 4, tzinfo=datetime.UTC),
) as dag:

    @task
    def get_price(symbol: str):
        return {"symbol": symbol, "price": 100}

    @task(outlets=[Asset("prices_stream")])
    def transform_prices(price, outlet_events):
        outlet_events[Asset("prices_stream")].extra = {price["symbol"]: price["price"] * 2}
        logger.info("Transformed price for %s, %s", price["symbol"], price["price"] * 2)

    prices = get_price.expand(symbol=[1, 2, 3])
    transform_prices.expand(price=prices)
