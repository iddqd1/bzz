from django.db import models


class IntervalChoices(models.TextChoices):
    MINUTE = "minute", "Minute"
    HOURLY = "hourly", "Hourly"
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    BIWEEKLY = "biweekly", "Biweekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    YEARLY = "yearly", "Yearly"


class YieldIntervalChoices(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    YEARLY = "yearly", "Yearly"


class TimeZoneChoices(models.TextChoices):
    AMERICA_NEW_YORK = "America/New_York", "America/New_York"
    EUROPE_WARSAW = "Europe/Warsaw", "Europe/Warsaw"
    EUROPE_LONDON = "Europe/London", "Europe/London"
    EUROPE_BERLIN = "Europe/Berlin", "Europe/Berlin"
    ASIA_HONG_KONG = "Asia/Hong_Kong", "Asia/Hong_Kong"
    ASIA_SINGAPORE = "Asia/Singapore", "Asia/Singapore"
    ASIA_TOKYO = "Asia/Tokyo", "Asia/Tokyo"
    ASIA_SHANGHAI = "Asia/Shanghai", "Asia/Shanghai"
    Asia_KOLKATA = "Asia/Kolkata", "Asia/Kolkata"
    EUROPE_PARIS = "Europe/Paris", "Europe/Paris"
    UTC = "UTC", "UTC"


class StockExchangeChoices(models.TextChoices):
    NYSE = "NYSE", "NEW YORK STOCK EXCHANGE"
    NASDAQ = "NASDAQ", "NASDAQ"
    GPW = "GPW", "WARSAW STOCK EXCHANGE"
    SSE = "SSE", "SHANGHAI STOCK EXCHANGE"
    EURONEXT = "EURONEXT", "EURONEXT"
    JPX = "JPX", "JAPAN EXCHANGE GROUP"
    SZSE = "SZSE", "SHENZHEN STOCK EXCHANGE"
    HKEX = "HKEX", "HONG KONG EXCHANGES AND CLEARING"
    LSE = "LSE", "LONDON STOCK EXCHANGE"
    TSX = "TSX", "TORONTO STOCK EXCHANGE"
    BSE = "BSE", "BOMBAY STOCK EXCHANGE"
    SIX = "SIX", "SWISS EXCHANGE"
    ASX = "ASX", "AUSTRALIAN SECURITIES EXCHANGE"
    KRX = "KRX", "KOREA EXCHANGE"
    FSE = "FSE", "FRANKFURT STOCK EXCHANGE"
    SGX = "SGX", "SINGAPORE EXCHANGE"
    JSE = "JSE", "JOHANNESBURG STOCK EXCHANGE"
    TWSE = "TWSE", "TAIWAN STOCK EXCHANGE"
    B3 = "B3", "B3 - BRAZIL STOCK EXCHANGE"
    BMV = "BMV", "MEXICAN STOCK EXCHANGE"
    BME = "BME", "SPANISH STOCK EXCHANGES"


class ReportSourceChoices(models.TextChoices):
    ALPHA_VANTAGE = "alpha_vantage", "Alpha Vantage"
    BLOOMBERG = "bloomberg", "Bloomberg"
    IEX = "iex", "IEX"
    YAHOO_FINANCE = "yahoo_finance", "Yahoo Finance"
    EMAIL = "email", "Email"
