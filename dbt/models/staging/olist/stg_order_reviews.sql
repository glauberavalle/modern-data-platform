select
    nullif(review_id, '') as review_id,
    nullif(order_id, '') as order_id,
    cast(nullif(review_score, '') as smallint) as review_score,
    nullif(review_comment_title, '') as review_comment_title,
    nullif(review_comment_message, '') as review_comment_message,
    cast(nullif(review_creation_date, '') as timestamp) as review_created_at,
    cast(nullif(review_answer_timestamp, '') as timestamp) as review_answered_at
from {{ source('raw', 'olist_order_reviews_dataset') }}
