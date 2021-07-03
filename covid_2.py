import csv
from pygal.maps.world import COUNTRIES
import pygal #Необходимо скачать данную библиотеку

covid_dict = {}
popul_dict = {}
overall = []

### Ниже функция, которая читает CSV файл, собирает данные и формирует словарь {страна: цифры}

def read_data(filename, country, value, delimiter):
    data_dict = {}

    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers = next(reader)

        for row in reader:
            if row[country] not in data_dict.keys():
                try:
                    data_dict.update({row[country]:int(row[value])})
                except:
                    data_dict.update({row[country]:int(float(row[value])*1000)})
            else:
                try:
                    data_dict.update({row[country]:int(row[value])+data_dict.get(row[country])})
                except:
                    data_dict.update({row[country]:int(float(row[value])*1000)+data_dict.get(row[country])})

    return data_dict

covid_dict = read_data("06_29_21.csv", 3, 7, ",") #если данные не лежат в текущей папке, то необходимо указать полный путь
popul_dict = read_data("2021_data.csv", 1, 2, ",")

### создаем сводный словарь {страна, население, зараженные}

for country in popul_dict:
    if country in covid_dict.keys():
        overall.append({"country":country, "population":popul_dict.get(country), "covid":covid_dict.get(country)})


### в сводном словаре обновляем коды стран

with open("2021_data.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    headers = next(reader)

    for i in reader:
        for j in overall:
            if i[1] == j.get("country"):
                j.update({"code":i[0].lower()})

### формируем карту мира

wm = pygal.maps.world.World()
wm.title = '% зараженных от общего числа населения'

### создаем словари для нанесения данных на карту

pop_1 = {}
pop_2 = {}
pop_3 = {}

### считаем процент, добавляем в словарь в формате {код страны: процент}

for i in overall:
    count = (i.get("covid") * 100)/i.get("population")
    if count > 1:
        pop_1.update({i.get("code"):count})
    elif count <= 1 and count >= 0.5:
        pop_2.update({i.get("code"):count})
    else:
        pop_3.update({i.get("code"):count})

### наносим данные на карту

wm.add('> 1', pop_1)
wm.add('>= 0.5 <= 1', pop_2)
wm.add('< 0.5', pop_3)

### генерим векторную картинку в текущую папку

wm.render_to_file('world_covid_3.svg')
