/* Basic Queries */
SELECT * FROM public.company;
SELECT * FROM public.ship;
SELECT * FROM public.landpad;
SELECT * FROM public.launch;
SELECT * FROM public.satellite;

/* Company Info */
SELECT
    json_data->>'headquarters' AS headquarters,
    json_data->>'employees' AS num_employees,
    json_data->>'valuation' AS valuation
FROM public.company
;

/* Lightest & Heaviest Ships */
WITH
lightest AS (
    SELECT
        json_data->>'name' AS ship_name,
        (json_data->>'mass_kg')::int AS ship_mass_kg,
        'Lightest' AS label
    FROM public.ship
    ORDER BY ship_mass_kg ASC NULLS LAST
    LIMIT 1
),
heaviest AS (
    SELECT
        json_data->>'name' AS ship_name,
        (json_data->>'mass_kg')::int AS ship_mass_kg,
        'Heaviest' AS label
    FROM public.ship
    ORDER BY ship_mass_kg DESC NULLS LAST
    LIMIT 1
)
SELECT * FROM lightest
UNION ALL
SELECT * FROM heaviest
;

/* Landing Pad Locations */
SELECT
    json_data->>'full_name' AS landpad_name,
    json_data->>'locality' AS landpad_locality,
    json_data->>'region' AS landpad_region,
    json_data->>'latitude' AS landpad_latitude,
    json_data->>'longitude' AS landpad_longitude
FROM public.landpad
;