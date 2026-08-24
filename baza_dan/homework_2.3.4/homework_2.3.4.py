import pandas as pd
import numpy as np


# 2. Загрузка
# Оказывается нужно еще правильно выгрузить данные
payment       = pd.read_csv('payment.csv',       sep='|')
rental        = pd.read_csv('rental.csv',        sep='|')
inventory     = pd.read_csv('inventory.csv',     sep='|')
film          = pd.read_csv('film.csv',          sep='|')
film_category = pd.read_csv('film_category.csv', sep='|')

# Пришлось удалить ненужную колонку last_update т.к. мешает merge
for df in [payment, rental, inventory, film, film_category]:
    if 'last_update' in df.columns:
        df.drop(columns=['last_update'], inplace=True)

# Приведение ключей к общему виду (строке)
for df in [payment, rental, inventory, film, film_category]:
    if 'rental_id' in df.columns:
        df['rental_id'] = df['rental_id'].astype(str)
    if 'inventory_id' in df.columns:
        df['inventory_id'] = df['inventory_id'].astype(str)
    if 'film_id' in df.columns:
        df['film_id'] = df['film_id'].astype(str)

# 3. JOIN-ы
df = (
    payment
    .merge(rental,        on='rental_id',    how='inner')
    .merge(inventory,     on='inventory_id', how='inner')
    .merge(film,          on='film_id',      how='inner')
    .merge(film_category, on='film_id',      how='inner')
)

# 4. GROUP BY + SUM
film_revenue = (
    df.groupby(['film_id', 'title'], as_index=False)['amount']
      .sum()
      .rename(columns={'amount': 'film_revenue'})
)

# 5. Оконные функции (OVER)
total_revenue = film_revenue['film_revenue'].sum()
film_revenue['total_revenue'] = total_revenue

film_revenue = film_revenue.sort_values('film_revenue', ascending=False).reset_index(drop=True)
film_revenue['revenue_rank'] = np.arange(1, len(film_revenue) + 1)

# 6. WHERE film_revenue > 100
film_revenue = film_revenue[film_revenue['film_revenue'] > 100]

# 7. ROUND
film_revenue['revenue_share_percent'] = np.round(
    film_revenue['film_revenue'] * 100.0 / film_revenue['total_revenue'], 2
)

# 8. CASE WHEN
film_revenue['popularity'] = np.where(
    film_revenue['revenue_rank'] <= 3, 'Топ', 'Обычная'
)

# 9. Финальная выборка
result = film_revenue[[
    'title',
    'film_revenue',
    'revenue_share_percent',
    'popularity'
]].sort_values('film_revenue', ascending=False).reset_index(drop=True)

print(result)
