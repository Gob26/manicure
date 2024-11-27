# scripts/load_cities.py
import json
from tortoise import Tortoise, run_async
from db.models.location.city import City

async def load_cities():
    '''
    Загрузка городов из файла JSON в базу данных
    '''
    await Tortoise.init(
        db_url="postgres://user:password@localhost:5432/dbname",
        modules={"models": ["app.domains.location.models"]}
    )
    await Tortoise.generate_schemas()

    with open("app/static/data/cities.json", "r", encoding="utf-8") as f:
        cities_data = json.load(f)
        
    for city in cities_data:
        coords = city["coords"]
        await City.create(
            name=city["name"],
            district=city["district"],
            subject=city["subject"],
            population=city["population"],
            latitude=float(coords["lat"]),
            longitude=float(coords["lon"])
        )
    print("Города успешно загружены!")
    await Tortoise.close_connections()

run_async(load_cities())
