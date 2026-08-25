-- Первый Запрос
SELECT customer_id, COUNT(payment_id) AS total_payments
FROM payment
GROUP BY customer_id
ORDER BY total_payments DESC;

-- Второй Запрос на основе первого
SELECT
    customer_id,
    COUNT(payment_id) AS total_payments,
    CASE
        WHEN COUNT(payment_id) > 30 THEN 1
        ELSE 0
    END AS frequent_payer
FROM payment
GROUP BY customer_id
ORDER BY total_payments DESC;

-- Третий запрос
SELECT customer_id, SUM(amount) AS sum_amount
FROM payment
GROUP BY customer_id
ORDER BY sum_amount DESC;

-- Чтвертый запрос на основе третьего
WITH sums AS (
    SELECT customer_id, SUM(amount) AS sum_amount
    FROM payment
    GROUP BY customer_id
),
median_val AS (
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sum_amount) AS median_amount
    FROM sums
)
SELECT
    s.customer_id,
    s.sum_amount,
    CASE
        WHEN s.sum_amount > m.median_amount THEN 1
        ELSE 0
    END AS prospective_client
FROM sums s
CROSS JOIN median_val m
ORDER BY s.sum_amount DESC;
