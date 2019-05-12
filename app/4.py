# Импортируем библиотеку для парсинга JSON
from json import loads
# используем библиотеку Flask
from flask import Flask
from flask import render_template
# Импортируем функцию для преобразования компаратора в ключ для сортировки
from functools import cmp_to_key


# Компаратор для сортивки, сравнивает два объекта, полученных из JSON
def compare(x, y):
    # Сравниваем дистанцию
    if x["distance"] < y["distance"]:
        return 1
    elif x["distance"] > y["distance"]:
        return -1
    else:
        #  Сравниваем цену
        if x["price"] < y["price"]:
            return 1
        elif x["price"] > y["price"]:
            return -1
        else:
            # Сравниваем рейтинг
            if x["rating"] > y["rating"]:
                return 1
            elif x["rating"] < y["rating"]:
                return -1
            else:
                # Проверяем наличие 3D сеанса
                if x["3D"] and not y["3D"]:
                    return 1
                else:
                    return -1


# инициализируем приложение Flask
app = Flask(__name__)


# объект, описывающий фильм
class Film:
    def __init__(self, num, film_name, cinema_name, start_time, image, distance, price, rating, film3d):
        self.filmID = num
        self.filmName = film_name
        self.cinemaName = cinema_name
        self.startTime = start_time
        self.price = price
        self.image = image
        self.filmRating = rating
        self.film3d = film3d
        self.distance = distance


# обрабатываем корневой запрос
@app.route('/')
def index():
    # возвращаем html страницу, заполненную данными
    return render_template('index.html', films=films)


# если запущен файл, считываем JSON
if __name__ == "__main__":
    with open(r'static/movie-sessions-full.json', encoding='UTF-8') as f:
        json_str = f.read()
        json_array = loads(json_str, encoding='UTF-8')
        # Сортируем список по компаратору в порядке убывания
        json_array = sorted(json_array, key=cmp_to_key(compare), reverse=True)
        films = []
        count = 1
        for i in json_array:
            # заполняем список films
            new_film = Film(count, i['filmName'], i['cinemaName'], i['startTime'], i['image'], i['distance'], i['price'], i['rating'],
                            i['3D'])
            films.append(new_film)
            count += 1
    # запускаем сервер на порте 8080
    app.run('127.0.0.1', 8080)
