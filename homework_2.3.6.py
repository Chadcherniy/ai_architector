import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

'''
Повторите графики из homework_2.3.5.py с помощью библиотеки seaborn:
- столбчатая диаграмма;
- гистограмма с распределением числовой переменной;
- точечная диаграмма для двух числовых переменных;
- тепловая карта для двух категориальных переменных.
'''

sns.set_theme(style='whitegrid')

# Task 1: bar chart
city = pd.read_csv('Tables/city.csv', sep='|')

matched_cities_a = city[city['city'].str.strip().str.startswith(('A', 'a'), na=False)]
matched_cities_b = city[city['city'].str.strip().str.startswith(('B', 'b'), na=False)]
matched_cities_c = city[city['city'].str.strip().str.startswith(('C', 'c'), na=False)]

bar_data = pd.DataFrame({
    'Группа': ['City A', 'City B', 'City C'],
    'Количество': [
        len(matched_cities_a),
        len(matched_cities_b),
        len(matched_cities_c),
    ],
})

plt.figure(figsize=(8, 5))
bar_plot = sns.barplot(
    data=bar_data,
    x='Группа',
    y='Количество',
    hue='Группа',
    palette=['red', 'green', 'blue'],
    edgecolor='black',
    linewidth=1.5,
    legend=False,
)
for container in bar_plot.containers:
    bar_plot.bar_label(container, padding=3)
plt.tight_layout()
plt.show()


# Task 2: histogram
film = pd.read_csv('Tables/film.csv', sep='|')

plt.figure(figsize=(8, 5))
sns.histplot(
    data=film,
    x='length',
    bins=10,
    color='orange',
    edgecolor='black',
)
plt.title('Распределение продолжительности фильмов')
plt.xlabel('Продолжительность, минут')
plt.ylabel('Количество фильмов')
plt.tight_layout()
plt.show()

'''
Вывод: большинство фильмов имеют среднюю продолжительность; очень коротких
и очень длинных фильмов заметно меньше.
'''


# Task 3: scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=film,
    x='length',
    y='rental_rate',
    color='teal',
    edgecolor='black',
    alpha=0.7,
)
plt.title('Зависимость стоимости аренды от продолжительности фильма')
plt.xlabel('Продолжительность, минут')
plt.ylabel('Стоимость аренды')
plt.tight_layout()
plt.show()

'''
Вывод: по расположению точек можно оценить, связана ли стоимость аренды
с продолжительностью фильма; плотность точек показывает наиболее частые сочетания.
'''


# Task 4: heatmap for two categorical variables
rating_language = pd.crosstab(film['rating'], film['language_id'])

plt.figure(figsize=(8, 5))
sns.heatmap(
    rating_language,
    cmap='YlOrRd',
    annot=True,
    fmt='g',
    cbar_kws={'label': 'Количество фильмов'},
)
plt.title('Количество фильмов по рейтингу и языку')
plt.xlabel('Идентификатор языка')
plt.ylabel('Рейтинг')
plt.tight_layout()
plt.show()

'''
Вывод: самые светлые и самые темные ячейки показывают редкие и частые
сочетания рейтинга и языка; по таблице можно увидеть преобладающие категории.
'''
