-- Анализ выручки по фильмам: топ‑позиции, доля в общем объёме и категоризация популярности
SELECT
    title,
    film_revenue,
    ROUND(film_revenue * 100.0 / total_revenue, 2) AS revenue_share_percent,
    CASE
        WHEN revenue_rank <= 3 THEN 'Топ'
        ELSE 'Обычная'
    END AS popularity
FROM (
    SELECT
        f.title,
        SUM(p.amount) AS film_revenue,
        SUM(SUM(p.amount)) OVER () AS total_revenue,
        ROW_NUMBER() OVER (ORDER BY SUM(p.amount) DESC) AS revenue_rank
    FROM payment p
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON fc.film_id = f.film_id
    GROUP BY f.film_id, fc.film_id
) sub
WHERE film_revenue > 100
ORDER BY film_revenue DESC;
