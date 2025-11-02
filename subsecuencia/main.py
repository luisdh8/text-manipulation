import time
import os
try:
    from subsecuencia.lcs import lcs
    from subsecuencia.similitud import calcSimilitud, reporteSimilitud
    from subsecuencia.fragmento_lcs import obtenerFragmentoLcs, obtenerFragmentoContexto
except ModuleNotFoundError:
    from lcs import lcs
    from similitud import calcSimilitud, reporteSimilitud
    from fragmento_lcs import obtenerFragmentoLcs, obtenerFragmentoContexto


def leerArchivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error leyendo archivo {ruta}: {e}")
        return ""


def dividirBloques(texto, tamaño_bloque=5000):
    if len(texto) <= tamaño_bloque:
        return [texto]
    
    bloques = []
    inicio = 0
    
    while inicio < len(texto):
        fin = inicio + tamaño_bloque
        
        # Intentar cortar en un espacio o salto de línea
        if fin < len(texto):
            # Buscar el último espacio en los últimos 200 caracteres
            espacio = texto.rfind(' ', fin - 200, fin)
            if espacio != -1:
                fin = espacio
        
        bloques.append(texto[inicio:fin])
        inicio = fin
    
    return bloques


def compararBloques(texto1, texto2, tamaño_bloque=5000):
    bloques1 = dividirBloques(texto1, tamaño_bloque)
    bloques2 = dividirBloques(texto2, tamaño_bloque)
    
    # Limitar comparaciones si hay demasiados bloques
    max_comparaciones = 100
    total_comparaciones = len(bloques1) * len(bloques2)
    
    if total_comparaciones > max_comparaciones:
        # Muestreo estratégico: comparar menos bloques
        step1 = max(1, len(bloques1) // 10)
        step2 = max(1, len(bloques2) // 10)
        bloques1 = bloques1[::step1]
        bloques2 = bloques2[::step2]
        print(f"\nDemasiados bloques, usando muestreo estratégico")
    
    print(f"\nEstrategia de comparación:")
    print(f"   - Texto 1: {len(bloques1)} bloque(s) a comparar")
    print(f"   - Texto 2: {len(bloques2)} bloque(s) a comparar")
    print(f"   - Comparaciones a realizar: {len(bloques1) * len(bloques2)}")
    
    mejor_lcs = 0
    mejor_similitud = 0
    mejor_fragmento = ""
    mejor_par = (0, 0)
    total_comparaciones_realizadas = len(bloques1) * len(bloques2)
    
    tiempo_inicio = time.time()
    
    # Comparar cada par de bloques
    for i, bloque1 in enumerate(bloques1):
        for j, bloque2 in enumerate(bloques2):
            actual = i * len(bloques2) + j + 1
            print(f"   Comparando: {actual}/{total_comparaciones_realizadas} ({actual*100//total_comparaciones_realizadas}%)...", end='\r')
            
            longitud_lcs, fragmento_lcs = lcs(bloque1, bloque2)
            
            if longitud_lcs > mejor_lcs:
                mejor_lcs = longitud_lcs
                mejor_similitud = calcSimilitud(bloque1, bloque2)
                mejor_par = (i, j)
                # Solo extraer fragmento del mejor par (ya lo tenemos de lcs)
                if len(fragmento_lcs) > 500:
                    mejor_fragmento = fragmento_lcs[:500] + "... [fragmento truncado]"
                else:
                    mejor_fragmento = fragmento_lcs
    
    tiempo_total = time.time() - tiempo_inicio
    print()  # Nueva línea después del progreso
    
    return {
        'longitud_lcs': mejor_lcs,
        'similitud': mejor_similitud,
        'fragmento': mejor_fragmento,
        'tiempo_ejecucion': tiempo_total,
        'mejor_par_bloques': mejor_par,
        'total_bloques': (len(bloques1), len(bloques2)),
        'tamaño_bloque': tamaño_bloque
    }


def compararTextosCompletos(texto1, texto2, max_tamaño=10000):
    if len(texto1) > max_tamaño or len(texto2) > max_tamaño:
        return None
    
    print(f"\nComparación directa (textos pequeños)")
    
    tiempo_inicio = time.time()
    
    longitud_lcs, fragmento = lcs(texto1, texto2)
    similitud = calcSimilitud(texto1, texto2)
    
    # Limitar fragmento si es muy largo
    if len(fragmento) > 500:
        fragmento = fragmento[:500] + "... [fragmento truncado]"
    
    tiempo_total = time.time() - tiempo_inicio
    
    return {
        'longitud_lcs': longitud_lcs,
        'similitud': similitud,
        'fragmento': fragmento,
        'tiempo_ejecucion': tiempo_total
    }


def mostrarResultados(resultados, nombre1, nombre2):
    print("\n" + "="*70)
    print(f"RESULTADOS DE LA COMPARACIÓN")
    print("="*70)
    print(f"Archivos comparados: {nombre1} vs {nombre2}")
    print(f"\nLongitud de LCS: {resultados['longitud_lcs']} caracteres")
    print(f"Similitud: {resultados['similitud']:.2f}%")
    print(f"Tiempo de ejecución: {resultados['tiempo_ejecucion']:.4f} segundos")
    
    if 'mejor_par_bloques' in resultados:
        print(f"\nInformación de bloques:")
        print(f"   - Total bloques texto 1: {resultados['total_bloques'][0]}")
        print(f"   - Total bloques texto 2: {resultados['total_bloques'][1]}")
        print(f"   - Mejor coincidencia: bloque {resultados['mejor_par_bloques'][0]+1} x bloque {resultados['mejor_par_bloques'][1]+1}")
        print(f"   - Tamaño de bloque usado: {resultados['tamaño_bloque']} caracteres")
    
    print(f"\nFragmento encontrado (primeros 500 caracteres):")
    print("-" * 70)
    if resultados['fragmento']:
        print(resultados['fragmento'][:500])
    else:
        print("(No se encontró subsecuencia común)")
    print("-" * 70)


def main():
    """Función principal del programa."""
    print("="*70)
    print("ANÁLISIS DE SIMILITUD DE TEXTOS USANDO LCS")
    print("="*70)
    
    # Determinar la ruta base (directorio padre si estamos en subsecuencia/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == 'subsecuencia':
        base_dir = os.path.dirname(script_dir)
    else:
        base_dir = script_dir
    
    # Configuración de archivos a comparar
    archivo1 = os.path.join(base_dir, "books/procesados", "manifesto_limpio.txt")
    archivo2 = os.path.join(base_dir, "books/procesados", "capital-v1_limpio.txt")
    
    print(f"\nLeyendo archivos...")
    texto1 = leerArchivo(archivo1)
    texto2 = leerArchivo(archivo2)
    
    if not texto1 or not texto2:
        print("Error: No se pudieron leer los archivos.")
        return
    
    print(f"Archivos leídos exitosamente")
    print(f"   - {archivo1}: {len(texto1):,} caracteres")
    print(f"   - {archivo2}: {len(texto2):,} caracteres")
    
    # Decidir estrategia de comparación
    tamaño_maximo_directo = 10000
    
    if len(texto1) <= tamaño_maximo_directo and len(texto2) <= tamaño_maximo_directo:
        # Comparación directa para textos pequeños
        resultados = compararTextosCompletos(texto1, texto2)
    else:
        # Comparación por bloques para textos grandes
        print(f"\nTextos muy grandes para comparación directa")
        print(f"   Se usará estrategia de división en bloques")
        resultados = compararBloques(texto1, texto2, tamaño_bloque=5000)
    
    # Mostrar resultados
    mostrarResultados(resultados, archivo1, archivo2)
    
    print("\n" + "="*70)
    print("Análisis completado")
    print("="*70)


if __name__ == "__main__":
    main()


