"""
Comparación entre algoritmos de Longest Common Substring:
1. Algoritmo clásico (Programación Dinámica) - O(n*m) tiempo y espacio
2. Rabin-Karp con rolling hash - O(n+m) tiempo promedio

Este script ejecuta ambos algoritmos y compara sus resultados.
"""

import time
from pathlib import Path

# Importar los algoritmos
from longest_common_substring import lcSub, analizar_textos
from rabin_karp_substring import (
    rabin_karp_longest_substring,
    rabin_karp_simple,
    analizar_textos_rabin_karp
)


def leer_archivo(nombre_archivo):
    """Lee un archivo de texto desde books/procesados"""
    ruta_base = Path(__file__).parent.parent
    ruta_archivo = ruta_base / 'books' / 'procesados' / nombre_archivo
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        return None


def comparacion_algoritmos_simple(texto1, texto2, nombre1, nombre2, max_chars=5000):
    """
    Compara ambos algoritmos en textos pequeños (para comparación directa)
    
    Args:
        texto1, texto2: Textos a comparar
        nombre1, nombre2: Nombres de los textos
        max_chars: Máximo de caracteres a usar (para mantener tiempos razonables)
    """
    # Limitar tamaño para comparación justa
    texto1_muestra = texto1[:max_chars]
    texto2_muestra = texto2[:max_chars]
    
    print("\n" + "="*80)
    print(f"COMPARACIÓN DIRECTA DE ALGORITMOS")
    print("="*80)
    print(f"Texto 1: {nombre1} (muestra de {len(texto1_muestra):,} caracteres)")
    print(f"Texto 2: {nombre2} (muestra de {len(texto2_muestra):,} caracteres)")
    print()
    
    resultados = []
    
    # 1. Algoritmo clásico (Programación Dinámica)
    print("1️⃣  Ejecutando: Algoritmo Clásico (Programación Dinámica)")
    print("   Complejidad: O(n*m) tiempo, O(n*m) espacio")
    tiempo_inicio = time.time()
    longitud_clasico, substring_clasico = lcSub(texto1_muestra, texto2_muestra)
    tiempo_clasico = time.time() - tiempo_inicio
    
    print(f"   ✓ Completado en {tiempo_clasico:.4f} segundos")
    print(f"   → Longitud encontrada: {longitud_clasico:,} caracteres")
    
    resultados.append({
        'algoritmo': 'Programación Dinámica (Clásico)',
        'longitud': longitud_clasico,
        'tiempo': tiempo_clasico,
        'substring': substring_clasico,
        'complejidad_tiempo': 'O(n*m)',
        'complejidad_espacio': 'O(n*m)'
    })
    
    # 2. Rabin-Karp con búsqueda binaria
    print("\n2️⃣  Ejecutando: Rabin-Karp (Búsqueda binaria + Rolling hash)")
    print("   Complejidad: O(n+m) promedio, O(n*m) peor caso")
    tiempo_inicio = time.time()
    longitud_rk_bin, substring_rk_bin = rabin_karp_longest_substring(texto1_muestra, texto2_muestra)
    tiempo_rk_bin = time.time() - tiempo_inicio
    
    print(f"   ✓ Completado en {tiempo_rk_bin:.4f} segundos")
    print(f"   → Longitud encontrada: {longitud_rk_bin:,} caracteres")
    
    resultados.append({
        'algoritmo': 'Rabin-Karp (Binaria)',
        'longitud': longitud_rk_bin,
        'tiempo': tiempo_rk_bin,
        'substring': substring_rk_bin,
        'complejidad_tiempo': 'O(n+m) prom.',
        'complejidad_espacio': 'O(n+m)'
    })
    
    # 3. Rabin-Karp versión simple
    print("\n3️⃣  Ejecutando: Rabin-Karp (Búsqueda lineal + Rolling hash)")
    print("   Complejidad: O(n*L) donde L es la longitud del substring")
    tiempo_inicio = time.time()
    longitud_rk_simple, substring_rk_simple = rabin_karp_simple(texto1_muestra, texto2_muestra)
    tiempo_rk_simple = time.time() - tiempo_inicio
    
    print(f"   ✓ Completado en {tiempo_rk_simple:.4f} segundos")
    print(f"   → Longitud encontrada: {longitud_rk_simple:,} caracteres")
    
    resultados.append({
        'algoritmo': 'Rabin-Karp (Lineal)',
        'longitud': longitud_rk_simple,
        'tiempo': tiempo_rk_simple,
        'substring': substring_rk_simple,
        'complejidad_tiempo': 'O(n*L)',
        'complejidad_espacio': 'O(n+m)'
    })
    
    # Mostrar tabla comparativa
    print("\n" + "="*80)
    print("TABLA COMPARATIVA DE RESULTADOS")
    print("="*80)
    print(f"{'Algoritmo':<30} {'Longitud':<12} {'Tiempo (s)':<12} {'Complejidad':<15}")
    print("-"*80)
    
    for r in resultados:
        print(f"{r['algoritmo']:<30} {r['longitud']:<12,} {r['tiempo']:<12.4f} {r['complejidad_tiempo']:<15}")
    
    # Análisis de resultados
    print("\n" + "="*80)
    print("ANÁLISIS DE RESULTADOS")
    print("="*80)
    
    # Verificar que todos encuentren el mismo substring
    longitudes = [r['longitud'] for r in resultados]
    if len(set(longitudes)) == 1:
        print("✓ Todos los algoritmos encontraron la misma longitud")
    else:
        print("⚠ ADVERTENCIA: Los algoritmos encontraron longitudes diferentes")
        for r in resultados:
            print(f"  • {r['algoritmo']}: {r['longitud']}")
    
    # Comparar velocidades
    tiempo_min = min(r['tiempo'] for r in resultados)
    print(f"\n🏆 Algoritmo más rápido:")
    for r in resultados:
        if r['tiempo'] == tiempo_min:
            print(f"   {r['algoritmo']} ({r['tiempo']:.4f} segundos)")
            speedup_clasico = resultados[0]['tiempo'] / r['tiempo']
            print(f"   Speedup vs clásico: {speedup_clasico:.2f}x")
    
    # Mostrar fragmentos si son diferentes
    print(f"\n📝 Substring común más largo encontrado:")
    substring_mostrar = resultados[0]['substring']
    if len(substring_mostrar) <= 200:
        print(f'   "{substring_mostrar}"')
    else:
        print(f'   Inicio: "{substring_mostrar[:100]}"')
        print(f'   Final:  "{substring_mostrar[-100:]}"')
    
    return resultados


def comparacion_textos_completos():
    """Ejecuta ambos algoritmos en textos completos usando bloques"""
    
    print("\n" + "="*80)
    print("COMPARACIÓN EN TEXTOS COMPLETOS (CON BLOQUES)")
    print("="*80)
    
    # Buscar archivos
    ruta_base = Path(__file__).parent.parent
    carpeta_procesados = ruta_base / 'books' / 'procesados'
    archivos_limpios = list(carpeta_procesados.glob('*_limpio.txt'))
    
    if len(archivos_limpios) < 2:
        print("Error: Se necesitan al menos 2 archivos")
        return
    
    # Leer textos
    textos = {}
    for archivo in archivos_limpios[:2]:  # Solo primeros 2 para la demo
        contenido = leer_archivo(archivo.name)
        if contenido:
            textos[archivo.name] = contenido
    
    nombres = list(textos.keys())
    archivo1, archivo2 = nombres[0], nombres[1]
    
    print(f"\nComparando:")
    print(f"  • {archivo1}: {len(textos[archivo1]):,} caracteres")
    print(f"  • {archivo2}: {len(textos[archivo2]):,} caracteres")
    
    # Ejecutar algoritmo clásico con bloques
    print("\n" + "-"*80)
    resultado_clasico = analizar_textos(
        textos[archivo1], textos[archivo2],
        archivo1, archivo2
    )
    
    # Ejecutar Rabin-Karp con bloques
    print("\n" + "-"*80)
    resultado_rk = analizar_textos_rabin_karp(
        textos[archivo1], textos[archivo2],
        archivo1, archivo2,
        usar_binaria=True
    )
    
    # Comparar resultados
    print("\n" + "="*80)
    print("COMPARACIÓN FINAL")
    print("="*80)
    print(f"{'Métrica':<30} {'Clásico':<20} {'Rabin-Karp':<20}")
    print("-"*80)
    print(f"{'Longitud encontrada':<30} {resultado_clasico['longitud']:<20,} {resultado_rk['longitud']:<20,}")
    print(f"{'Tiempo de ejecución':<30} {resultado_clasico['tiempo']:<20.4f} {resultado_rk['tiempo']:<20.4f}")
    print(f"{'Similitud (%)':<30} {resultado_clasico['porcentaje']:<20.2f} {resultado_rk['porcentaje']:<20.2f}")
    
    if resultado_rk['tiempo'] < resultado_clasico['tiempo']:
        speedup = resultado_clasico['tiempo'] / resultado_rk['tiempo']
        print(f"\n🏆 Rabin-Karp fue {speedup:.2f}x más rápido")
    else:
        slowdown = resultado_rk['tiempo'] / resultado_clasico['tiempo']
        print(f"\n⚠ Rabin-Karp fue {slowdown:.2f}x más lento (posiblemente por colisiones)")


def main():
    """Función principal"""
    
    print("="*80)
    print("COMPARACIÓN DE ALGORITMOS DE LONGEST COMMON SUBSTRING")
    print("="*80)
    print("\nAlgoritmos a comparar:")
    print("1. Programación Dinámica (Clásico) - O(n*m)")
    print("2. Rabin-Karp con búsqueda binaria - O(n+m) promedio")
    print("3. Rabin-Karp con búsqueda lineal - O(n*L)")
    
    # Leer archivos de prueba
    ruta_base = Path(__file__).parent.parent
    carpeta_procesados = ruta_base / 'books' / 'procesados'
    archivos_limpios = list(carpeta_procesados.glob('*_limpio.txt'))
    
    if len(archivos_limpios) < 2:
        print("\nError: Se necesitan al menos 2 archivos de texto limpios")
        return
    
    # Leer primeros dos archivos
    archivo1 = archivos_limpios[0].name
    archivo2 = archivos_limpios[1].name
    
    texto1 = leer_archivo(archivo1)
    texto2 = leer_archivo(archivo2)
    
    if not texto1 or not texto2:
        print("Error al leer los archivos")
        return
    
    # 1. Comparación con muestras pequeñas (comparación directa justa)
    print("\n" + "="*80)
    print("PARTE 1: COMPARACIÓN DIRECTA CON MUESTRAS PEQUEÑAS")
    print("="*80)
    comparacion_algoritmos_simple(texto1, texto2, archivo1, archivo2, max_chars=5000)
    
    # 2. Comparación con textos completos usando bloques
    print("\n\n" + "="*80)
    print("PARTE 2: COMPARACIÓN CON TEXTOS COMPLETOS")
    print("="*80)
    comparacion_textos_completos()
    
    print("\n" + "="*80)
    print("CONCLUSIONES")
    print("="*80)
    print("""
Rabin-Karp ofrece ventajas significativas:

✓ Ventajas:
  • Más rápido en promedio: O(n+m) vs O(n*m)
  • Menos uso de memoria: O(n+m) vs O(n*m)
  • Rolling hash permite actualizaciones eficientes
  • Ideal para textos muy grandes
  • Encuentra múltiples coincidencias naturalmente

⚠ Desventajas:
  • Posibles colisiones de hash (raras con buen hash)
  • Peor caso sigue siendo O(n*m)
  • Más complejo de implementar correctamente

🎯 Recomendación:
  Usar Rabin-Karp para textos grandes donde la velocidad es crítica.
  El algoritmo clásico es más simple y garantiza exactitud total.
    """)
    
    print("="*80)


if __name__ == "__main__":
    main()
