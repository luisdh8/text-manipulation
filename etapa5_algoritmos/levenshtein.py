"""
Distancia de Edición (Levenshtein Distance)

La distancia de Levenshtein mide el número mínimo de operaciones de edición 
(inserciones, eliminaciones o sustituciones) necesarias para transformar 
un string en otro.

Ventajas:
- Mide qué tan diferentes son dos textos
- Considera sustituciones además de inserciones/eliminaciones
- Útil para detectar errores tipográficos y variaciones
- Ampliamente usado en corrección ortográfica y bioinformática

Pseudo-código:
    Levenshtein(S1, S2):
        Entrada: Dos strings S1 y S2 de longitudes n y m
        Salida: La distancia de edición mínima entre S1 y S2
        
        Crear matriz d de tamaño (n+1) x (m+1)
        
        # Inicializar primera columna (0, 1, 2, ..., n)
        Para i de 0 a n:
            d[i][0] = i
        
        # Inicializar primera fila (0, 1, 2, ..., m)
        Para j de 0 a m:
            d[0][j] = j
        
        # Llenar la matriz
        Para i de 1 a n:
            Para j de 1 a m:
                Si S1[i-1] == S2[j-1]:
                    costo_sustitucion = 0
                Sino:
                    costo_sustitucion = 1
                
                d[i][j] = min(
                    d[i-1][j] + 1,           # eliminación
                    d[i][j-1] + 1,           # inserción
                    d[i-1][j-1] + costo_sustitucion  # sustitución
                )
        
        Regresar d[n][m]

Complejidad:
- Tiempo: O(n * m)
- Espacio: O(n * m) (puede optimizarse a O(min(n,m)))
"""


def levenshtein_distancia(s1, s2):
    """
    Calcula la distancia de Levenshtein entre dos strings.
    
    Args:
        s1: Primer string
        s2: Segundo string
    
    Returns:
        La distancia de edición (número de operaciones necesarias)
    """
    n, m = len(s1), len(s2)
    
    # Casos especiales
    if n == 0:
        return m
    if m == 0:
        return n
    
    # Crear matriz de distancias
    d = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Inicializar primera columna
    for i in range(n + 1):
        d[i][0] = i
    
    # Inicializar primera fila
    for j in range(m + 1):
        d[0][j] = j
    
    # Llenar la matriz usando programación dinámica
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                costo_sustitucion = 0
            else:
                costo_sustitucion = 1
            
            d[i][j] = min(
                d[i-1][j] + 1,                    # eliminación
                d[i][j-1] + 1,                    # inserción
                d[i-1][j-1] + costo_sustitucion   # sustitución
            )
    
    return d[n][m]


def levenshtein_distancia_optimizado(s1, s2):
    """
    Versión optimizada en espacio de la distancia de Levenshtein.
    Solo mantiene dos filas en memoria en lugar de la matriz completa.
    
    Args:
        s1: Primer string
        s2: Segundo string
    
    Returns:
        La distancia de edición
    """
    n, m = len(s1), len(s2)
    
    if n == 0:
        return m
    if m == 0:
        return n
    
    # Asegurar que s2 sea el más corto para optimizar espacio
    if n > m:
        s1, s2 = s2, s1
        n, m = m, n
    
    # Solo necesitamos dos filas
    fila_anterior = list(range(m + 1))
    fila_actual = [0] * (m + 1)
    
    for i in range(1, n + 1):
        fila_actual[0] = i
        
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                costo_sustitucion = 0
            else:
                costo_sustitucion = 1
            
            fila_actual[j] = min(
                fila_anterior[j] + 1,              # eliminación
                fila_actual[j-1] + 1,              # inserción
                fila_anterior[j-1] + costo_sustitucion  # sustitución
            )
        
        fila_anterior, fila_actual = fila_actual, fila_anterior
    
    return fila_anterior[m]


def similitud_levenshtein(s1, s2):
    """
    Calcula el porcentaje de similitud basado en la distancia de Levenshtein.
    
    La similitud se calcula como:
    similitud = (1 - distancia / max_longitud) * 100
    
    Args:
        s1: Primer string
        s2: Segundo string
    
    Returns:
        Porcentaje de similitud (0-100)
    """
    if len(s1) == 0 and len(s2) == 0:
        return 100.0
    
    max_longitud = max(len(s1), len(s2))
    
    if max_longitud == 0:
        return 100.0
    
    distancia = levenshtein_distancia_optimizado(s1, s2)
    
    # Convertir distancia a similitud
    similitud = (1 - distancia / max_longitud) * 100
    
    return max(0, similitud)  # Asegurar que no sea negativo


def levenshtein_con_bloques(texto1, texto2, tamaño_bloque=5000):
    """
    Aplica Levenshtein a bloques de texto para manejar textos grandes.
    Compara bloques y reporta el promedio y el mejor caso.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        tamaño_bloque: Tamaño de cada bloque
    
    Returns:
        Diccionario con resultados de similitud
    """
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        distancia = levenshtein_distancia_optimizado(texto1, texto2)
        similitud = similitud_levenshtein(texto1, texto2)
        return {
            'distancia': distancia,
            'similitud': similitud,
            'metodo': 'directo'
        }
    
    # Dividir en bloques
    bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
    bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
    
    # Limitar comparaciones agresivamente
    max_comparaciones = 25  # Reducido significativamente
    total_comparaciones = len(bloques1) * len(bloques2)
    
    if total_comparaciones > max_comparaciones:
        step1 = max(1, len(bloques1) // 5)
        step2 = max(1, len(bloques2) // 5)
        bloques1_muestra = bloques1[::step1]
        bloques2_muestra = bloques2[::step2]
    else:
        bloques1_muestra = bloques1
        bloques2_muestra = bloques2
    
    similitudes = []
    distancias = []
    mejor_similitud = 0
    mejor_distancia = float('inf')
    mejor_par = (0, 0)
    
    total = len(bloques1_muestra) * len(bloques2_muestra)
    actual = 0
    
    for i, bloque1 in enumerate(bloques1_muestra):
        for j, bloque2 in enumerate(bloques2_muestra):
            actual += 1
            print(f"   Levenshtein: {actual}/{total} ({actual*100//total}%)...", end='\r')
            
            distancia = levenshtein_distancia_optimizado(bloque1, bloque2)
            similitud = similitud_levenshtein(bloque1, bloque2)
            
            similitudes.append(similitud)
            distancias.append(distancia)
            
            if similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_distancia = distancia
                mejor_par = (i, j)
    
    print()  # Nueva línea
    
    return {
        'distancia_promedio': sum(distancias) / len(distancias),
        'similitud_promedio': sum(similitudes) / len(similitudes),
        'mejor_distancia': mejor_distancia,
        'mejor_similitud': mejor_similitud,
        'similitud': mejor_similitud,  # Para compatibilidad
        'mejor_par': mejor_par,
        'total_bloques': (len(bloques1_muestra), len(bloques2_muestra)),
        'metodo': 'bloques'
    }


def reconstruir_ediciones(s1, s2):
    """
    Reconstruye la secuencia de operaciones de edición necesarias.
    
    Args:
        s1: String original
        s2: String destino
    
    Returns:
        Lista de operaciones (tipo, posición, carácter)
    """
    n, m = len(s1), len(s2)
    
    # Crear matriz de distancias
    d = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                costo = 0
            else:
                costo = 1
            
            d[i][j] = min(
                d[i-1][j] + 1,
                d[i][j-1] + 1,
                d[i-1][j-1] + costo
            )
    
    # Reconstruir las operaciones
    operaciones = []
    i, j = n, m
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            # Coincidencia, no hay operación
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and d[i][j] == d[i-1][j-1] + 1:
            # Sustitución
            operaciones.append(('sustituir', i-1, s1[i-1], s2[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and d[i][j] == d[i-1][j] + 1:
            # Eliminación
            operaciones.append(('eliminar', i-1, s1[i-1]))
            i -= 1
        else:
            # Inserción
            operaciones.append(('insertar', j-1, s2[j-1]))
            j -= 1
    
    operaciones.reverse()
    return operaciones
