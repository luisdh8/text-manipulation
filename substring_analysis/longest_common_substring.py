"""
Implementación del algoritmo Longest Common Substring (LCS)
Basado exactamente en el pseudocódigo de la actividad anterior
"""

import time
from pathlib import Path


def leer_archivo(nombre_archivo):
    """Lee un archivo de texto desde books/procesados"""
    # Ruta absoluta desde la carpeta de trabajo actual
    ruta_base = Path(__file__).parent.parent  # Subir dos niveles desde substring_analysis
    ruta_archivo = ruta_base / 'books' / 'procesados' / nombre_archivo
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            print(f"Archivo leído: {nombre_archivo} ({len(contenido):,} caracteres)")
            return contenido
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        return None


def lcSub(S_1, S_2):
    """
    Implementacióndel pseudocódigo:
    
    lcSub(S_1, S_2):
        Entrada: Dos strings S_1 y S_2 de tamaños n y m
        Salida: El tamaño del substring común más largo entre S_1 y S_2
        
        Sea lc una matriz de n x m
        Sea maxlcsub = 0 el valor de la longitud del substring común más largo encontrado.
        
        Repetir para i = 0 hasta n - 1:
            Repetir para j = 0 hasta m - 1:
                Si S_1[i] != S_2[j]:
                    lc[i][j] = 0
                De lo contrario:
                    Si i == 0 o j == 0:
                        lc[i][j] = 1
                    De lo contrario:
                        lc[i][j] = lc[i - 1][j - 1] + 1
                    
                    Si lc[i][j] > maxlcsub:
                        maxlcsub = lc[i][j]
        Regresa maxlcsub
    """
    
    # Entrada: Dos strings S_1 y S_2 de tamaños n y m
    n, m = len(S_1), len(S_2)
    
    if n == 0 or m == 0:
        return 0, ""
    
    # Sea lc una matriz de n x m
    lc = [[0] * m for _ in range(n)]
    
    # Sea maxlcsub = 0 el valor de la longitud del substring común más largo encontrado
    maxlcsub = 0
    ending_pos_i = 0  # Para extraer el substring después
    
    # Repetir para i = 0 hasta n - 1:
    for i in range(n):
        # Repetir para j = 0 hasta m - 1:
        for j in range(m):
            # Si S_1[i] != S_2[j]:
            if S_1[i] != S_2[j]:
                lc[i][j] = 0
            # De lo contrario:
            else:
                # Si i == 0 o j == 0:
                if i == 0 or j == 0:
                    lc[i][j] = 1
                # De lo contrario:
                else:
                    lc[i][j] = lc[i - 1][j - 1] + 1
                
                # Si lc[i][j] > maxlcsub:
                if lc[i][j] > maxlcsub:
                    maxlcsub = lc[i][j]
                    ending_pos_i = i
    
    # Extraer el substring para mostrarlo
    if maxlcsub == 0:
        substring = ""
    else:
        start_pos = ending_pos_i - maxlcsub + 1
        substring = S_1[start_pos:ending_pos_i + 1]
    
    # Regresa maxlcsub (y el substring para reportarlo)
    return maxlcsub, substring


def analizar_textos(texto1, texto2, nombre1, nombre2):
    """Analiza dos textos con el algoritmo lcSub"""
    
    print(f"\n=== ANÁLISIS DE SUBSTRING COMÚN MÁS LARGO ===")
    print(f"Texto 1: {nombre1} ({len(texto1):,} caracteres)")
    print(f"Texto 2: {nombre2} ({len(texto2):,} caracteres)")
    
    # Para evitar problemas de memoria/tiempo, trabajamos con muestras
    TAMAÑO_MUESTRA = 30000  # 10,000 caracteres por muestra
    
    muestra1 = texto1[:TAMAÑO_MUESTRA]
    muestra2 = texto2[:TAMAÑO_MUESTRA]
    
    print(f"Analizando muestras de {TAMAÑO_MUESTRA:,} caracteres para evitar problemas de memoria")
    print(f"Muestra 1: {len(muestra1):,} caracteres")
    print(f"Muestra 2: {len(muestra2):,} caracteres")
    
    # Medir tiempo de ejecución
    tiempo_inicio = time.time()
    
    # Ejecutar algoritmo (SOLO el del pseudocódigo)
    longitud, substring = lcSub(muestra1, muestra2)
    
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - tiempo_inicio
    
    # Calcular porcentaje de similitud básico (sobre las muestras)
    if len(muestra1) > 0 and len(muestra2) > 0:
        porcentaje_similitud = (2 * longitud) / (len(muestra1) + len(muestra2)) * 100
    else:
        porcentaje_similitud = 0
    
    # Mostrar resultados
    print(f"\nRESULTADOS:")
    print(f"• Longitud del substring común más largo: {longitud:,} caracteres")
    print(f"• Porcentaje de similitud: {porcentaje_similitud:.2f}%")
    print(f"• Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
    
    if longitud > 0:
        # Mostrar fragmento (o parte si es muy largo)
        if len(substring) <= 300:
            print(f"• Fragmento encontrado: \"{substring}\"")
        else:
            print(f"• Fragmento encontrado (primeros/últimos 150 chars): \"{substring[:150]}...{substring[-150:]}\"")
    else:
        print("• No se encontró substring común")
    
    return {
        'longitud': longitud,
        'porcentaje': porcentaje_similitud, 
        'tiempo': tiempo_ejecucion,
        'fragmento': substring
    }


def buscar_archivos_limpios():
    """Busca todos los archivos *_limpio.txt en books/procesados"""
    # Ruta absoluta desde la carpeta de trabajo actual
    ruta_base = Path(__file__).parent.parent  # Subir dos niveles desde substring_analysis
    carpeta_procesados = ruta_base / 'books' / 'procesados'
    
    print(f"Buscando en: {carpeta_procesados.absolute()}")
    
    if not carpeta_procesados.exists():
        print(f"Error: No se encontró la carpeta {carpeta_procesados}")
        return []
    
    # Buscar archivos que terminen en '_limpio.txt'
    archivos_limpios = list(carpeta_procesados.glob('*_limpio.txt'))
    
    # Convertir a nombres de archivo solamente
    nombres_archivos = [archivo.name for archivo in archivos_limpios]
    
    return nombres_archivos


def main():
    """Función principal"""
    
    print("=== ALGORITMO LONGEST COMMON SUBSTRING ===")
    
    # Buscar archivos de texto limpios disponibles
    archivos = buscar_archivos_limpios()
    
    if not archivos:
        print("Error: No se encontraron archivos de texto limpios en books/procesados")
        print("Asegúrate de ejecutar primero el script de limpieza de textos")
        return
    
    print("Archivos de texto limpios encontrados:")
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo}")
    
    # Leer textos
    textos = {}
    for archivo in archivos:
        contenido = leer_archivo(archivo)
        if contenido:
            textos[archivo] = contenido
    
    if len(textos) < 2:
        print("Error: Se necesitan al menos 2 archivos para la comparación")
        return
    
    print(f"\nSe cargaron {len(textos)} archivos correctamente")
    
    # Analizar cada par de textos
    nombres = list(textos.keys())
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            archivo1, archivo2 = nombres[i], nombres[j]
            resultado = analizar_textos(
                textos[archivo1], textos[archivo2], 
                archivo1, archivo2
            )
    
    print("\n=== ANÁLISIS COMPLETADO ===")


if __name__ == "__main__":
    main()