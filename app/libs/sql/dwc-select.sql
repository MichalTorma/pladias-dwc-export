SELECT
    CONCAT('BU-SAV:PLADIAS:', r.id) AS occurrenceID,
    t.name_lat AS scientificName,
    r.latitude AS decimalLatitude,
    r.longitude AS decimalLongitude,
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
    r.gps_coords_precision AS coordinateUncertaintyInMeters
FROM
    atlas.records AS r
        LEFT JOIN public.taxons AS t ON r.taxon_id = t.id
        LEFT JOIN atlas.projects AS p ON r.project_id = p.id
WHERE
    r.validation_status != 2
