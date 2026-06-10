from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

lada_data = {
    "vesta": {
        "name": "LADA Vesta",
        "years": "2015 — настоящее время",
        "image": "https://avatars.mds.yandex.net/get-autoru-vos/18005086/8eb1b3458c30a5d3d7aba220d7585bdb/1200x900",
        "description": "Седан и универсал семейного класса. Один из самых популярных автомобилей LADA в России.",
        "parts": [
            {"id": "v001", "name": "Масляный фильтр", "category": "Фильтры", "price": 350, "article": "V-001-OF", "in_stock": True, "image": "https://cdn1.ozone.ru/s3/multimedia-6/6417369102.jpg"},
            {"id": "v002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 420, "article": "V-002-AF", "in_stock": True},
            {"id": "v003", "name": "Топливный фильтр", "category": "Фильтры", "price": 580, "article": "V-003-FF", "in_stock": True},
            {"id": "v004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 1200, "article": "V-004-BP", "in_stock": True},
            {"id": "v005", "name": "Комплект тормозных колодок задних", "category": "Тормозная система", "price": 950, "article": "V-005-BPR", "in_stock": True},
            {"id": "v006", "name": "Тормозной диск передний", "category": "Тормозная система", "price": 1800, "article": "V-006-BD", "in_stock": True},
            {"id": "v007", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 890, "article": "V-007-SP", "in_stock": True},
            {"id": "v008", "name": "Ремень ГРМ", "category": "Двигатель", "price": 2100, "article": "V-008-TB", "in_stock": False},
            {"id": "v009", "name": "Ролик натяжной ГРМ", "category": "Двигатель", "price": 1500, "article": "V-009-TR", "in_stock": True},
            {"id": "v010", "name": "Амортизатор передний", "category": "Подвеска", "price": 3200, "article": "V-010-SF", "in_stock": True},
            {"id": "v011", "name": "Амортизатор задний", "category": "Подвеска", "price": 2800, "article": "V-011-SR", "in_stock": True},
            {"id": "v012", "name": "Шаровая опора", "category": "Подвеска", "price": 650, "article": "V-012-BJ", "in_stock": True},
            {"id": "v013", "name": "Рычаг передний левый", "category": "Подвеска", "price": 2400, "article": "V-013-AL", "in_stock": True},
            {"id": "v014", "name": "Рычаг передний правый", "category": "Подвеска", "price": 2400, "article": "V-014-AR", "in_stock": True},
            {"id": "v015", "name": "Фара передняя левая", "category": "Оптика", "price": 4500, "article": "V-015-HL", "in_stock": True},
            {"id": "v016", "name": "Фара передняя правая", "category": "Оптика", "price": 4500, "article": "V-016-HR", "in_stock": False},
            {"id": "v017", "name": "Бампер передний", "category": "Кузов", "price": 6800, "article": "V-017-FB", "in_stock": True},
            {"id": "v018", "name": "Капот", "category": "Кузов", "price": 12000, "article": "V-018-HD", "in_stock": True},
            {"id": "v019", "name": "Радиатор охлаждения", "category": "Охлаждение", "price": 8900, "article": "V-019-RAD", "in_stock": True},
            {"id": "v020", "name": "Вентилятор радиатора", "category": "Охлаждение", "price": 3500, "article": "V-020-FAN", "in_stock": True},
        ]
    },
    "granta": {
        "name": "LADA Granta",
        "years": "2011 — настоящее время",
        "image": "https://autokovrik.ru/trumbsImages/5ed69b53c6e49b6a0839bd8ae8a26df5/413797e831588b8ab78177da9007883f_980x_0_90.jpg",
        "description": "Бюджетный седан, хэтчбек и универсал. Самый доступный автомобиль в линейке LADA.",
        "parts": [
            {"id": "g001", "name": "Масляный фильтр", "category": "Фильтры", "price": 280, "article": "G-001-OF", "in_stock": True},
            {"id": "g002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 350, "article": "G-002-AF", "in_stock": True},
            {"id": "g003", "name": "Салонный фильтр", "category": "Фильтры", "price": 320, "article": "G-003-CF", "in_stock": True},
            {"id": "g004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 950, "article": "G-004-BP", "in_stock": True},
            {"id": "g005", "name": "Тормозной диск передний", "category": "Тормозная система", "price": 1500, "article": "G-005-BD", "in_stock": True},
            {"id": "g006", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 650, "article": "G-006-SP", "in_stock": True},
            {"id": "g007", "name": "Ремень генератора", "category": "Двигатель", "price": 450, "article": "G-007-AB", "in_stock": True},
            {"id": "g008", "name": "Помпа водяная", "category": "Охлаждение", "price": 1800, "article": "G-008-WP", "in_stock": True},
            {"id": "g009", "name": "Термостат", "category": "Охлаждение", "price": 550, "article": "G-009-TH", "in_stock": True},
            {"id": "g010", "name": "Амортизатор передний", "category": "Подвеска", "price": 2200, "article": "G-010-SF", "in_stock": True},
            {"id": "g011", "name": "Амортизатор задний", "category": "Подвеска", "price": 1900, "article": "G-011-SR", "in_stock": True},
            {"id": "g012", "name": "Сайлентблок переднего рычага", "category": "Подвеска", "price": 280, "article": "G-012-SB", "in_stock": True},
            {"id": "g013", "name": "Ступица передняя", "category": "Подвеска", "price": 3200, "article": "G-013-HB", "in_stock": True},
            {"id": "g014", "name": "ШРУС наружный", "category": "Привод", "price": 1800, "article": "G-014-CV", "in_stock": True},
            {"id": "g015", "name": "Пыльник ШРУСа", "category": "Привод", "price": 350, "article": "G-015-BC", "in_stock": True},
            {"id": "g016", "name": "Фара передняя левая", "category": "Оптика", "price": 3200, "article": "G-016-HL", "in_stock": True},
            {"id": "g017", "name": "Зеркало боковое левое", "category": "Кузов", "price": 1800, "article": "G-017-MR", "in_stock": False},
            {"id": "g018", "name": "Дверь передняя левая", "category": "Кузов", "price": 8500, "article": "G-018-DL", "in_stock": True},
        ]
    },
    "niva": {
        "name": "LADA Niva / Niva Travel",
        "years": "1977 — настоящее время",
        "image": "https://avatars.mds.yandex.net/get-autoru-vos/2113863/0ac83e0fd6aca4d6e07053c5f7c34e21/1200x900",
        "description": "Легендарный внедорожник с полным приводом. Неприхотливый и проходимый автомобиль для любых условий.",
        "parts": [
            {"id": "n001", "name": "Масляный фильтр", "category": "Фильтры", "price": 250, "article": "N-001-OF", "in_stock": True},
            {"id": "n002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 300, "article": "N-002-AF", "in_stock": True},
            {"id": "n003", "name": "Топливный фильтр", "category": "Фильтры", "price": 400, "article": "N-003-FF", "in_stock": True},
            {"id": "n004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 850, "article": "N-004-BP", "in_stock": True},
            {"id": "n005", "name": "Комплект тормозных колодок задних (барабан)", "category": "Тормозная система", "price": 600, "article": "N-005-BPR", "in_stock": True},
            {"id": "n006", "name": "Тормозной цилиндр передний", "category": "Тормозная система", "price": 750, "article": "N-006-WC", "in_stock": True},
            {"id": "n007", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 550, "article": "N-007-SP", "in_stock": True},
            {"id": "n008", "name": "Карбюратор", "category": "Двигатель", "price": 8500, "article": "N-008-CB", "in_stock": True},
            {"id": "n009", "name": "Распределитель зажигания (трамблёр)", "category": "Двигатель", "price": 3200, "article": "N-009-DI", "in_stock": True},
            {"id": "n010", "name": "Амортизатор передний", "category": "Подвеска", "price": 1800, "article": "N-010-SF", "in_stock": True},
            {"id": "n011", "name": "Амортизатор задний", "category": "Подвеска", "price": 1600, "article": "N-011-SR", "in_stock": True},
            {"id": "n012", "name": "Рессора задняя", "category": "Подвеска", "price": 2200, "article": "N-012-SL", "in_stock": True},
            {"id": "n013", "name": "Шаровая опора верхняя", "category": "Подвеска", "price": 450, "article": "N-013-BJU", "in_stock": True},
            {"id": "n014", "name": "Шаровая опора нижняя", "category": "Подвеска", "price": 450, "article": "N-014-BJL", "in_stock": True},
            {"id": "n015", "name": "Редуктор переднего моста", "category": "Трансмиссия", "price": 15000, "article": "N-015-FR", "in_stock": False},
            {"id": "n016", "name": "Карданный вал передний", "category": "Трансмиссия", "price": 8500, "article": "N-016-DS", "in_stock": True},
            {"id": "n017", "name": "Передний бампер", "category": "Кузов", "price": 4500, "article": "N-017-FB", "in_stock": True},
            {"id": "n018", "name": "Крыло переднее левое", "category": "Кузов", "price": 3200, "article": "N-018-FL", "in_stock": True},
        ]
    },
    "xray": {
        "name": "LADA XRAY",
        "years": "2016 — настоящее время",
        "image": "https://i.pinimg.com/originals/76/b6/08/76b6089afcadaba85c438a3a2d671209.jpg",
        "description": "Компактный кроссовер с повышенной проходимостью и современным дизайном.",
        "parts": [
            {"id": "x001", "name": "Масляный фильтр", "category": "Фильтры", "price": 380, "article": "X-001-OF", "in_stock": True},
            {"id": "x002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 450, "article": "X-002-AF", "in_stock": True},
            {"id": "x003", "name": "Салонный фильтр", "category": "Фильтры", "price": 380, "article": "X-003-CF", "in_stock": True},
            {"id": "x004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 1350, "article": "X-004-BP", "in_stock": True},
            {"id": "x005", "name": "Комплект тормозных колодок задних", "category": "Тормозная система", "price": 1100, "article": "X-005-BPR", "in_stock": True},
            {"id": "x006", "name": "Тормозной диск передний", "category": "Тормозная система", "price": 2100, "article": "X-006-BD", "in_stock": True},
            {"id": "x007", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 950, "article": "X-007-SP", "in_stock": True},
            {"id": "x008", "name": "Катушка зажигания", "category": "Двигатель", "price": 2800, "article": "X-008-CI", "in_stock": True},
            {"id": "x009", "name": "Ремень ГРМ", "category": "Двигатель", "price": 2400, "article": "X-009-TB", "in_stock": True},
            {"id": "x010", "name": "Амортизатор передний", "category": "Подвеска", "price": 3500, "article": "X-010-SF", "in_stock": True},
            {"id": "x011", "name": "Амортизатор задний", "category": "Подвеска", "price": 3000, "article": "X-011-SR", "in_stock": True},
            {"id": "x012", "name": "Опора амортизатора передняя", "category": "Подвеска", "price": 1200, "article": "X-012-ST", "in_stock": True},
            {"id": "x013", "name": "Рычаг передний левый", "category": "Подвеска", "price": 2800, "article": "X-013-AL", "in_stock": True},
            {"id": "x014", "name": "ШРУС наружный", "category": "Привод", "price": 2200, "article": "X-014-CV", "in_stock": True},
            {"id": "x015", "name": "Фара передняя левая (LED)", "category": "Оптика", "price": 12000, "article": "X-015-HL", "in_stock": False},
            {"id": "x016", "name": "Фара передняя правая (LED)", "category": "Оптика", "price": 12000, "article": "X-016-HR", "in_stock": False},
            {"id": "x017", "name": "Бампер передний", "category": "Кузов", "price": 8500, "article": "X-017-FB", "in_stock": True},
            {"id": "x018", "name": "Радиатор кондиционера", "category": "Охлаждение", "price": 9500, "article": "X-018-AC", "in_stock": True},
        ]
    },
    "largus": {
        "name": "LADA Largus",
        "years": "2012 — настоящее время",
        "image": "https://static.tildacdn.com/tild3338-3832-4732-b235-626331316634/lada_lar_universal.png",
        "description": "Универсал и фургон повышенной вместимости. Идеален для семьи и бизнеса.",
        "parts": [
            {"id": "l001", "name": "Масляный фильтр", "category": "Фильтры", "price": 320, "article": "L-001-OF", "in_stock": True},
            {"id": "l002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 380, "article": "L-002-AF", "in_stock": True},
            {"id": "l003", "name": "Топливный фильтр", "category": "Фильтры", "price": 520, "article": "L-003-FF", "in_stock": True},
            {"id": "l004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 1100, "article": "L-004-BP", "in_stock": True},
            {"id": "l005", "name": "Комплект тормозных колодок задних", "category": "Тормозная система", "price": 900, "article": "L-005-BPR", "in_stock": True},
            {"id": "l006", "name": "Тормозной диск передний", "category": "Тормозная система", "price": 1900, "article": "L-006-BD", "in_stock": True},
            {"id": "l007", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 780, "article": "L-007-SP", "in_stock": True},
            {"id": "l008", "name": "Ремень ГРМ", "category": "Двигатель", "price": 2200, "article": "L-008-TB", "in_stock": True},
            {"id": "l009", "name": "Помпа водяная", "category": "Охлаждение", "price": 2100, "article": "L-009-WP", "in_stock": True},
            {"id": "l010", "name": "Амортизатор передний", "category": "Подвеска", "price": 2800, "article": "L-010-SF", "in_stock": True},
            {"id": "l011", "name": "Амортизатор задний", "category": "Подвеска", "price": 2500, "article": "L-011-SR", "in_stock": True},
            {"id": "l012", "name": "Сайлентблок задней балки", "category": "Подвеска", "price": 450, "article": "L-012-SB", "in_stock": True},
            {"id": "l013", "name": "Шаровая опора", "category": "Подвеска", "price": 580, "article": "L-013-BJ", "in_stock": True},
            {"id": "l014", "name": "ШРУС наружный", "category": "Привод", "price": 2000, "article": "L-014-CV", "in_stock": True},
            {"id": "l015", "name": "Фара передняя левая", "category": "Оптика", "price": 3800, "article": "L-015-HL", "in_stock": True},
            {"id": "l016", "name": "Фара передняя правая", "category": "Оптика", "price": 3800, "article": "L-016-HR", "in_stock": True},
            {"id": "l017", "name": "Бампер передний", "category": "Кузов", "price": 5500, "article": "L-017-FB", "in_stock": True},
            {"id": "l018", "name": "Капот", "category": "Кузов", "price": 9500, "article": "L-018-HD", "in_stock": True},
        ]
    },
    "priora": {
        "name": "LADA Priora",
        "years": "2007 — 2018",
        "image": "https://red-auto.ru/uploads/new_car/265/images/large_priora_3.jpg",
        "description": "Седан, хэтчбек и универсал. Популярная модель с хорошей ремонтопригодностью.",
        "parts": [
            {"id": "p001", "name": "Масляный фильтр", "category": "Фильтры", "price": 220, "article": "P-001-OF", "in_stock": True},
            {"id": "p002", "name": "Воздушный фильтр", "category": "Фильтры", "price": 280, "article": "P-002-AF", "in_stock": True},
            {"id": "p003", "name": "Салонный фильтр", "category": "Фильтры", "price": 250, "article": "P-003-CF", "in_stock": True},
            {"id": "p004", "name": "Комплект тормозных колодок передних", "category": "Тормозная система", "price": 800, "article": "P-004-BP", "in_stock": True},
            {"id": "p005", "name": "Комплект тормозных колодок задних", "category": "Тормозная система", "price": 650, "article": "P-005-BPR", "in_stock": True},
            {"id": "p006", "name": "Тормозной диск передний", "category": "Тормозная система", "price": 1300, "article": "P-006-BD", "in_stock": True},
            {"id": "p007", "name": "Свеча зажигания (комплект 4 шт)", "category": "Двигатель", "price": 500, "article": "P-007-SP", "in_stock": True},
            {"id": "p008", "name": "Ремень ГРМ", "category": "Двигатель", "price": 1800, "article": "P-008-TB", "in_stock": True},
            {"id": "p009", "name": "Ролик натяжной ГРМ", "category": "Двигатель", "price": 1200, "article": "P-009-TR", "in_stock": True},
            {"id": "p010", "name": "Амортизатор передний", "category": "Подвеска", "price": 1800, "article": "P-010-SF", "in_stock": True},
            {"id": "p011", "name": "Амортизатор задний", "category": "Подвеска", "price": 1500, "article": "P-011-SR", "in_stock": True},
            {"id": "p012", "name": "Шаровая опора", "category": "Подвеска", "price": 350, "article": "P-012-BJ", "in_stock": True},
            {"id": "p013", "name": "Рычаг передний левый", "category": "Подвеска", "price": 1800, "article": "P-013-AL", "in_stock": True},
            {"id": "p014", "name": "Ступица передняя", "category": "Подвеска", "price": 2200, "article": "P-014-HB", "in_stock": True},
            {"id": "p015", "name": "ШРУС наружный", "category": "Привод", "price": 1500, "article": "P-015-CV", "in_stock": True},
            {"id": "p016", "name": "Фара передняя левая", "category": "Оптика", "price": 2800, "article": "P-016-HL", "in_stock": True},
            {"id": "p017", "name": "Фара передняя правая", "category": "Оптика", "price": 2800, "article": "P-017-HR", "in_stock": False},
            {"id": "p018", "name": "Бампер передний", "category": "Кузов", "price": 3500, "article": "P-018-FB", "in_stock": True},
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', models=lada_data)

@app.route('/model/<model_id>')
def model_page(model_id):
    if model_id not in lada_data:
        return "Модель не найдена", 404
    model = lada_data[model_id]
    categories = sorted(list(set(part['category'] for part in model['parts'])))
    return render_template('model.html', model_id=model_id, model=model, categories=categories)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    for model_id, model in lada_data.items():
        for part in model['parts']:
            if (query in part['name'].lower() or
                query in part['article'].lower() or
                query in part['category'].lower()):
                part_copy = part.copy()
                part_copy['model_name'] = model['name']
                part_copy['model_id'] = model_id
                results.append(part_copy)
    return jsonify(results)

@app.route('/api/model/<model_id>/parts')
def get_parts(model_id):
    if model_id not in lada_data:
        return jsonify([])
    return jsonify(lada_data[model_id]['parts'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

