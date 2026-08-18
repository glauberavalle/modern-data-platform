select
    nullif(order_id, '') as order_id,
    nullif(customer_id, '') as customer_id,
    nullif(order_status, '') as order_status,
    cast(nullif(order_purchase_timestamp, '') as timestamp) as order_purchased_at,
    cast(nullif(order_approved_at, '') as timestamp) as order_approved_at,
    cast(nullif(order_delivered_carrier_date, '') as timestamp) as order_delivered_carrier_at,
    cast(nullif(order_delivered_customer_date, '') as timestamp) as order_delivered_customer_at,
    cast(nullif(order_estimated_delivery_date, '') as timestamp) as order_estimated_delivery_at
from {{ source('raw', 'olist_orders_dataset') }}
