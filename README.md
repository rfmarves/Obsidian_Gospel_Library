# Escrituras en markdown para usar en Obisidian

Inspirado por otros repositorios en Github (sólo en inglés), empecé a hacer el mío en español y aquí estoy compartiendo el programa en Python y los archivos que usé para hacerlo, junto con los archivos en markdown resultantes en 3 idiomas.

## Cómo instalar en Obsidian:

1.  Descarga las carpetas que quieras agregar a tu repositorio
2.  Agrégalas a tu biblioteca en Obsidian

## Cómo crear un nuevo idioma o darle tu propio formato:

1.  Usa el archivo de Excel incluido para crear la nueva lista de metadata. Primero, elige tu configuración. La primera hoja tiene varios parámetros para personalizar:
    1.  El prefijo de idioma (language prefix) es el código de 3 letras utilizado en el sitio de la iglesia para identificar el idioma (todas las páginas terminan con `?lang=` seguido por ese código de 3 letras)
    2.  El folder raíz (Library Root folder) es la carpeta donde está la biblioteca de Obisidian. Todos los archivos serán puestos ahí.
    3.  El nombre de la colección (collection name) cambia el nombre de la carpeta donde se podrán todos los archivos de las escrituras.
    4.  Use el parámetro de prefijo (prefix) para evitar problemas de nombres en Obsidian al agregar ese prefijo a todos los archivos en la biblioteca (yo lo usé para agregar el prefijo “sw” a todos los archivos en inglés para evitar conflictos con mi juego de archivos en español).
    5.  La tabla de abajo tiene la traducción de los nombres de los libros. Para agregar un idioma nuevo, sólo tiene que agregar una columna nueva a la tabla. Las contribución aquí son bienvenidas.
2.  Ya que esté lista su configuración, de la siguiente hoja, copie desde la celda R2 hasta la R1591 a un nuevo archivo de texto. Tengo 3 archivos de texto que generé y usé en el repositorio. Estará generando sus propios archivos ahí.
3.  Ahora, edite el archivo download.py. Ahí tiene que configurar lo siguiente:
    1.  En la sección de configuración (`Configuration Parameters`) de parámetros, cambie la variable del nombre de archivos (`filename`) de `list-es.txt` a lo que sea que puso de nombre su archivo en el paso anterior. (Asegúrese que el programita de Python esté en la misma carpeta que su archivo txt).
    2.  Cambie `SummaryText` para que diga lo que desee que esté de título para los resúmenes de los capítulos
    3.  Cambie `OnlineText` para que diga lo que desee que salga en los enlaces hacia la página web de donde salió cada página de markdown.
    4.  Si desea personalizar el encabezado de metadata, busque el comentario `#Construct YAML heading for each md file`. El encabezado de metadata está construido en las líneas que le siguen.
4.  Ya que terminó de personalizar, corra download.py. Requiere que tenga instalado Python, con los módulos os, requests, y BeautifulSoup instalados. Utilicé Python 3.10, con las últimas versiones de todo al 24 de abril, 2022.

# Markdown Scriptures/Standard Works for use in Obsidian

Inspired by other repositories found in GitHub (only in English) I started to get mine in Spanish and here I’m sharing the Python script and file used to make this, along with the markdown files result in 3 languages.

## How to install in Obsidian:

1.  Download the folders you want added to your repository
2.  Add them to your Obsidian Library

## How to create a new language or reformat for your own version:

1.  Use the excel file included to create a new metadata list. First, pick your configuration. The first sheet has several parameters to customize:
    1.  The language prefix is the 3-letter language code used in the church site to identify the language (all pages end with `?lang=` followed by this 3 letter code)
    2.  The Library Root is the root folder for your Obsidian Library. All files will be place in there.
    3.  The Collection name changes the name of the folder where all the files will be loaded
    4.  Use the prefix parameter to avoid naming conflicts in obsidian and adding that prefix to all files in the library (I used it to add a ‘sw’ prefix to the English set to avoid conflict with my Spanish set).
    5.  The table on the bottom has the book translations. To add a new language, just add a new column to the table. Contributions are welcome here.
2.  Once your configuration is ready, copy from cell R2 to cell R1591 into a new text file. I have the 3 text files I generated in the repository. You’d be generating your own here.
3.  Now edit the `download.py` file. Here, you need to configure the following:
    1.  In the Configuration Parameters section, change the `filename` variable from `list-es.txt` to whatever you named your file from the previous step. (Make sure the script is in the same folder as your txt file)
    2.  Change `SummaryText` to read to whaver you want to name your chapter summaries.
    3.  Change `OnlineText` to read to whatever you want to have displayed as the text to the online version of each markdown file.
    4.  If you want to customize the metadata header, look for the `#Construct YAML heading for each md file` comment. The metadata header is constructed in the lines after that.
4.  Once you’re done customizing, run the `download.py` script. It requires that you have Python installed, with the `os`, `requests`, and `BeautifulSoup` modules installed. I used Python 3.10, with the latest version of everything as of April 24, 2022.
