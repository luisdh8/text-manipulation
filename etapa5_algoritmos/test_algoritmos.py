"""
Script de prueba simple para verificar que todos los algoritmos funcionan
"""

try:
    from hirschberg import hirschberg, calcular_similitud_hirschberg
    from levenshtein import levenshtein_distancia_optimizado, similitud_levenshtein
    from jaccard_ngram import similitud_jaccard, similitud_jaccard_ponderada
except ModuleNotFoundError:
    from etapa5_algoritmos.hirschberg import hirschberg, calcular_similitud_hirschberg
    from etapa5_algoritmos.levenshtein import levenshtein_distancia_optimizado, similitud_levenshtein
    from etapa5_algoritmos.jaccard_ngram import similitud_jaccard, similitud_jaccard_ponderada


def test_algoritmos():
    """Prueba rápida de todos los algoritmos con textos pequeños."""
    print("="*70)
    print("PRUEBA DE ALGORITMOS - ETAPA 5")
    print("="*70)
    
    # Textos de prueba
    texto1 = "El algoritmo de programación dinámica es muy eficiente"
    texto2 = "El algoritmo de programacion dinamica es eficiente"
    
    print(f"\nTexto 1: {texto1}")
    print(f"Texto 2: {texto2}")
    print(f"\nLongitudes: {len(texto1)} y {len(texto2)} caracteres")
    
    # Test Hirschberg
    print(f"\n{'1. HIRSCHBERG':-^70}")
    try:
        longitud, subsecuencia = hirschberg(texto1, texto2)
        similitud = (2 * longitud) / (len(texto1) + len(texto2)) * 100
        print(f"✓ Longitud LCS: {longitud}")
        print(f"✓ Similitud: {similitud:.2f}%")
        print(f"✓ Subsecuencia: {subsecuencia[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test Levenshtein
    print(f"\n{'2. LEVENSHTEIN':-^70}")
    try:
        distancia = levenshtein_distancia_optimizado(texto1, texto2)
        similitud = similitud_levenshtein(texto1, texto2)
        print(f"✓ Distancia: {distancia}")
        print(f"✓ Similitud: {similitud:.2f}%")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test Jaccard
    print(f"\n{'3. JACCARD N-GRAMAS':-^70}")
    for n in [2, 3, 4]:
        try:
            similitud_simple = similitud_jaccard(texto1, texto2, n)
            similitud_pond = similitud_jaccard_ponderada(texto1, texto2, n)
            print(f"✓ {n}-gramas: {similitud_simple:.2f}% (ponderada: {similitud_pond:.2f}%)")
        except Exception as e:
            print(f"✗ Error en {n}-gramas: {e}")
    
    print("\n" + "="*70)
    print("✓ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*70)
    
    # Ejemplo con textos más diferentes
    print(f"\n{'EJEMPLO 2: TEXTOS MÁS DIFERENTES':-^70}")
    
    texto3 = "Python es un lenguaje de programación"
    texto4 = "Java es otro lenguaje de programación"
    
    print(f"\nTexto 3: {texto3}")
    print(f"Texto 4: {texto4}")
    
    print(f"\nComparación rápida:")
    try:
        _, subsec = hirschberg(texto3, texto4)
        sim_lev = similitud_levenshtein(texto3, texto4)
        sim_jacc = similitud_jaccard(texto3, texto4, 3)
        
        print(f"  Hirschberg LCS: {subsec}")
        print(f"  Levenshtein: {sim_lev:.2f}%")
        print(f"  Jaccard 3-gramas: {sim_jacc:.2f}%")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_algoritmos()
