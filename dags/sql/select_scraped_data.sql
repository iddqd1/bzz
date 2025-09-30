SELECT
    sd.approved_at,
    sd.data,
    sd.report_type_id,
    sd.created,
    i.code,
    i.id AS instrument_id
FROM
    scraper_scrapeddata sd
JOIN
    scraper_instrumentconfiguration ic ON sd.instrument_configuration_id = ic.id
JOIN
    mangle_instrument i ON ic.instrument_id = i.id
WHERE
    sd.approved_at IS NOT NULL
    AND sd.approved_at > '{{prev_start_date_success or "1970-01-01 00:00:00"}}'
    AND sd.approved=1
ORDER BY
    sd.approved_at DESC
