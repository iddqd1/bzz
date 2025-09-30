
INSERT IGNORE INTO scraper_scrapeddata(
    created,
    modified,
    approved,
    approved_at,
    source_type,
    data,
    data_hash,
    raw_data,
    instrument_configuration_id,
    report_type_id)
VALUES (
    NOW(),
    NOW(),
    %(approved)s,
    CASE WHEN %(approved)s THEN NOW() ELSE NULL END,
    'scraper',
    %(data)s,
    %(data_hash)s,
    %(raw_data)s,
    %(instrument_configuration_id)s,
    %(report_type_id)s
);
