select
    nullif(geolocation_zip_code_prefix, '') as geolocation_zip_code_prefix,
    cast(nullif(geolocation_lat, '') as numeric) as geolocation_lat,
    cast(nullif(geolocation_lng, '') as numeric) as geolocation_lng,
    nullif(geolocation_city, '') as geolocation_city,
    nullif(geolocation_state, '') as geolocation_state
from {{ source('raw', 'olist_geolocation_dataset') }}
