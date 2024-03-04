CREATE VIEW darwin_core_extended_occurrence AS
SELECT
    r.id AS occurrenceID,
    t.scientific_name AS scientificName,
    r.latitude AS decimalLatitude,
    r.longitude AS decimalLongitude,
    r.datum AS eventDate,
    r.locality,
    r.altitude_min AS minimumElevationInMeters,
    r.altitude_max AS maximumElevationInMeters,
    r.comment AS occurrenceRemarks,
    ra.authors_id AS recordedByID, -- Assuming recorder's ID maps to an author in the authors table
    r.source,
    r.environment,
    r.project_id AS associatedSequences, -- Example of mapping project ID to associated sequences; adjust based on actual data mapping
    r.validation_status AS identificationVerificationStatus,
    r.original_name AS verbatimScientificName,
    r.gps_coords_precision AS coordinatePrecision,
    r.datum_precision AS verbatimEventDate,
    r.nearest_town_text AS locality,
    h.name AS habitat, -- Assuming habitat information is available in a related table
    r.phytochorion_id AS locationID -- Example of using phytochorion_id as a location ID
FROM
    atlas.records AS r
LEFT JOIN public.taxons AS t ON r.taxon_id = t.id
LEFT JOIN atlas.records_authors AS ra ON r.id = ra.records_id
LEFT JOIN atlas.herbariums AS h ON r.id = h.id -- This line is speculative; adjust based on actual data mapping
WHERE
    r.include_in_map = TRUE;
