import requests
from bs4 import BeautifulSoup

def get_humble_bundle_games(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    # Encontrar todas las filas de la tabla que contienen los detalles de los juegos
    game_rows = soup.select('table tbody tr')

    for row in game_rows:
        # Obtener el nombre del juego
        name_cell = row.select_one('td:nth-of-type(1)')
        name = name_cell.get_text(strip=True)

        # Obtener el precio del juego
        price_cell = row.select_one('td:nth-of-type(2)')
        price = price_cell.get_text(strip=True).replace('$', '')

        # Encontrar la descripción del juego
        description_cell = row.find_next_sibling('tr').select_one('td')
        description = description_cell.get_text(strip=True)

        # Encontrar la imagen del juego
        image_cell = row.find_next_sibling('tr').select_one('td img')
        image_url = image_cell['src'] if image_cell else None

        game_details = {
            'name': name,
            'price': price,
            'description': description,
            'image_url': image_url
        }

        games.append(game_details)

    return games

# Función para publicar un juego en Mercado Libre
def publish_game_on_mercado_libre(game_details):
    # Aquí debes consumir la API de Mercado Libre
    # para crear una nueva publicación con los detalles del juego

    # Ejemplo de cómo hacer una solicitud a la API de Mercado Libre
    headers = {
        'Content-Type': 'application/json',
        # Agrega tus credenciales de acceso a la API aquí
    }
    data = {
        # Estructura los detalles del juego según los requerimientos de la API
        'title': game_details['name'],
        'price': game_details['price'],
        'description': game_details['description'],
        'image': game_details['image_url'],
        # Agrega más detalles si es necesario
    }
    response = requests.post('https://api.mercadolibre.com/items', headers=headers, json=data)

    if response.status_code == 201:
        print(f'Juego publicado correctamente en Mercado Libre: {game_details["name"]}')
    else:
        print(f'Error al publicar el juego en Mercado Libre: {game_details["name"]}')
        print(response.text)

# Ejemplo de uso
humble_bundle_url = 'https://www.humblebundle.com/games/ejemplo-paquete'
games = get_humble_bundle_games(humble_bundle_url)

for game in games:
    publish_game_on_mercado_libre(game)
