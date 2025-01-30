import os


# Создание папки города
def create_city_folder(city_slug: str) -> str:
    city_folder = f"./app/templates/cities/{city_slug}"
    os.makedirs(city_folder, exist_ok=True)
    return city_folder


# Создание папки салона или мастера ('moscow', 'masters', 'ivan')
def create_salon_folder(city_slug: str, entity_type: str, entity_slug: str) -> str:
    if entity_type not in ["salons", "masters"]:
        raise ValueError("Тип должен быть 'salons' или 'masters'")

    # Создаём папку города
    city_folder = create_city_folder(city_slug)

    # Создаём папку типа (salons или masters)
    type_folder = f"{city_folder}/{entity_type}"
    os.makedirs(type_folder, exist_ok=True)

    # Создаём папку для конкретного мастера или салона
    entity_folder = f"{type_folder}/{entity_slug}"
    os.makedirs(entity_folder, exist_ok=True)

    return entity_folder
