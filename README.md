<a href="http://proyectoaii.pythonanywhere.com/home/">
    <img src="https://github.com/ezegonmac/CubeMarket/blob/main/src/static/images/logo.png" alt="CubeMarket logo" title="CubeMarket" align="right" height="60" />
</a>

# Cube Market

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/home-1.png" alt="Inicio" align="center" width="900" />

## Table of content

- [Cube Market](#cube-market)
  - [Table of content](#table-of-content)
  - [Objetivos](#objetivos)
  - [Tecnologías](#tecnologías)
    - [BeautifoulSoup (Scraping)](#beautifoulsoup-scraping)
    - [Whoosh y SQLite (Bases de datos)](#whoosh-y-sqlite-bases-de-datos)
    - [Sistema de recomendación](#sistema-de-recomendación)
    - [Django (Aplicación Web)](#django-aplicación-web)
    - [Midjourney y ChatGPT](#midjourney-y-chatgpt)
  - [Manual de uso](#manual-de-uso)
    - [Inicio de sesión y registro](#inicio-de-sesión-y-registro)
    - [Administrador](#administrador)
    - [Catálogo](#catálogo)
    - [Recomendaciones](#recomendaciones)
    - [Perfil](#perfil)
  - [Dependencias](#dependencias)
  - [Setup](#setup)
  - [Cargar datos iniciales](#cargar-datos-iniciales)


## Objetivos

Este trabajo tiene la intención de demostrar los conocimientos adquiridos en la asignatura, aplicándolos a un proyecto real. Cube Market es una aplicación web creada para los coleccionistas y amantes del cubo de Rubik. Extrae los datos le los cubos vendidos en la página “speedcubeshop.com”, concretamente de la sección “Puzzles”, y permite a los usuarios realizar búsquedas personalizadas, permitiendo marcar los productos como gustados. A partir de los gustos extraídos del usuario, se recomiendan nuevos productos no marcados anteriormente. Además, contiene otras funcionalidades que permiten una experiencia mejorada tanto a los usuarios como al administrador de la web.

## Tecnologías

### BeautifoulSoup (Scraping)

Para obtener los datos de la página, se realiza un web Scraping a la página https://speedcubeshop.com/collections/all-puzzles dentro de la página “speedcubeshop.com”, donde se realiza la venta de cubos de Rubik de manera online.
Este catálogo contiene más de 500 cubos organizados en casi 50 páginas. De aquí se obtienen los datos principales: nombre, imagen, precio y enlace al producto en dicha página.
Para obtener los detalles del producto, es necesario acceder a cada url de los productos, y obtenerlos de la página de detalle. De aquí se obtiene una imagen de detalle, la marca y un nombre reducido. Además, dependiendo del producto existen diferentes atributos que se pueden personalizar, así como el color de las pegatinas o el color interno. Más abajo, existen dos secciones de donde se obtienen atributos, la descripción, y otros detalles, como: tipo, imanes, peso, tamaño y fecha de publicación. Estos también pueden variar dependiendo del producto.


### Whoosh y SQLite (Bases de datos)

Se han creado dos bases de datos, una de tipo no-SQL (Whoosh) para almacenar los productos, y una SQL (SQLite por simplicidad, aunque en un entorno real debería ser sustituida por otra tecnología como MySQL o PostgresSQL) para almacenar tanto los usuarios como los likes de los usuarios.
La base de datos no-SQL se ha escogido para facilitar la búsqueda de los productos, sobre todo en los campos de tipo texto. Se han creado un esquema principal para el producto, y varios auxiliares para poder referenciar los atributos enumerados desde tablas individuales. Así se reduce el tamaño de la base de datos, almacenando solamente las ids de los atributos, en lugar de los nombres completos.
La base de datos SQL se ha escogido para relacionar los usuarios con las ids de los productos. Así tenemos una tabla con una entrada por cada like de cada usuario que nos permitirá realizar la recomendación más tarde. 

### Sistema de recomendación

Se ha implementado un sistema de recomendación basado en contenido. No se tienen en cuenta por tanto los gustos de otros usuarios, solo la similaridad de los productos que le gustan al usuario con los demás productos.
Se ha implementado desde cero, sin usar ninguna librería. En el archivo “recommendations.py” se define la función “recommend_items(user_id)” permite obtener la lista de todos los productos no marcados aún por el usuario, ordenados por puntuación.
Las puntuaciones se calculan en las otras funciones del fichero. En el caso el caso del nombre se usa el coeficiente de Dice para comparar los conjuntos de palabras. Para los atributos que solo pueden tomar un valor se puntúa con 1 en el caso que coincidan y 0 en caso contrario. Para los atributos que tienen varios valores, como las posibles personalizaciones de cada producto, se usa otro método de puntuación. En este caso se obtiene una mayor punción mientras más atributos de los del producto marcado también contenga.


### Django (Aplicación Web)

Para la creación de la aplicación web se ha usado el framework Django. La aplicación principal “main” contiene los modelos anteriormente mencionados, las vistas creadas, las urls etc. No se usa ningún framework para los estilos.

### Midjourney y ChatGPT

Para hacer más interesante la aplicación y aprovechando el auge de algunas aplicaciones de inteligencia artificial, se ha generado la imagen de la página de inicio usando “Midjourney” una aplicación que permite crear imágenes a partir de un input de texto, y los textos de esta misma página han sido generados por la aplicación “ChatGPT”.

## Manual de uso

### Inicio de sesión y registro

Al entrar a la página clicaremos en la parte superior derecha en “Login” para acceder a la página de inicio de sesión.

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/home.png" alt="Inicio" align="center" width="500" />

En esta página podemos tanto iniciar sesión con alguno de los usuarios ya creados, como clicar en "Signup" para registrarnos.

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/login.png" alt="Inicio de sesión" align="center" width="500" />
<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/signup.png" alt="Registro" align="center" width="500" />

Dependiendo si somos usuarios habituales o administradores, aparecerán distintas opciones en la barra de navegación.

### Administrador

Desde la barra de navegación siendo administradores, podremos desplegar el menú “Admin” donde encontraremos dos secciones: “Scrape” y “Admin Panel”.

  - Scrape: al acceder a esta sección se realiza el proceso de Scraping, en la consola se provee información, como atributos nuevos encontrados que no hayan sido tenido en cuenta previamente, o la página actual. Finalmente se muestra un resumen de los datos almacenados.

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/scrape-console.png" alt="Scraping consola" align="center" width="500" />
<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/scraping.png" alt="Scraping" align="center" width="500" />

  - Admin Panel: se nos reenvía al panel de administrador.

### Catálogo

Desde la barra de navegación siendo usuarios o administradores, podremos acceder a esta sección.
Se nos mostrarán todos los productos almacenados, y se nos permite filtrar de distintas maneras. Por un campo de texto, que buscará en los campos nombre y descripción con un algoritmo fuzzy, que permite manejar mejor los errores cometidos por el usuario al introducir la búsqueda, además no tiene en cuenta las mayúsculas. Y por filtros dependiendo del tipo, la marca y los imanes. Además, se agrupan en páginas de 10 productos por las que podemos navegar desde la parte inferior del catálogo.
Cada producto muestra algunos detalles junto a su foto, marcarlo como gustados o acceder a la página de detalle del producto pinchando en él. 

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/catalog-1.png" alt="Catálogo" align="center" width="500" />
<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/catalog-2.png" alt="Búsqueda en catálogo" align="center" width="500" />

### Recomendaciones

Desde la barra de navegación siendo usuarios o administradores, podremos acceder a la sección "For You".
Aquí se mostrarán 10 artículos nuevos recomendados en base a los que te han gustado anteriormente, para poder guardarlos dándoles "like".

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/foryou.png" alt="Recomendaciones" align="center" width="500" />

### Perfil

Desde la parte derecha de la barra de navegación, pulsando en nuestro usuario, podremos acceder a nuestro perfil.
Allí encontramos un botón para cerrar sesión “Logout” y una sección donde se muestran los artículos marcados como "like".

<img src="https://github.com/ezegonmac/CubeMarket/blob/main/screenshots/profile.png" alt="Perfil" align="center" width="500" />

## Dependencias

- Python - 3.10.7
- Whoosh - 2.7.4
- Beautifoulsoup - 4.11.1
- Django - 4.1.3


## Setup

1. Clonamos el repositorio:

```
git clone https://github.com/ezegonmac/CubeMarket
```

2. Iniciamos el entorno virtual y descargamos las dependencias:

```
pipenv shell
pip install -r requirements.txt
```

3. Cargamos la base de datos SQL:

```
cd /src
python manage.py migrate
```

4. Ejecutamos el proyecto:

```
python manage.py runserver
```

Ya podremos acceder a http://localhost:8000/home/ o http://localhost:8000 para visualizar la web.

## Cargar datos iniciales

Si queremos cargar los datos iniciales relacionados con usuarios y likes, desde el directorio /src:

```
python manage.py loaddata fixtures/initial.json
```




