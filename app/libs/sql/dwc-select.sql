WITH temp_protection AS (
    SELECT taxons.id,
           CASE WHEN value != 200000 THEN TRUE
                ELSE FALSE END AS is_protected
    FROM public.taxons
        LEFT JOIN measurements.data_enum AS de ON taxons.id = de.taxon_id
    WHERE de.trait_id = 200001 AND entry_type = 1 AND is_enabled
)
SELECT
    CONCAT('BU-SAV:PLADIAS:', r.id) AS occurrenceID,
    t.name_lat AS scientificName,
    CASE WHEN is_protected THEN round(r.latitude * 100) / 100
        ELSE r.latitude END AS decimalLatitude,
    CASE WHEN is_protected THEN round(r.longitude * 100) / 100
         ELSE r.longitude END AS decimalLongitude,
    CASE
        WHEN r.datum_precision = 'Y' THEN TO_CHAR(r.datum, 'YYYY')
        WHEN r.datum_precision = 'M' THEN TO_CHAR(r.datum, 'YYYY-MM')
        WHEN r.datum_precision = 'D' THEN TO_CHAR(r.datum, 'YYYY-MM-DD')
        ELSE NULL
        END AS eventDate,
    r.locality,
    r.altitude_min AS minimumElevationInMeters,
    r.altitude_max AS maximumElevationInMeters,
    r.comment AS occurrenceRemarks,
    (
        SELECT string_agg(CASE WHEN a.name = '' THEN a.surname ELSE CONCAT(a.name, ' ', a.surname) END, '|')
        FROM atlas.records_authors
                 INNER JOIN atlas.authors AS a ON records_authors.authors_id = a.id
        WHERE records_id = r.id) AS recordedBy,
    r.source,
    r.environment,
    CASE
        WHEN r.validation_status IN (0, 1) THEN 'verification required'
        WHEN r.validation_status = 3 THEN 'verified'
        ELSE NULL
        END AS identificationVerificationStatus,
    r.original_name AS verbatimScientificName,
    CASE WHEN is_protected THEN NULL
         ELSE r.gps_coords_precision END AS coordinateUncertaintyInMeters,
    CASE WHEN is_protected THEN 0.01
         ELSE NULL END AS coordinatePrecision
FROM
    atlas.records AS r
        LEFT JOIN temp_protection AS tp ON r.taxon_id = tp.id
        LEFT JOIN public.taxons AS t ON r.taxon_id = t.id
        LEFT JOIN atlas.projects AS p ON r.project_id = p.id
WHERE
    r.validation_status != 2
