"""
Script de comparación completa: Etapas 3, 4 y 5
Compara TODOS los métodos implementados en el proyecto
"""

import time
import os
import sys

# Importar algoritmos de etapas anteriores
try:
    # Intentar importar desde subsecuencia_optimizado (Etapa 4)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'subsecuencia_optimizado'))
    from subsecuencia_optimizado.lcs import lcs
    from subsecuencia_optimizado.similitud import calcSimilitud
except:
    try:
        from lcs import lcs
        from similitud import calcSimilitud
    except:
        lcs = None
        calcSimilitud = None

# Importar algoritmos de etapa 5
try:
    from etapa5_algoritmos.hirschberg import hirschberg, calcular_similitud_hirschberg
    from etapa5_algoritmos.levenshtein import levenshtein_distancia_optimizado, similitud_levenshtein
    from etapa5_algoritmos.jaccard_ngram import similitud_jaccard, similitud_jaccard_ponderada
except ModuleNotFoundError:
    from hirschberg import hirschberg, calcular_similitud_hirschberg
    from levenshtein import levenshtein_distancia_optimizado, similitud_levenshtein
    from jaccard_ngram import similitud_jaccard, similitud_jaccard_ponderada


def leer_archivo(ruta):
    """Lee un archivo de texto."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error leyendo archivo {ruta}: {e}")
        return ""


def ejecutar_comparacion_completa(texto1, texto2, max_chars=10000):
    """
    Ejecuta todos los algoritmos en muestras de los textos y compara resultados.
    
    Args:
        texto1: Primer texto completo
        texto2: Segundo texto completo
        max_chars: Número máximo de caracteres a usar para la comparación
    """
    # Tomar muestras para comparación justa
    muestra1 = texto1[:max_chars]
    muestra2 = texto2[:max_chars]
    
    print("\n" + "="*80)
    print("COMPARACIÓN COMPLETA DE TODOS LOS ALGORITMOS")
    print("="*80)
    print(f"\nComparando muestras de {max_chars:,} caracteres de cada texto")
    print(f"Texto 1: {len(texto1):,} caracteres (muestra: {len(muestra1):,})")
    print(f"Texto 2: {len(texto2):,} caracteres (muestra: {len(muestra2):,})")
    
    resultados = []
    
    # ===== ETAPA 4: LCS (Subsecuencia Común Más Larga) =====
    if lcs and calcSimilitud:
        print(f"\n{'Ejecutando LCS (Etapa 4)...':-^80}")
        tiempo_inicio = time.time()
        try:
            longitud_lcs, fragmento_lcs = lcs(muestra1, muestra2)
            similitud_lcs = calcSimilitud(muestra1, muestra2)
            tiempo_lcs = time.time() - tiempo_inicio
            
            resultados.append({
                'etapa': 'Etapa 4',
                'algoritmo': 'LCS (Subsecuencia común)',
                'similitud': similitud_lcs,
                'tiempo': tiempo_lcs,
                'detalles': f'Longitud: {longitud_lcs:,} chars',
                'complejidad_tiempo': 'O(n×m)',
                'complejidad_espacio': 'O(n×m)'
            })
            print(f"✓ Completado en {tiempo_lcs:.4f}s - Similitud: {similitud_lcs:.2f}%")
        except Exception as e:
            print(f"✗ Error en LCS: {e}")
    
    # ===== ETAPA 5.1: HIRSCHBERG =====
    print(f"\n{'Ejecutando Hirschberg (Etapa 5)...':-^80}")
    tiempo_inicio = time.time()
    try:
        longitud_hirsch, fragmento_hirsch = hirschberg(muestra1, muestra2)
        similitud_hirsch = (2 * longitud_hirsch) / (len(muestra1) + len(muestra2)) * 100
        tiempo_hirsch = time.time() - tiempo_inicio
        
        resultados.append({
            'etapa': 'Etapa 5',
            'algoritmo': 'Hirschberg (LCS optimizado)',
            'similitud': similitud_hirsch,
            'tiempo': tiempo_hirsch,
            'detalles': f'Longitud: {longitud_hirsch:,} chars',
            'complejidad_tiempo': 'O(n×m)',
            'complejidad_espacio': 'O(min(n,m))'
        })
        print(f"✓ Completado en {tiempo_hirsch:.4f}s - Similitud: {similitud_hirsch:.2f}%")
    except Exception as e:
        print(f"✗ Error en Hirschberg: {e}")
    
    # ===== ETAPA 5.2: LEVENSHTEIN =====
    print(f"\n{'Ejecutando Levenshtein (Etapa 5)...':-^80}")
    tiempo_inicio = time.time()
    try:
        distancia_lev = levenshtein_distancia_optimizado(muestra1, muestra2)
        similitud_lev = similitud_levenshtein(muestra1, muestra2)
        tiempo_lev = time.time() - tiempo_inicio
        
        resultados.append({
            'etapa': 'Etapa 5',
            'algoritmo': 'Levenshtein (Distancia de edición)',
            'similitud': similitud_lev,
            'tiempo': tiempo_lev,
            'detalles': f'Distancia: {distancia_lev:,} ediciones',
            'complejidad_tiempo': 'O(n×m)',
            'complejidad_espacio': 'O(min(n,m))'
        })
        print(f"✓ Completado en {tiempo_lev:.4f}s - Similitud: {similitud_lev:.2f}%")
    except Exception as e:
        print(f"✗ Error en Levenshtein: {e}")
    
    # ===== ETAPA 5.3: JACCARD N-GRAMAS =====
    for n in [2, 3, 4]:
        print(f"\n{'Ejecutando Jaccard '+str(n)+'-gramas (Etapa 5)...':-^80}")
        tiempo_inicio = time.time()
        try:
            similitud_jacc = similitud_jaccard(muestra1, muestra2, n)
            similitud_jacc_pond = similitud_jaccard_ponderada(muestra1, muestra2, n)
            tiempo_jacc = time.time() - tiempo_inicio
            
            resultados.append({
                'etapa': 'Etapa 5',
                'algoritmo': f'Jaccard {n}-gramas',
                'similitud': similitud_jacc,
                'tiempo': tiempo_jacc,
                'detalles': f'Ponderada: {similitud_jacc_pond:.2f}%',
                'complejidad_tiempo': 'O(n+m)',
                'complejidad_espacio': 'O(n+m)'
            })
            print(f"✓ Completado en {tiempo_jacc:.4f}s - Similitud: {similitud_jacc:.2f}%")
        except Exception as e:
            print(f"✗ Error en Jaccard {n}-gramas: {e}")
    
    return resultados


def mostrar_tabla_comparativa(resultados):
    """Muestra una tabla comparativa de todos los resultados."""
    print("\n" + "="*80)
    print("TABLA COMPARATIVA DE RESULTADOS")
    print("="*80)
    
    # Encabezados
    print(f"\n{'Algoritmo':^35} | {'Etapa':^8} | {'Similitud':^11} | {'Tiempo':^10} | {'Complejidad'}")
    print("-" * 80)
    
    # Ordenar por similitud descendente
    resultados_ordenados = sorted(resultados, key=lambda x: x['similitud'], reverse=True)
    
    for res in resultados_ordenados:
        comp_str = f"{res.get('complejidad_tiempo', 'N/A')}"
        print(f"{res['algoritmo']:35} | {res['etapa']:^8} | {res['similitud']:>9.2f}% | "
              f"{res['tiempo']:>8.4f}s | {comp_str}")
        print(f"{'':37}   {'':8}   {'':11}   {'':10}   └─ {res.get('detalles', '')}")
    
    print("-" * 80)


def analizar_resultados(resultados):
    """Realiza un análisis estadístico de los resultados."""
    print("\n" + "="*80)
    print("ANÁLISIS ESTADÍSTICO")
    print("="*80)
    
    similitudes = [r['similitud'] for r in resultados]
    tiempos = [r['tiempo'] for r in resultados]
    
    print(f"\n📊 Similitud:")
    print(f"   Máxima:    {max(similitudes):>8.2f}%  ({[r['algoritmo'] for r in resultados if r['similitud'] == max(similitudes)][0]})")
    print(f"   Mínima:    {min(similitudes):>8.2f}%  ({[r['algoritmo'] for r in resultados if r['similitud'] == min(similitudes)][0]})")
    print(f"   Promedio:  {sum(similitudes)/len(similitudes):>8.2f}%")
    print(f"   Mediana:   {sorted(similitudes)[len(similitudes)//2]:>8.2f}%")
    
    print(f"\n⏱️  Tiempo de ejecución:")
    print(f"   Más rápido:  {min(tiempos):>8.4f}s  ({[r['algoritmo'] for r in resultados if r['tiempo'] == min(tiempos)][0]})")
    print(f"   Más lento:   {max(tiempos):>8.4f}s  ({[r['algoritmo'] for r in resultados if r['tiempo'] == max(tiempos)][0]})")
    print(f"   Promedio:    {sum(tiempos)/len(tiempos):>8.4f}s")
    print(f"   Total:       {sum(tiempos):>8.4f}s")
    
    # Eficiencia (similitud / tiempo)
    print(f"\n⚡ Eficiencia (similitud / tiempo):")
    eficiencias = [(r['similitud'] / r['tiempo'], r['algoritmo']) for r in resultados]
    eficiencias.sort(reverse=True)
    
    for i, (ef, alg) in enumerate(eficiencias[:3], 1):
        print(f"   {i}. {alg:35} : {ef:>8.2f} pts/s")


def mostrar_recomendaciones(resultados):
    """Muestra recomendaciones basadas en los resultados."""
    print("\n" + "="*80)
    print("RECOMENDACIONES Y CONCLUSIONES")
    print("="*80)
    
    # Encontrar los mejores en cada categoría
    mejor_precision = max(resultados, key=lambda x: x['similitud'])
    mas_rapido = min(resultados, key=lambda x: x['tiempo'])
    
    # Calcular eficiencia
    for r in resultados:
        r['eficiencia'] = r['similitud'] / r['tiempo']
    mejor_equilibrio = max(resultados, key=lambda x: x['eficiencia'])
    
    print(f"\n🎯 Para MÁXIMA PRECISIÓN:")
    print(f"   ➜ {mejor_precision['algoritmo']}")
    print(f"     Similitud: {mejor_precision['similitud']:.2f}%")
    print(f"     Tiempo: {mejor_precision['tiempo']:.4f}s")
    print(f"     Uso ideal: Cuando necesitas la medida más precisa de similitud")
    
    print(f"\n⚡ Para MÁXIMA VELOCIDAD:")
    print(f"   ➜ {mas_rapido['algoritmo']}")
    print(f"   Tiempo: {mas_rapido['tiempo']:.4f}s")
    print(f"     Similitud: {mas_rapido['similitud']:.2f}%")
    print(f"     Uso ideal: Comparaciones rápidas de muchos documentos")
    
    print(f"\n⚖️  Para MEJOR EQUILIBRIO (precisión/velocidad):")
    print(f"   ➜ {mejor_equilibrio['algoritmo']}")
    print(f"     Similitud: {mejor_equilibrio['similitud']:.2f}%")
    print(f"     Tiempo: {mejor_equilibrio['tiempo']:.4f}s")
    print(f"     Eficiencia: {mejor_equilibrio['eficiencia']:.2f} pts/s")
    print(f"     Uso ideal: Uso general cuando importa tanto velocidad como precisión")
    
    print(f"\n📝 Casos de uso específicos:")
    print(f"   • Detección de plagio/duplicados:")
    jaccard = [r for r in resultados if 'Jaccard' in r['algoritmo']]
    if jaccard:
        mejor_jaccard = max(jaccard, key=lambda x: x['similitud'])
        print(f"     ➜ {mejor_jaccard['algoritmo']} - {mejor_jaccard['similitud']:.2f}%")
    
    print(f"   • Encontrar subsecuencias exactas comunes:")
    lcs_algs = [r for r in resultados if 'LCS' in r['algoritmo'] or 'Hirschberg' in r['algoritmo']]
    if lcs_algs:
        mejor_lcs = max(lcs_algs, key=lambda x: x['similitud'])
        print(f"     ➜ {mejor_lcs['algoritmo']} - {mejor_lcs['similitud']:.2f}%")
    
    print(f"   • Textos con errores tipográficos:")
    lev = [r for r in resultados if 'Levenshtein' in r['algoritmo']]
    if lev:
        print(f"     ➜ {lev[0]['algoritmo']} - {lev[0]['similitud']:.2f}%")
    
    print(f"\n💡 Conclusión general:")
    promedio_similitud = sum(r['similitud'] for r in resultados) / len(resultados)
    
    if promedio_similitud > 70:
        conclusion = "Los textos son MUY SIMILARES"
    elif promedio_similitud > 40:
        conclusion = "Los textos tienen SIMILITUD MODERADA"
    elif promedio_similitud > 20:
        conclusion = "Los textos tienen BAJA SIMILITUD"
    else:
        conclusion = "Los textos son MUY DIFERENTES"
    
    print(f"   {conclusion} (promedio: {promedio_similitud:.2f}%)")
    print(f"   Todos los algoritmos coinciden en tendencias generales,")
    print(f"   pero cada uno aporta una perspectiva diferente sobre la similitud.")


def main():
    """Función principal."""
    print("="*80)
    print("COMPARACIÓN COMPLETA: ETAPAS 3, 4 y 5")
    print("="*80)
    
    # Determinar la ruta base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir
    
    # Si estamos en etapa5_algoritmos, subir un nivel
    if os.path.basename(script_dir) == 'etapa5_algoritmos':
        base_dir = os.path.dirname(script_dir)
    
    # Archivos a comparar
    archivo1 = os.path.join(base_dir, "books/procesados", "manifesto_limpio.txt")
    archivo2 = os.path.join(base_dir, "books/procesados", "capital-v1_limpio.txt")
    
    print(f"\n📁 Cargando archivos...")
    texto1 = leer_archivo(archivo1)
    texto2 = leer_archivo(archivo2)
    
    if not texto1 or not texto2:
        print("❌ Error: No se pudieron leer los archivos.")
        return
    
    print(f"✓ Archivos cargados:")
    print(f"   - {os.path.basename(archivo1)}: {len(texto1):,} caracteres")
    print(f"   - {os.path.basename(archivo2)}: {len(texto2):,} caracteres")
    
    # Ejecutar comparación
    resultados = ejecutar_comparacion_completa(texto1, texto2, max_chars=5000)
    
    # Mostrar resultados
    mostrar_tabla_comparativa(resultados)
    analizar_resultados(resultados)
    mostrar_recomendaciones(resultados)
    
    print("\n" + "="*80)
    print("✓ Análisis completo finalizado")
    print("="*80)


if __name__ == "__main__":
    main()
