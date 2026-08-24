-- Первый запрос
SELECT
	i.film_id,
	COUNT(DISTINCT r.customer_id) AS unique_customers
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
GROUP BY i.film_id
ORDER BY unique_customers DESC
;

-- Второй запрос
SELECT
	i.film_id,
	SUM(p.amount) AS total_sum
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
GROUP BY i.film_id
ORDER BY total_sum
;

-- Третий запрос
SELECT
    i.film_id,
    AVG(r.return_date - r.rental_date) AS avg_rental_time
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
WHERE r.return_date IS NOT NULL
GROUP BY i.film_id
ORDER BY avg_rental_time DESC
;

-- Четвертый запрос
SELECT
    ROUND(
        AVG(
            CASE 
                WHEN (r.return_date - r.rental_date) > (f.rental_duration || ' days')::interval THEN 1 
                ELSE 0 
            END
        ) * 100, 2
    ) AS overall_overdue_percent
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NOT NULL
;

-- Пятый запрос
WITH rentals_with_film AS (
	-- привязываем фильм к прокатам 
    SELECT
        r.customer_id,
        i.film_id
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
),
customer_film_counts AS (
    -- Считаем, сколько раз каждый клиент брал какой-либо фильм
    SELECT
        customer_id,
        film_id,
        COUNT(*) AS times_rented
    FROM rentals_with_film
    GROUP BY customer_id, film_id
)
SELECT
    film_id,
    COUNT(customer_id) AS repeat_customers
FROM customer_film_counts
WHERE times_rented > 1
GROUP BY film_id
ORDER BY repeat_customers DESC
;
