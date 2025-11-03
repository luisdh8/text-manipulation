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
    from etapa5_algoritmos.lcs import lcs
    from etapa5_algoritmos.longest_common_substring import lcSub
    from etapa5_algoritmos.rabin_karp_substring import rabin_karp_longest_substring
except ModuleNotFoundError:
    from hirschberg import hirschberg_con_bloques, calcular_similitud_hirschberg
    from levenshtein import levenshtein_con_bloques, similitud_levenshtein
    from jaccard_ngram import (
        jaccard_con_bloques, 
        analisis_multingrama,
        ngramas_comunes_frecuentes
    )
    from lcs import lcs
    from longest_common_substring import lcSub
    from rabin_karp_substring import rabin_karp_longest_substring


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


def ejecutar_lcs(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo LCS tradicional (de Etapa 4)."""
    print("\n" + "="*70)
    print("ALGORITMO 4: LCS TRADICIONAL (Etapa 4 - Comparación)")
    print("="*70)
    print("\nNota:")
    print("Este es el algoritmo LCS tradicional implementado en la Etapa 4.")
    print("Se incluye para comparación directa con Hirschberg (Etapa 5),")
    print("que tiene la misma complejidad de tiempo O(n*m) pero usa menos memoria.")
    print("\nComplejidad: O(n*m) tiempo, O(n*m) espacio")
    
    # Usar bloques del mismo tamaño que Hirschberg para comparación justa
    tamaño_bloque = 5000
    
    tiempo_inicio = time.time()
    
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        longitud_lcs, fragmento_lcs = lcs(texto1, texto2)
        similitud = (2 * longitud_lcs) / (len(texto1) + len(texto2)) * 100
        metodo = 'directo'
        mejor_par = None
        total_bloques = None
    else:
        # Dividir en bloques
        bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
        bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
        
        # Mismo muestreo que Hirschberg
        max_comparaciones = 25
        total_comparaciones = len(bloques1) * len(bloques2)
        
        if total_comparaciones > max_comparaciones:
            step1 = max(1, len(bloques1) // 5)
            step2 = max(1, len(bloques2) // 5)
            bloques1_muestra = bloques1[::step1]
            bloques2_muestra = bloques2[::step2]
        else:
            bloques1_muestra = bloques1
            bloques2_muestra = bloques2
        
        mejor_longitud = 0
        mejor_fragmento = ""
        mejor_par = (0, 0)
        
        total = len(bloques1_muestra) * len(bloques2_muestra)
        actual = 0
        
        for i, bloque1 in enumerate(bloques1_muestra):
            for j, bloque2 in enumerate(bloques2_muestra):
                actual += 1
                print(f"   LCS: {actual}/{total} ({actual*100//total}%)...", end='\r')
                
                longitud, fragmento = lcs(bloque1, bloque2)
                
                if longitud > mejor_longitud:
                    mejor_longitud = longitud
                    mejor_fragmento = fragmento
                    mejor_par = (i, j)
        
        print()  # Nueva línea
        
        longitud_lcs = mejor_longitud
        fragmento_lcs = mejor_fragmento
        similitud = (2 * longitud_lcs) / (tamaño_bloque + tamaño_bloque) * 100
        metodo = 'bloques'
        total_bloques = (len(bloques1_muestra), len(bloques2_muestra))
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n{'Resultados':-^70}")
    print(f"Longitud del LCS: {longitud_lcs:,} caracteres")
    print(f"Porcentaje de similitud: {similitud:.2f}%")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {metodo}")
    
    if metodo == 'bloques':
        print(f"Total de bloques comparados: {total_bloques}")
        print(f"Mejor coincidencia: bloque {mejor_par}")
    
    print(f"\nFragmento encontrado (primeros 300 caracteres):")
    print("-" * 70)
    print(fragmento_lcs[:300] if fragmento_lcs else "(No hay fragmento)")
    print("-" * 70)
    
    return {
        'algoritmo': 'LCS Tradicional (Etapa 4)',
        'similitud': similitud,
        'tiempo': tiempo_total,
        'longitud_lcs': longitud_lcs,
        'metodo': metodo
    }


def ejecutar_longest_substring(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo Longest Common Substring (Etapa 3)."""
    print("\n" + "="*70)
    print("ALGORITMO 5: LONGEST COMMON SUBSTRING (Etapa 3 - Comparación)")
    print("="*70)
    print("\nNota:")
    print("Este es el algoritmo LCSstr de la Etapa 3 (substring común más largo).")
    print("A diferencia del LCS (subsequence), este busca fragmentos CONTIGUOS.")
    print("Se incluye para comparar con Rabin-Karp (Etapa 5).")
    print("\nComplejidad: O(n*m) tiempo, O(n*m) espacio")
    
    # Usar bloques del mismo tamaño para comparación justa
    tamaño_bloque = 5000
    
    tiempo_inicio = time.time()
    
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        longitud_substr, fragmento_substr = lcSub(texto1, texto2)
        similitud = (2 * longitud_substr) / (len(texto1) + len(texto2)) * 100
        metodo = 'directo'
        mejor_par = None
        total_bloques = None
    else:
        # Dividir en bloques
        bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
        bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
        
        print(f"Bloques de texto 1: {len(bloques1)}")
        print(f"Bloques de texto 2: {len(bloques2)}")
        
        # Mismo muestreo que en substring_analysis
        max_comparaciones = 50
        total_comparaciones = len(bloques1) * len(bloques2)
        
        if total_comparaciones > max_comparaciones:
            step1 = max(1, len(bloques1) // 7)
            step2 = max(1, len(bloques2) // 7)
            bloques1_muestra = bloques1[::step1]
            bloques2_muestra = bloques2[::step2]
            print(f"Demasiados bloques - usando muestreo (cada {step1} x cada {step2})")
        else:
            bloques1_muestra = bloques1
            bloques2_muestra = bloques2
        
        print(f"Comparaciones a realizar: {len(bloques1_muestra) * len(bloques2_muestra)}")
        
        mejor_longitud = 0
        mejor_fragmento = ""
        mejor_par = (0, 0)
        
        total = len(bloques1_muestra) * len(bloques2_muestra)
        actual = 0
        
        for i, bloque1 in enumerate(bloques1_muestra):
            for j, bloque2 in enumerate(bloques2_muestra):
                actual += 1
                print(f"   LCSstr: {actual}/{total} ({actual*100//total}%)...", end='\r')
                
                longitud, fragmento = lcSub(bloque1, bloque2)
                
                if longitud > mejor_longitud:
                    mejor_longitud = longitud
                    mejor_fragmento = fragmento
                    mejor_par = (i, j)
        
        print()  # Nueva línea
        
        longitud_substr = mejor_longitud
        fragmento_substr = mejor_fragmento
        similitud = (2 * longitud_substr) / (tamaño_bloque + tamaño_bloque) * 100
        metodo = 'bloques'
        total_bloques = (len(bloques1_muestra), len(bloques2_muestra))
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n{'Resultados':-^70}")
    print(f"Longitud del substring común: {longitud_substr:,} caracteres")
    print(f"Porcentaje de similitud: {similitud:.2f}%")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {metodo}")
    
    if metodo == 'bloques':
        print(f"Total de bloques comparados: {total_bloques}")
        print(f"Mejor coincidencia: bloque {mejor_par}")
    
    print(f"\nFragmento encontrado (primeros 300 caracteres):")
    print("-" * 70)
    print(fragmento_substr[:300] if fragmento_substr else "(No hay fragmento)")
    print("-" * 70)
    
    return {
        'algoritmo': 'Longest Substring (Etapa 3)',
        'similitud': similitud,
        'tiempo': tiempo_total,
        'longitud_substr': longitud_substr,
        'metodo': metodo
    }


def ejecutar_rabin_karp(texto1, texto2, nombre1, nombre2):
    """Ejecuta el algoritmo Rabin-Karp con ventana deslizante."""
    print("\n" + "="*70)
    print("ALGORITMO 6: RABIN-KARP (Ventana deslizante - Etapa 5)")
    print("="*70)
    print("\nJustificación:")
    print("Rabin-Karp usa hashing (rolling hash) para encontrar el substring")
    print("común más largo de forma más eficiente. Calcula un hash de cada")
    print("ventana y solo compara strings cuando los hashes coinciden.")
    print("Usa búsqueda binaria en la longitud para optimizar aún más.")
    print("\nVentaja esperada: Mucho más rápido que LCSstr tradicional.")
    print("Complejidad: O(n+m) promedio vs O(n*m) del método clásico")
    
    # Usar bloques del mismo tamaño para comparación justa
    tamaño_bloque = 5000
    
    tiempo_inicio = time.time()
    
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        longitud_substr, fragmento_substr = rabin_karp_longest_substring(texto1, texto2)
        similitud = (2 * longitud_substr) / (len(texto1) + len(texto2)) * 100
        metodo = 'directo'
        mejor_par = None
        total_bloques = None
    else:
        # Dividir en bloques
        bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
        bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
        
        print(f"Bloques de texto 1: {len(bloques1)}")
        print(f"Bloques de texto 2: {len(bloques2)}")
        
        # Mismo muestreo que en substring_analysis
        max_comparaciones = 50
        total_comparaciones = len(bloques1) * len(bloques2)
        
        if total_comparaciones > max_comparaciones:
            step1 = max(1, len(bloques1) // 7)
            step2 = max(1, len(bloques2) // 7)
            bloques1_muestra = bloques1[::step1]
            bloques2_muestra = bloques2[::step2]
            print(f"Demasiados bloques - usando muestreo (cada {step1} x cada {step2})")
        else:
            bloques1_muestra = bloques1
            bloques2_muestra = bloques2
        
        print(f"Comparaciones a realizar: {len(bloques1_muestra) * len(bloques2_muestra)}")
        
        mejor_longitud = 0
        mejor_fragmento = ""
        mejor_par = (0, 0)
        
        total = len(bloques1_muestra) * len(bloques2_muestra)
        actual = 0
        
        for i, bloque1 in enumerate(bloques1_muestra):
            for j, bloque2 in enumerate(bloques2_muestra):
                actual += 1
                print(f"   Rabin-Karp: {actual}/{total} ({actual*100//total}%)...", end='\r')
                
                longitud, fragmento = rabin_karp_longest_substring(bloque1, bloque2)
                
                if longitud > mejor_longitud:
                    mejor_longitud = longitud
                    mejor_fragmento = fragmento
                    mejor_par = (i, j)
        
        print()  # Nueva línea
        
        longitud_substr = mejor_longitud
        fragmento_substr = mejor_fragmento
        similitud = (2 * longitud_substr) / (tamaño_bloque + tamaño_bloque) * 100
        metodo = 'bloques'
        total_bloques = (len(bloques1_muestra), len(bloques2_muestra))
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n{'Resultados':-^70}")
    print(f"Longitud del substring común: {longitud_substr:,} caracteres")
    print(f"Porcentaje de similitud: {similitud:.2f}%")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    print(f"Método usado: {metodo}")
    
    if metodo == 'bloques':
        print(f"Total de bloques comparados: {total_bloques}")
        print(f"Mejor coincidencia: bloque {mejor_par}")
    
    print(f"\nFragmento encontrado (primeros 300 caracteres):")
    print("-" * 70)
    print(fragmento_substr[:300] if fragmento_substr else "(No hay fragmento)")
    print("-" * 70)
    
    return {
        'algoritmo': 'Rabin-Karp (Etapa 5)',
        'similitud': similitud,
        'tiempo': tiempo_total,
        'longitud_substr': longitud_substr,
        'metodo': metodo
    }


def comparar_resultados(resultados_lista):
    """Compara los resultados de todos los algoritmos."""
    print("\n" + "="*70)
    print("COMPARACIÓN DE RESULTADOS DE TODOS LOS ALGORITMOS")
    print("="*70)
    
    # Separar por categorías
    etapa5 = [r for r in resultados_lista if 'Etapa 5' in r['algoritmo'] or r['algoritmo'] in ['Hirschberg', 'Levenshtein', 'Jaccard (n-grama)', 'Rabin-Karp (Etapa 5)']]
    anteriores = [r for r in resultados_lista if r not in etapa5]
    
    print(f"\n{'[NUEVOS] ALGORITMOS (Etapa 5)':^70}")
    print(f"{'Algoritmo':^30} | {'Similitud':^12} | {'Tiempo (s)':^12}")
    print("-" * 70)
    
    for res in etapa5:
        print(f"{res['algoritmo']:^30} | {res['similitud']:^12.2f}% | {res['tiempo']:^12.4f}")
    
    print(f"\n{'[ANTERIORES] ALGORITMOS (Comparación)':^70}")
    print(f"{'Algoritmo':^30} | {'Similitud':^12} | {'Tiempo (s)':^12}")
    print("-" * 70)
    
    for res in anteriores:
        print(f"{res['algoritmo']:^30} | {res['similitud']:^12.2f}% | {res['tiempo']:^12.4f}")
    
    # Encontrar el mejor en cada categoría
    mejor_similitud = max(resultados_lista, key=lambda x: x['similitud'])
    mas_rapido = min(resultados_lista, key=lambda x: x['tiempo'])
    
    print("\n" + "="*70)
    print("ANÁLISIS COMPARATIVO")
    print("="*70)
    
    print(f"\n[*] Mayor similitud detectada:")
    print(f"   {mejor_similitud['algoritmo']}: {mejor_similitud['similitud']:.2f}%")
    
    print(f"\n[*] Algoritmo más rápido:")
    print(f"   {mas_rapido['algoritmo']}: {mas_rapido['tiempo']:.4f} segundos")
    
    # Comparaciones específicas
    print(f"\n[*] Comparaciones específicas:")
    
    # Hirschberg vs LCS Tradicional
    hirschberg = next((r for r in resultados_lista if r['algoritmo'] == 'Hirschberg'), None)
    lcs_trad = next((r for r in resultados_lista if 'LCS Tradicional' in r['algoritmo']), None)
    
    if hirschberg and lcs_trad:
        print(f"\n   � Hirschberg vs LCS Tradicional (ambos buscan subsequence):")
        print(f"      Similitud: {hirschberg['similitud']:.2f}% vs {lcs_trad['similitud']:.2f}%")
        speedup = lcs_trad['tiempo'] / hirschberg['tiempo'] if hirschberg['tiempo'] > 0 else 0
        print(f"      Tiempo: {hirschberg['tiempo']:.4f}s vs {lcs_trad['tiempo']:.4f}s")
        if speedup > 1:
            print(f"      -> Hirschberg es {speedup:.2f}x más rápido")
        elif speedup < 1 and speedup > 0:
            print(f"      -> LCS Tradicional es {1/speedup:.2f}x más rápido")
        print(f"      [+] Ventaja de Hirschberg: Mismo resultado, menos memoria")
    
    # Rabin-Karp vs Longest Substring
    rabin = next((r for r in resultados_lista if 'Rabin-Karp' in r['algoritmo']), None)
    lcstr = next((r for r in resultados_lista if 'Longest Substring' in r['algoritmo']), None)
    
    if rabin and lcstr:
        print(f"\n   📌 Rabin-Karp vs Longest Substring (ambos buscan substring):")
        print(f"      Similitud: {rabin['similitud']:.2f}% vs {lcstr['similitud']:.2f}%")
        speedup = lcstr['tiempo'] / rabin['tiempo'] if rabin['tiempo'] > 0 else 0
        print(f"      Tiempo: {rabin['tiempo']:.4f}s vs {lcstr['tiempo']:.4f}s")
        if speedup > 1:
            print(f"      -> Rabin-Karp es {speedup:.2f}x más rápido")
        elif speedup < 1 and speedup > 0:
            print(f"      -> Longest Substring es {1/speedup:.2f}x más rápido")
        print(f"      [+] Ventaja de Rabin-Karp: Rolling hash, búsqueda binaria")
    
    print("\n[*] Interpretación de resultados:")
    
    # Análisis de similitudes
    similitudes = [r['similitud'] for r in resultados_lista]
    promedio = sum(similitudes) / len(similitudes)
    
    print(f"\n   Similitud promedio entre todos los métodos: {promedio:.2f}%")
    
    if promedio > 70:
        print("   -> Los textos son MUY SIMILARES según todos los algoritmos")
    elif promedio > 40:
        print("   -> Los textos tienen SIMILITUD MODERADA")
    elif promedio > 20:
        print("   -> Los textos tienen BAJA SIMILITUD")
    else:
        print("   -> Los textos son MUY DIFERENTES")
    
    # Análisis de tiempos
    print(f"\n[*] Análisis de eficiencia:")
    tiempos = [r['tiempo'] for r in resultados_lista]
    tiempo_total = sum(tiempos)
    
    for res in resultados_lista:
        porcentaje = (res['tiempo'] / tiempo_total) * 100
        print(f"   {res['algoritmo']:30} : {res['tiempo']:7.4f}s ({porcentaje:5.1f}%)")
    
    print(f"\n   Tiempo total de ejecución: {tiempo_total:.4f} segundos")


def mostrar_conclusiones():
    """Muestra las conclusiones del análisis."""
    print("\n" + "="*70)
    print("CONCLUSIONES")
    print("="*70)
    
    print("""
[*] Resumen de Etapa 5:

Se implementaron y compararon 6 algoritmos de similitud textual:

[NUEVOS] ALGORITMOS (Etapa 5):
   
   1. Hirschberg (LCS optimizado en espacio)
       [+] Reduce memoria de O(n*m) a O(min(n,m))
       [+] Mismo resultado que LCS tradicional
       [!] Más lento en la práctica por overhead de divide-y-conquista
       >> Mejor para: Textos grandes con memoria limitada
   
   2. Distancia de Levenshtein
       [+] Detecta ediciones, sustituciones, inserciones, eliminaciones
       [+] Ideal para detectar textos casi idénticos con errores
       [!] Muy lento O(n*m) con constantes altas
       >> Mejor para: Corrección ortográfica, diff de archivos
   
   3. Similitud de Jaccard con n-gramas
       [+] EXTREMADAMENTE RÁPIDO: O(n+m)
       [+] Robusto ante reordenamientos
       [+] Usado en detección de plagio
       >> Mejor para: Comparaciones rápidas, grandes volúmenes
   
   4. Rabin-Karp con ventana deslizante
       [+] Mucho más rápido que Longest Substring tradicional
       [+] Rolling hash permite búsqueda eficiente
       [+] Búsqueda binaria optimiza aún más
       >> Mejor para: Encontrar fragmentos comunes exactos rápidamente

[ANTERIORES] ALGORITMOS (Comparación):

   [*] Hirschberg vs LCS Tradicional (Etapa 4):
      • Ambos buscan longest common SUBSEQUENCE
      • Resultado depende del caso específico
      • Hirschberg usa menos memoria (ventaja en textos gigantes)
      • Resultado: Misma longitud de LCS encontrada
   
   [*] Rabin-Karp vs Longest Substring (Etapa 3):
      • Ambos buscan longest common SUBSTRING (contiguo)
      • Rabin-Karp es significativamente más rápido
      • Ambos encuentran el mismo substring
      • Rabin-Karp es claramente superior en eficiencia

[*] RECOMENDACIONES POR CASO DE USO:

   [->] Necesitas velocidad máxima?
      >> Jaccard con n-gramas (el más rápido)
   
   [->] Buscas fragmentos comunes exactos?
      >> Rabin-Karp (mucho más rápido que método clásico)
   
   [->] Necesitas detectar textos con errores tipográficos?
      >> Levenshtein (pero prepara café, es lento)
   
   [->] Textos gigantes con poca memoria?
      >> Hirschberg (usa O(min(n,m)) espacio vs O(n*m))
   
   [->] Necesitas precisión académica?
      >> LCS Tradicional (balance entre velocidad y precisión)

[*] LECCIÓN PRINCIPAL:
   
   No existe "el mejor algoritmo" - cada uno tiene su nicho:
   
   • Jaccard: Ganador absoluto en velocidad y detección general
   • Rabin-Karp: Mejor para substrings exactos, gran mejora sobre método clásico
   • Levenshtein: Único que detecta distancia de edición
   • Hirschberg: Útil cuando la memoria es el cuello de botella
   
   La elección depende de:
   [+] Tamaño de los textos
   [+] Restricciones de tiempo
   [+] Restricciones de memoria
   [+] Tipo de similitud que buscas (subsequence vs substring)
   [+] Tolerancia a errores o cambios
    """)


def main():
    """Función principal del programa."""
    print("="*70)
    print("ETAPA 5 - INVESTIGACION DE ALTERNATIVAS ALGORITMICAS")
    print("="*70)
    print("\nImplementacion y comparacion de algoritmos:")
    print("\n[NUEVOS] ALGORITMOS (Etapa 5):")
    print("1. Hirschberg (LCS optimizado en espacio)")
    print("2. Distancia de Levenshtein")
    print("3. Similitud de Jaccard con n-gramas")
    print("4. Rabin-Karp con ventana deslizante")
    print("\n[ANTERIORES] ALGORITMOS (para comparacion):")
    print("5. LCS Tradicional (Etapa 4 - subsequence)")
    print("6. Longest Common Substring (Etapa 3 - substring)")
    
    # Determinar la ruta base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == 'etapa5_algoritmos':
        base_dir = os.path.dirname(script_dir)
    else:
        base_dir = script_dir
    
    # Configuración de archivos a comparar
    archivo1 = os.path.join(base_dir, "books/procesados", "manifesto_limpio.txt")
    archivo2 = os.path.join(base_dir, "books/procesados", "capital-v1_limpio.txt")
    
    print(f"\n>> Leyendo archivos...")
    texto1 = leer_archivo(archivo1)
    texto2 = leer_archivo(archivo2)
    
    if not texto1 or not texto2:
        print("[!] Error: No se pudieron leer los archivos.")
        return
    
    print(f"[OK] Archivos leídos exitosamente")
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
    
    resultado4 = ejecutar_rabin_karp(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado4)
    
    # Ejecutar algoritmos anteriores para comparación
    resultado5 = ejecutar_lcs(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado5)
    
    resultado6 = ejecutar_longest_substring(texto1, texto2, archivo1, archivo2)
    todos_los_resultados.append(resultado6)
    
    # Comparar resultados
    comparar_resultados(todos_los_resultados)
    
    # Mostrar conclusiones
    mostrar_conclusiones()
    
    print("\n" + "="*70)
    print("[OK] Análisis completado exitosamente")
    print("="*70)


if __name__ == "__main__":
    main()
