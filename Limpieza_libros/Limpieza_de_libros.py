import re
import string
from nltk.corpus import stopwords
# Descargar el conjunto de stopwords de NLTK si aún no está
# (Solo es necesario la primera vez):
import nltk
nltk.download('stopwords')

def limpiar_y_normalizar(texto: str) -> str:
    
    #Realiza la limpieza básica (puntuación, caracteres especiales, dígitos)
    #y la normalización a minúsculas.
    
    # 1. Normalización a Minúsculas
    texto_min = texto.lower()

    # 2. Eliminación de Puntuación
    # Define una expresión regular que incluya todos los signos de puntuación
    # y los reemplace con un espacio ' '.
    texto_sin_puntuacion = texto_min.translate(
        str.maketrans('', '', string.punctuation)
    )

    # 3. Eliminación de Dígitos (Opcional)
    # Reemplaza cualquier dígito (0-9) con un espacio.
    texto_sin_digitos = re.sub(r'\d+', ' ', texto_sin_puntuacion)

    # 4. Eliminación de Saltos de Línea y Tabulaciones
    # Reemplaza secuencias de espacios, saltos de línea y tabulaciones por un solo espacio.
    texto_limpio = re.sub(r'\s+', ' ', texto_sin_digitos).strip()

    return texto_limpio

def eliminar_stopwords_y_tokenizar(texto_limpio: str) -> list:

    #Divide el texto limpio en tokens (palabras) y elimina las stopwords en inglés.

    # 1Conjunto de Stopwords
    # Se carga la lista predefinida de palabras muy comunes en inglés.
    english_stopwords = set(stopwords.words('english'))

    # 2Tokenización
    # Divide el texto en una lista de palabras usando los espacios como delimitador.
    tokens = texto_limpio.split()

    # 3Filtrado de Stopwords
    # Crea una nueva lista de tokens, excluyendo aquellos que están en la lista de stopwords.
    tokens_filtrados = [word for word in tokens if word not in english_stopwords]

    return tokens_filtrados

# --- Función Principal de Procesamiento ---
def preprocesar_texto(texto: str) -> list:
    #Encapsula todo el proceso de preprocesamiento.
    # Limpieza
    texto_intermedio = limpiar_y_normalizar(texto)

    # Reducción de Redundancia y Tokenización
    tokens_finales = eliminar_stopwords_y_tokenizar(texto_intermedio)

    return tokens_finales

