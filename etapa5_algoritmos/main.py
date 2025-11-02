"""
Etapa 5 - Investigación de alternativas algorítmicas
Main script para ejecutar y comparar todos los algoritmos

Este script ejecuta y compara:
1. Hirschberg (LCS optimizado en espacio)
2. Distancia de Levenshtein
3. Similitud de Jaccard con n-gramas
"""

import time
import os
import sys

# Imports de los algoritmos de etapa 5
try:
    from etapa5_algoritmos.hirschberg import hirschberg_con_bloques, calcular_similitud_hirschberg
    from etapa5_algoritmos.levenshtein import levenshtein_con_bloques, similitud_levenshtein
    from etapa5_algoritmos.jaccard_ngram import (
        jaccard_con_bloques, 
        analisis_multingrama,
        ngramas_comunes_frecuentes
    )
except ModuleNotFoundError:
    from hirschberg import hirschberg_con_bloques, calcular_similitud_hirschberg
    from levenshtein import levenshtein_con_bloques, similitud_levenshtein
    from jaccard_ngram import (
        jaccard_con_bloques, 
        analisis_multingrama,
        ngramas_comunes_frecuentes
    )


def leer_archivo(ruta):
    """Lee un archivo de texto."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error leyendo archivo {ruta}: {e}")
        return ""


def ejecutar_hirschberg(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo de Hirschberg."""
    print("\n" + "="*70)
    print("ALGORITMO 1: HIRSCHBERG (LCS optimizado en espacio)")
    print("="*70)
    print("\nJustificación:")
    print("El algoritmo de Hirschberg es una versión optimizada del LCS que")
    print("reduce la complejidad de espacio de O(n*m) a O(min(n,m)) usando")
    print("divide y vencerás. Esto permite procesar textos más grandes sin")
    print("quedarse sin memoria, manteniendo la misma precisión que el LCS.")
    print("\nVentaja esperada: Menor uso de memoria en textos grandes.")
    
    tiempo_inicio = time.time()
    
    # Para textos grandes, usar versión con bloques (usar bloques más pequeños para velocidad)
    resultados = hirschberg_con_bloques(texto1, texto2, tamaño_bloque=5000)
    
    tiempo_total = time.time() - tiempo_inicio
    
    # Calcular similitud
    if resultados['metodo'] == 'directo':
        similitud = (2 * resultados['longitud_lcs']) / (len(texto1) + len(texto2)) * 100
    else:
        # Para bloques, estimar similitud basada en el mejor resultado
        similitud = (2 * resultados['longitud_lcs']) / (10000 + 10000) * 100
    
    print(f"\n{'Resultados':-^70}")
    print(f"Longitud del LCS: {resultados['longitud_lcs']:,} caracteres")
    print(f"Porcentaje de similitud: {similitud:.2f}%")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {resultados['metodo']}")
    
    if resultados['metodo'] == 'bloques':
        print(f"Total de bloques comparados: {resultados['total_bloques']}")
        print(f"Mejor coincidencia: bloque {resultados['mejor_par']}")
    
    print(f"\nFragmento encontrado (primeros 300 caracteres):")
    print("-" * 70)
    print(resultados['fragmento'][:300] if resultados['fragmento'] else "(No hay fragmento)")
    print("-" * 70)
    
    return {
        'algoritmo': 'Hirschberg',
        'similitud': similitud,
        'tiempo': tiempo_total,
        'longitud_lcs': resultados['longitud_lcs'],
        'metodo': resultados['metodo']
    }


def ejecutar_levenshtein(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo de Levenshtein."""
    print("\n" + "="*70)
    print("ALGORITMO 2: DISTANCIA DE LEVENSHTEIN")
    print("="*70)
    print("\nJustificación:")
    print("La distancia de Levenshtein mide cuántas operaciones (insertar,")
    print("eliminar, sustituir) se necesitan para transformar un texto en otro.")
    print("A diferencia del LCS, penaliza las diferencias y considera sustituciones,")
    print("lo que lo hace ideal para detectar textos casi idénticos con errores.")
    print("\nVentaja esperada: Mejor detección de variaciones y errores tipográficos.")
    
    tiempo_inicio = time.time()
    
    # Usar bloques pequeños y limitar comparaciones para velocidad
    resultados = levenshtein_con_bloques(texto1, texto2, tamaño_bloque=5000)
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n{'Resultados':-^70}")
    
    if resultados['metodo'] == 'directo':
        print(f"Distancia de edición: {resultados['distancia']:,}")
        print(f"Porcentaje de similitud: {resultados['similitud']:.2f}%")
    else:
        print(f"Distancia promedio entre bloques: {resultados['distancia_promedio']:,.2f}")
        print(f"Similitud promedio: {resultados['similitud_promedio']:.2f}%")
        print(f"Mejor similitud encontrada: {resultados['mejor_similitud']:.2f}%")
        print(f"Mejor distancia encontrada: {resultados['mejor_distancia']:,}")
        print(f"Total de bloques comparados: {resultados['total_bloques']}")
        print(f"Mejor coincidencia: bloque {resultados['mejor_par']}")
    
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {resultados['metodo']}")
    
    similitud_final = resultados.get('similitud', resultados.get('mejor_similitud', 0))
    
    return {
        'algoritmo': 'Levenshtein',
        'similitud': similitud_final,
        'tiempo': tiempo_total,
        'distancia': resultados.get('distancia', resultados.get('mejor_distancia', 0)),
        'metodo': resultados['metodo']
    }


def ejecutar_jaccard(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo de Jaccard con n-gramas."""
    print("\n" + "="*70)
    print("ALGORITMO 3: SIMILITUD DE JACCARD CON N-GRAMAS")
    print("="*70)
    print("\nJustificación:")
    print("Jaccard con n-gramas divide los textos en fragmentos de n caracteres")
    print("consecutivos y mide cuántos se comparten. No requiere que los fragmentos")
    print("estén en el mismo orden, lo que lo hace robusto ante reordenamientos.")
    print("Es muy eficiente (O(n+m)) y usado en detección de plagio.")
    print("\nVentaja esperada: Alta eficiencia y robustez ante reordenamientos.")
    
    # Análisis con múltiples tamaños de n-gramas
    print(f"\n{'Análisis con diferentes tamaños de n-gramas':-^70}")
    
    # Para el análisis completo, usar muestras pequeñas
    muestra1 = texto1[:10000] if len(texto1) > 10000 else texto1
    muestra2 = texto2[:10000] if len(texto2) > 10000 else texto2
    
    resultados_multi = analisis_multingrama(muestra1, muestra2, tamaños=[2, 3, 4, 5])
    
    print("\nResultados por tamaño de n-grama (muestra de 10,000 caracteres):")
    print(f"{'n':>3} | {'Similitud':>10} | {'Ponderada':>10} | {'N-gramas T1':>12} | {'N-gramas T2':>12} | {'Comunes':>8}")
    print("-" * 70)
    
    for n, datos in sorted(resultados_multi.items()):
        print(f"{n:3d} | {datos['similitud_simple']:9.2f}% | {datos['similitud_ponderada']:9.2f}% | "
              f"{datos['ngramas_texto1']:12,} | {datos['ngramas_texto2']:12,} | {datos['ngramas_comunes']:8,}")
    
    # Análisis completo con trigramas (n=3)
    print(f"\n{'Análisis completo con trigramas (n=3)':-^70}")
    
    tiempo_inicio = time.time()
    
    # Jaccard es más eficiente, puede usar bloques más grandes
    resultados = jaccard_con_bloques(texto1, texto2, n=3, tamaño_bloque=5000)
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\nResultados:")
    
    if resultados['metodo'] == 'directo':
        print(f"Similitud de Jaccard: {resultados['similitud']:.2f}%")
        print(f"Similitud ponderada: {resultados['similitud_ponderada']:.2f}%")
    else:
        print(f"Similitud promedio: {resultados['similitud_promedio']:.2f}%")
        print(f"Similitud ponderada promedio: {resultados['similitud_ponderada_promedio']:.2f}%")
        print(f"Mejor similitud encontrada: {resultados['similitud']:.2f}%")
        print(f"Mejor similitud ponderada: {resultados['similitud_ponderada']:.2f}%")
        print(f"Total de bloques comparados: {resultados['total_bloques']}")
        print(f"Mejor coincidencia: bloque {resultados['mejor_par']}")
    
    print(f"Tamaño de n-grama usado: {resultados['tamaño_ngrama']}")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {resultados['metodo']}")
    
    # Mostrar n-gramas comunes más frecuentes
    print(f"\n{'Top 10 n-gramas comunes más frecuentes':-^70}")
    comunes = ngramas_comunes_frecuentes(muestra1, muestra2, n=3, top_k=10)
    
    if comunes:
        print(f"{'N-grama':>10} | {'Freq T1':>10} | {'Freq T2':>10} | {'Total':>10}")
        print("-" * 70)
        for ngrama, freq1, freq2 in comunes:
            print(f"{repr(ngrama):>10} | {freq1:10,} | {freq2:10,} | {freq1+freq2:10,}")
    else:
        print("(No se encontraron n-gramas comunes)")
    
    return {
        'algoritmo': 'Jaccard (n-grama)',
        'similitud': resultados['similitud'],
        'tiempo': tiempo_total,
        'similitud_ponderada': resultados.get('similitud_ponderada', 0),
        'metodo': resultados['metodo'],
        'resultados_multi': resultados_multi
    }


def comparar_resultados(resultados_lista):
    """Compara los resultados de todos los algoritmos."""
    print("\n" + "="*70)
    print("COMPARACIÓN DE RESULTADOS DE TODOS LOS ALGORITMOS")
    print("="*70)
    
    print(f"\n{'Algoritmo':^25} | {'Similitud':^12} | {'Tiempo (s)':^12}")
    print("-" * 70)
    
    for res in resultados_lista:
        print(f"{res['algoritmo']:^25} | {res['similitud']:^12.2f}% | {res['tiempo']:^12.4f}")
    
    # Encontrar el mejor en cada categoría
    mejor_similitud = max(resultados_lista, key=lambda x: x['similitud'])
    mas_rapido = min(resultados_lista, key=lambda x: x['tiempo'])
    
    print("\n" + "="*70)
    print("ANÁLISIS COMPARATIVO")
    print("="*70)
    
    print(f"\n🏆 Mayor similitud detectada:")
    print(f"   {mejor_similitud['algoritmo']}: {mejor_similitud['similitud']:.2f}%")
    
    print(f"\n⚡ Algoritmo más rápido:")
    print(f"   {mas_rapido['algoritmo']}: {mas_rapido['tiempo']:.4f} segundos")
    
    print("\n📊 Interpretación de resultados:")
    
    # Análisis de similitudes
    similitudes = [r['similitud'] for r in resultados_lista]
    promedio = sum(similitudes) / len(similitudes)
    
    print(f"\n   Similitud promedio entre todos los métodos: {promedio:.2f}%")
    
    if promedio > 70:
        print("   ➜ Los textos son MUY SIMILARES según todos los algoritmos")
    elif promedio > 40:
        print("   ➜ Los textos tienen SIMILITUD MODERADA")
    elif promedio > 20:
        print("   ➜ Los textos tienen BAJA SIMILITUD")
    else:
        print("   ➜ Los textos son MUY DIFERENTES")
    
    # Análisis de tiempos
    print(f"\n⏱️  Análisis de eficiencia:")
    tiempos = [r['tiempo'] for r in resultados_lista]
    tiempo_total = sum(tiempos)
    
    for res in resultados_lista:
        porcentaje = (res['tiempo'] / tiempo_total) * 100
        print(f"   {res['algoritmo']:25} : {res['tiempo']:7.4f}s ({porcentaje:5.1f}%)")


def mostrar_conclusiones():
    """Muestra las conclusiones del análisis."""
    print("\n" + "="*70)
    print("CONCLUSIONES")
    print("="*70)


def main():
    """Función principal del programa."""
    print("="*70)
    print("ETAPA 5 - INVESTIGACIÓN DE ALTERNATIVAS ALGORÍTMICAS")
    print("="*70)
    print("\nImplementación y comparación de tres nuevos algoritmos:")
    print("1. Hirschberg (LCS optimizado en espacio)")
    print("2. Distancia de Levenshtein")
    print("3. Similitud de Jaccard con n-gramas")
    
    # Determinar la ruta base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == 'etapa5_algoritmos':
        base_dir = os.path.dirname(script_dir)
    else:
        base_dir = script_dir
    
    # Configuración de archivos a comparar
    archivo1 = os.path.join(base_dir, "books/procesados", "manifesto_limpio.txt")
    archivo2 = os.path.join(base_dir, "books/procesados", "capital-v1_limpio.txt")
    
    print(f"\n📁 Leyendo archivos...")
    texto1 = leer_archivo(archivo1)
    texto2 = leer_archivo(archivo2)
    
    if not texto1 or not texto2:
        print("❌ Error: No se pudieron leer los archivos.")
        return
    
    print(f"✓ Archivos leídos exitosamente")
    print(f"   - {os.path.basename(archivo1)}: {len(texto1):,} caracteres")
    print(f"   - {os.path.basename(archivo2)}: {len(texto2):,} caracteres")
    
    # Lista para almacenar todos los resultados
    todos_los_resultados = []
    
    # Ejecutar cada algoritmo
    resultado1 = ejecutar_hirschberg(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado1)
    
    resultado2 = ejecutar_levenshtein(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado2)
    
    resultado3 = ejecutar_jaccard(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado3)
    
    # Comparar resultados
    comparar_resultados(todos_los_resultados)
    
    # Mostrar conclusiones
    mostrar_conclusiones()
    
    print("\n" + "="*70)
    print("✓ Análisis completado exitosamente")
    print("="*70)


if __name__ == "__main__":
    main()
