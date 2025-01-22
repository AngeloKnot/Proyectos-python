import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# URL de la página web a hacer scraping
url = 'https://www.bbc.com/news'

# Realizamos la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Parseamos el contenido HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encontramos los títulos de las noticias (en este caso, usando una clase específica)
titulos = soup.find_all('h3', class_='gs-c-promo-heading__title')

# Creamos el elemento raíz del XML
root = ET.Element("Noticias")

# Recorremos los títulos y los añadimos como elementos del XML
for titulo in titulos:
    noticia = ET.SubElement(root, "Noticia")
    noticia.text = titulo.get_text()

# Creamos el árbol XML
tree = ET.ElementTree(root)

# Guardamos el árbol en un archivo XML
tree.write("titulos_noticias.xml", encoding="utf-8", xml_declaration=True)

print("Archivo XML creado correctamente.")
