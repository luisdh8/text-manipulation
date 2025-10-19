# Limpieza_de_libros.py
import re #modulo de expresiones regulares ()
import string#
import os
from pathlib import Path #para las rutass de los archivos
from nltk.corpus import stopwords #este modulo contiene listas de palabras comunes (stopwords) en varios idiomas
import nltk #para el procesamiento de lenguaje natural, o sea trabajar con textos
# Tienes que descargar el conjunto de stopwords de NLTK si aún no está instalado

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')


def limpiar_y_normalizar(texto: str) -> str:
    """
    Realiza la limpieza básica del texto: elimina puntuación, caracteres especiales,
    dígitos y normaliza a minúsculas.
    
    Args:
        texto (str): Texto original a limpiar
        
    Returns:
        str: Texto limpio y normalizado
    """

    #paso 1: Convertir todo el texto a minúsculas
    # Word = word
    texto_min = texto.lower()

    # PASO 2: Eliminar signos de puntuación
    # Usamos string.punctuation que contiene: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    # translate() reemplaza cada carácter de puntuación por nada, los elimina vaya
    texto_sin_puntuacion = texto_min.translate(
        str.maketrans('', '', string.punctuation)
    )

    # PASO 3: Eliminar números y dígitos
    # La expresión regular \d+ encuentra secuencias de uno o más dígitos
    # y los reemplaza con un espacio
    texto_sin_digitos = re.sub(r'\d+', ' ', texto_sin_puntuacion)

    # PASO 4: Normalizar espacios en blanco
    # \s+ encuentra uno o más espacios, saltos de línea, tabulaciones, etc.
    # Los reemplaza con un solo espacio y elimina espacios al inicio/final
    texto_limpio = re.sub(r'\s+', ' ', texto_sin_digitos).strip()

    return texto_limpio


def tokenizar(texto_limpio: str) -> list:
    """
    Divide el texto limpio en palabras individuales (tokens).
    
    Args:
        texto_limpio (str): Texto ya limpio y normalizado
        
    Returns:
        list: Lista de palabras (tokens)
    """
    
    # PASO 5: Separar el texto en palabras individuales
    # split() divide el texto usando espacios como delimitador
    tokens = texto_limpio.split()
    
    return tokens


def eliminar_stopwords(tokens: list, idioma: str = 'english') -> list:
    """
    Elimina palabras muy comunes (stopwords) que no aportan significado relevante.
    
    Args:
        tokens (list): Lista de palabras
        idioma (str): Idioma de las stopwords ('english', 'spanish', etc.)
        
    Returns:
        list: Lista de tokens sin stopwords
    """
    

    # Stopwords: "the", "is", "at", "which", "on", etc.
    try:
        stop_words = set(stopwords.words(idioma))
    except:
        print(f"Advertencia: No se pudieron cargar stopwords para '{idioma}'")
        return tokens
    
    # PASO 6: Filtrar tokens que NO están en la lista de stopwords
    # Esto nos deja solo con palabras más significativas
    tokens_filtrados = [word for word in tokens if word not in stop_words]
    
    return tokens_filtrados


def obtener_vocabulario_unico(tokens: list) -> list:
    """
    Genera una lista de todas las palabras únicas presentes en el texto,
    ordenadas alfabéticamente.
    
    Args:
        tokens (list): Lista de tokens (puede contener duplicados)
        
    Returns:
        list: Lista de palabras únicas ordenadas
    """
    
    # PASO 7: Crear conjunto (set) para eliminar duplicados
    # Un set automáticamente elimina elementos repetidos
    vocabulario_unico = set(tokens)
    
    # PASO 8: Convertir a lista ordenada alfabéticamente
    # Esto facilita búsquedas y autocompletado posteriores
    vocabulario_ordenado = sorted(list(vocabulario_unico))
    
    return vocabulario_ordenado


def preprocesar_texto(texto: str, eliminar_stops: bool = True) -> dict:
    """
    Encapsula todo el proceso de preprocesamiento de texto.
    
    Args:
        texto (str): Texto original
        eliminar_stops (bool): Si True, elimina stopwords
        
    Returns:
        dict: Diccionario con todos los resultados del preprocesamiento
    """
    
    # Ejecutar pipeline completo de limpieza
    texto_limpio = limpiar_y_normalizar(texto)
    tokens = tokenizar(texto_limpio)
    
    #Eliminar stopwords
    if eliminar_stops:
        tokens = eliminar_stopwords(tokens)
    
    # Generar vocabulario único
    vocabulario = obtener_vocabulario_unico(tokens)
    
    # Retornar todos los resultados
    return {
        'texto_limpio': texto_limpio,
        'tokens': tokens,
        'vocabulario_unico': vocabulario,
        'num_palabras_totales': len(tokens),
        'num_palabras_unicas': len(vocabulario)
    }


def procesar_archivo(ruta_entrada: str, carpeta_salida: str, eliminar_stops: bool = True):
    """
    Procesa un archivo de texto completo y genera archivos de salida con los resultados.
    
    Args:
        ruta_entrada (str): Ruta del archivo a procesar
        carpeta_salida (str): Carpeta donde guardar los resultados
        eliminar_stops (bool): Si True, elimina stopwords
    """
    
    print(f"\n{'='*60}")
    print(f"Procesando: {os.path.basename(ruta_entrada)}")
    print(f"{'='*60}")
    
    # Leer el archivo original
    with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
        texto_original = archivo.read()
    
    print(f"✓ Archivo leído: {len(texto_original)} caracteres")
    
    # Preprocesar el texto
    resultado = preprocesar_texto(texto_original, eliminar_stops)
    
    # Crear nombres de archivos de salida
    nombre_base = Path(ruta_entrada).stem
    ruta_texto_limpio = os.path.join(carpeta_salida, f"{nombre_base}_limpio.txt")
    ruta_tokens = os.path.join(carpeta_salida, f"{nombre_base}_tokens.txt")
    ruta_vocabulario = os.path.join(carpeta_salida, f"{nombre_base}_vocabulario.txt")
    ruta_estadisticas = os.path.join(carpeta_salida, f"{nombre_base}_estadisticas.txt")
    
    # Guardar texto limpio
    with open(ruta_texto_limpio, 'w', encoding='utf-8') as archivo:
        archivo.write(resultado['texto_limpio'])
    print(f"✓ Texto limpio guardado en: {nombre_base}_limpio.txt")
    
    # Guardar tokens (una palabra por línea)
    with open(ruta_tokens, 'w', encoding='utf-8') as archivo:
        archivo.write('\n'.join(resultado['tokens']))
    print(f"✓ Tokens guardados en: {nombre_base}_tokens.txt")
    
    # Guardar vocabulario único
    with open(ruta_vocabulario, 'w', encoding='utf-8') as archivo:
        archivo.write('\n'.join(resultado['vocabulario_unico']))
    print(f"✓ Vocabulario único guardado en: {nombre_base}_vocabulario.txt")
    
    # Guardar estadísticas
    with open(ruta_estadisticas, 'w', encoding='utf-8') as archivo:
        archivo.write(f"Estadísticas de: {os.path.basename(ruta_entrada)}\n")
        archivo.write(f"{'='*50}\n\n")
        archivo.write(f"Total de palabras (tokens): {resultado['num_palabras_totales']}\n")
        archivo.write(f"Palabras únicas (vocabulario): {resultado['num_palabras_unicas']}\n")
        archivo.write(f"Stopwords eliminadas: {'Sí' if eliminar_stops else 'No'}\n")
        archivo.write(f"\nPrimeras 20 palabras del vocabulario:\n")
        archivo.write('\n'.join(resultado['vocabulario_unico'][:20]))
    print(f"✓ Estadísticas guardadas en: {nombre_base}_estadisticas.txt")
    
    # Mostrar resumen en consola
    print(f"\nResumen:")
    print(f"   - Total de palabras: {resultado['num_palabras_totales']}")
    print(f"   - Palabras únicas: {resultado['num_palabras_unicas']}")
    print(f"   - Stopwords eliminadas: {'Sí' if eliminar_stops else 'No'}")


def procesar_carpeta(carpeta_entrada: str, carpeta_salida: str, eliminar_stops: bool = True):
    """
    Procesa todos los archivos .txt de una carpeta.
    
    Args:
        carpeta_entrada (str): Carpeta con archivos de texto a procesar
        carpeta_salida (str): Carpeta donde guardar los resultados
        eliminar_stops (bool): Si True, elimina stopwords
    """
    
    # Crear carpeta de salida si no existe
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Buscar todos los archivos .txt en la carpeta
    archivos_txt = list(Path(carpeta_entrada).glob('*.txt'))
    
    if not archivos_txt:
        print(f"No se encontraron archivos .txt en: {carpeta_entrada}")
        return
    
    print(f"\nIniciando procesamiento de {len(archivos_txt)} archivo(s)...")
    
    # Procesar cada archivo
    for archivo in archivos_txt:
        procesar_archivo(str(archivo), carpeta_salida, eliminar_stops)
    
    print(f"\n{'='*60}")
    print(f"Procesamiento completado!")
    print(f"   Archivos procesados: {len(archivos_txt)}")
    print(f"   Resultados guardados en: {carpeta_salida}")
    print(f"{'='*60}\n")


# --- Ejecución Principal ---
if __name__ == "__main__":
    # Configuración de rutas
    CARPETA_BOOKS = os.path.join('..', 'books')  # Carpeta con los textos originales
    CARPETA_SALIDA = os.path.join('..', 'books', 'procesados')  # Carpeta para resultados
    
    # Procesar todos los archivos de la carpeta books
    procesar_carpeta(CARPETA_BOOKS, CARPETA_SALIDA, eliminar_stops=True)

