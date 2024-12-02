import os

# Создание папки города
def create_city_folder(city_slag: str):
    city_folder = f"./app/templates/cities/{city_slag}"
    if not os.path.exists(city_folder):
        os.makedirs(city_folder)
    return city_folder

# Создание папки салона или мастера
def create_salon_folder(city_slag: str, type: str, entity_slug: str):
    type_folder = f"/{type}"
    if not os.path.exists(type_folder):
        os.makedirs(type_folder)


    # Папка для конкретного мастера или салона
    entity_folder = f"{type_folder}/{entity_slug}"
    if not os.path.exists(entity_folder):
        os.makedirs(entity_folder)

    return entity_folder