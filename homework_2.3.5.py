import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
Постройте столбчатую диаграмму
Постройте гистограмму с распределением числовой переменной
Постройте точечную диаграмму для двух числовых переменных
Постройте тепловую карту для двух категориальных переменных
Прокомментируйте для каждого графика, какие выводы можно по ним сделать?
'''

# # Example: Line
# x = [1,2,3,4,5]
# y = [10,20,30,40,50]
# plt.plot(x,y)
# plt.title('Линейный график')
# plt.xlabel('ОСЬ Х')
# plt.ylabel('ОСЬ У')
# plt.show()

# # Example2: Столбчатая диаграмма
# sizes = [35, 45]
# labels = ['A',  'O']


# Task 1: bar chart
city = pd.read_csv('Tables/city.csv', sep='|')

# города на А
matched_cities_a = city[city['city'].str.strip().str.startswith(('A', 'a'), na=False)]
count_city_a = len(matched_cities_a)

# города на B
matched_cities_b = city[city['city'].str.strip().str.startswith(('B', 'b'), na=False)]
count_city_b = len(matched_cities_b)

# города на C
matched_cities_c = city[city['city'].str.strip().str.startswith(('C', 'c'), na=False)]
count_city_c = len(matched_cities_c)

# Строим столбчатую диаграмму
sizes = [count_city_a, count_city_b, count_city_c]
labels = ['City A', 'City B', 'City C']
plt.bar(
    x = labels,
    height = sizes,
    bottom = 0,
    color=['red', 'green', 'blue'],
    edgecolor='black',
    linewidth=1.5,
    width=0.6)

for i in range(len(sizes)):
    plt.annotate(text = f'{sizes[i]}', xy = (labels[i], sizes[i]+1))
plt.tight_layout()
plt.show()


# Task 2: histogram
film = pd.read_csv('Tables/film.csv', sep='|')

plt.figure(figsize=(8, 5))
plt.hist(
    x=film['length'].dropna(),
    bins=10,
    color='orange',
    edgecolor='black')
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
plt.scatter(
    x=film['length'],
    y=film['rental_rate'],
    color='teal',
    edgecolors='black',
    alpha=0.7)
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
plt.imshow(rating_language, cmap='YlOrRd', aspect='auto')
plt.title('Количество фильмов по рейтингу и языку')
plt.xlabel('Идентификатор языка')
plt.ylabel('Рейтинг')
plt.xticks(
    ticks=np.arange(len(rating_language.columns)),
    labels=rating_language.columns)
plt.yticks(
    ticks=np.arange(len(rating_language.index)),
    labels=rating_language.index)
plt.colorbar(label='Количество фильмов')

for row_index in range(rating_language.shape[0]):
    for column_index in range(rating_language.shape[1]):
        plt.text(
            column_index,
            row_index,
            rating_language.iloc[row_index, column_index],
            ha='center',
            va='center')

plt.tight_layout()
plt.show()

'''
Вывод: самые светлые и самые темные ячейки показывают редкие и частые
сочетания рейтинга и языка; по таблице можно увидеть преобладающие категории.
'''