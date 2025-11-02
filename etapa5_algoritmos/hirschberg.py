"""
Algoritmo de Hirschberg para encontrar la subsecuencia común más larga (LCS)
con complejidad de espacio O(min(m,n)) en lugar de O(m*n).

El algoritmo de Hirschberg es una optimización del algoritmo clásico de LCS
que utiliza la técnica de "divide y vencerás" combinada con el algoritmo de 
Needleman-Wunsch para reducir el uso de memoria.

Ventajas:
- Complejidad de tiempo: O(m*n) (igual que el LCS tradicional)
- Complejidad de espacio: O(min(m,n)) (mejor que O(m*n) del tradicional)
- Útil para textos muy largos donde la memoria es limitada
- Reconstruye la subsecuencia completa

Pseudo-código:
    NWScore(X, Y):
        Entrada: Dos strings X y Y
        Salida: Array con scores de la última fila
        
        Crear arrays Score_current y Score_previous de tamaño len(Y)+1
        Inicializar Score_previous con 0s
        
        Para cada carácter x en X:
            Score_current[0] = 0
            Para cada posición j de 1 a len(Y):
                Si x == Y[j-1]:
                    Score_current[j] = Score_previous[j-1] + 1
                Sino:
                    Score_current[j] = max(Score_current[j-1], Score_previous[j])
            Score_previous = Score_current
        
        Regresar Score_current
    
    Hirschberg(X, Y):
        Entrada: Dos strings X y Y
        Salida: La subsecuencia común más larga
        
        Si X está vacío:
            Regresar ""
        Si len(X) == 1:
            Si X[0] en Y:
                Regresar X[0]
            Sino:
                Regresar ""
        
        i = len(X) // 2
        Score_L = NWScore(X[:i], Y)
        Score_R = NWScore(X[i:][::-1], Y[::-1])
        
        Encontrar j que maximiza Score_L[j] + Score_R[len(Y)-j]
        
        Regresar Hirschberg(X[:i], Y[:j]) + Hirschberg(X[i:], Y[j:])
"""


def nw_score(X, Y):
    """
    Calcula los scores de la última fila usando el algoritmo de Needleman-Wunsch.
    Solo mantiene dos filas en memoria en lugar de la matriz completa.
    
    Args:
        X: Primer string
        Y: Segundo string
    
    Returns:
        Lista con los scores de la última fila
    """
    m, n = len(X), len(Y)
    
    # Solo necesitamos dos filas: la anterior y la actual
    score_previous = [0] * (n + 1)
    score_current = [0] * (n + 1)
    
    for i in range(1, m + 1):
        score_current[0] = 0
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                score_current[j] = score_previous[j-1] + 1
            else:
                score_current[j] = max(score_current[j-1], score_previous[j])
        
        # La fila actual se convierte en la anterior para la siguiente iteración
        score_previous = score_current[:]
    
    return score_current


def hirschberg(X, Y):
    """
    Implementación del algoritmo de Hirschberg para encontrar el LCS
    con complejidad de espacio O(min(m,n)).
    
    Args:
        X: Primer string
        Y: Segundo string
    
    Returns:
        Tupla (longitud_lcs, subsecuencia_lcs)
    """
    m, n = len(X), len(Y)
    
    # Casos base
    if m == 0 or n == 0:
        return 0, ""
    
    if m == 1:
        if X[0] in Y:
            return 1, X[0]
        else:
            return 0, ""
    
    if n == 1:
        if Y[0] in X:
            return 1, Y[0]
        else:
            return 0, ""
    
    # Dividir X por la mitad
    i = m // 2
    
    # Calcular scores para la primera mitad de X vs todo Y
    score_L = nw_score(X[:i], Y)
    
    # Calcular scores para la segunda mitad de X (invertida) vs Y invertido
    score_R = nw_score(X[i:][::-1], Y[::-1])
    
    # Encontrar el punto de división óptimo en Y
    # Buscamos j que maximiza score_L[j] + score_R[n-j]
    max_score = -1
    partition = 0
    
    for j in range(n + 1):
        score = score_L[j] + score_R[n - j]
        if score > max_score:
            max_score = score
            partition = j
    
    # Recursivamente resolver para las dos mitades
    left_length, left_lcs = hirschberg(X[:i], Y[:partition])
    right_length, right_lcs = hirschberg(X[i:], Y[partition:])
    
    # Combinar resultados
    total_length = left_length + right_length
    total_lcs = left_lcs + right_lcs
    
    return total_length, total_lcs


def hirschberg_con_bloques(texto1, texto2, tamaño_bloque=10000):
    """
    Versión de Hirschberg que divide textos muy grandes en bloques
    para hacerlo más práctico con archivos enormes.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        tamaño_bloque: Tamaño máximo de cada bloque
    
    Returns:
        Diccionario con resultados de la mejor comparación
    """
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        longitud, fragmento = hirschberg(texto1, texto2)
        return {
            'longitud_lcs': longitud,
            'fragmento': fragmento[:500] if len(fragmento) > 500 else fragmento,
            'metodo': 'directo'
        }
    
    # Dividir en bloques
    bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
    bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
    
    mejor_longitud = 0
    mejor_fragmento = ""
    mejor_par = (0, 0)
    
    # Limitar comparaciones si hay demasiados bloques
    max_comparaciones = 25  # Reducido para mayor velocidad
    total_comparaciones = len(bloques1) * len(bloques2)
    
    if total_comparaciones > max_comparaciones:
        # Muestreo: tomar solo algunos bloques
        step1 = max(1, len(bloques1) // 5)
        step2 = max(1, len(bloques2) // 5)
        bloques1_muestra = bloques1[::step1]
        bloques2_muestra = bloques2[::step2]
    else:
        bloques1_muestra = bloques1
        bloques2_muestra = bloques2
    
    total = len(bloques1_muestra) * len(bloques2_muestra)
    actual = 0
    
    for i, bloque1 in enumerate(bloques1_muestra):
        for j, bloque2 in enumerate(bloques2_muestra):
            actual += 1
            print(f"   Hirschberg: {actual}/{total} ({actual*100//total}%)...", end='\r')
            
            longitud, fragmento = hirschberg(bloque1, bloque2)
            
            if longitud > mejor_longitud:
                mejor_longitud = longitud
                mejor_fragmento = fragmento
                mejor_par = (i, j)
    
    print()  # Nueva línea
    
    return {
        'longitud_lcs': mejor_longitud,
        'fragmento': mejor_fragmento[:500] if len(mejor_fragmento) > 500 else mejor_fragmento,
        'mejor_par': mejor_par,
        'total_bloques': (len(bloques1_muestra), len(bloques2_muestra)),
        'metodo': 'bloques'
    }


def calcular_similitud_hirschberg(texto1, texto2):
    """
    Calcula el porcentaje de similitud basado en el LCS de Hirschberg.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
    
    Returns:
        Porcentaje de similitud (0-100)
    """
    if len(texto1) == 0 and len(texto2) == 0:
        return 100.0
    
    if len(texto1) == 0 or len(texto2) == 0:
        return 0.0
    
    longitud_lcs, _ = hirschberg(texto1, texto2)
    
    # Similitud basada en la longitud promedio
    similitud = (2 * longitud_lcs) / (len(texto1) + len(texto2)) * 100
    
    return similitud
