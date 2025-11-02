"""
Similitud de Jaccard con n-gramas

La similitud de Jaccard mide el tamaño de la intersección dividido por 
el tamaño de la unión de dos conjuntos. Aplicado a n-gramas, divide los 
textos en fragmentos de n caracteres consecutivos y compara cuántos se comparten.

Ventajas:
- No requiere que los fragmentos estén en el mismo orden
- Muy eficiente computacionalmente O(n + m)
- Robusto ante reordenamientos de texto
- Funciona bien para detectar plagio y textos similares
- Permite ajustar la granularidad con diferentes tamaños de n-gramas

N-gramas:
- Unigrama (n=1): caracteres individuales
- Bigrama (n=2): pares de caracteres consecutivos
- Trigrama (n=3): tríos de caracteres consecutivos
- etc.

Ejemplo con bigramas:
    "hola" -> {"ho", "ol", "la"}
    "hilo" -> {"hi", "il", "lo"}
    Intersección: {} (vacío)
    Unión: {"ho", "ol", "la", "hi", "il", "lo"}
    Similitud: 0 / 6 = 0%

Pseudo-código:
    Jaccard(S1, S2, n):
        Entrada: Dos strings S1 y S2, y el tamaño de n-grama n
        Salida: Índice de similitud de Jaccard (0 a 1)
        
        ngramas1 = extraer_ngramas(S1, n)
        ngramas2 = extraer_ngramas(S2, n)
        
        interseccion = ngramas1 ∩ ngramas2
        union = ngramas1 ∪ ngramas2
        
        Si |union| == 0:
            Regresar 0
        
        similitud = |interseccion| / |union|
        Regresar similitud

Complejidad:
- Tiempo: O(|S1| + |S2|) para extraer n-gramas + O(min(|S1|, |S2|)) para calcular Jaccard
- Espacio: O(|S1| + |S2|) para almacenar los conjuntos de n-gramas
"""


def extraer_ngramas(texto, n):
    """
    Extrae todos los n-gramas de un texto.
    
    Args:
        texto: El texto del cual extraer n-gramas
        n: El tamaño de cada n-grama
    
    Returns:
        Conjunto (set) de n-gramas
    """
    if len(texto) < n:
        return set([texto]) if texto else set()
    
    ngramas = set()
    for i in range(len(texto) - n + 1):
        ngrama = texto[i:i+n]
        ngramas.add(ngrama)
    
    return ngramas


def extraer_ngramas_con_frecuencia(texto, n):
    """
    Extrae n-gramas con su frecuencia de aparición.
    
    Args:
        texto: El texto del cual extraer n-gramas
        n: El tamaño de cada n-grama
    
    Returns:
        Diccionario {ngrama: frecuencia}
    """
    if len(texto) < n:
        return {texto: 1} if texto else {}
    
    ngramas = {}
    for i in range(len(texto) - n + 1):
        ngrama = texto[i:i+n]
        ngramas[ngrama] = ngramas.get(ngrama, 0) + 1
    
    return ngramas


def similitud_jaccard(texto1, texto2, n=3):
    """
    Calcula la similitud de Jaccard entre dos textos usando n-gramas.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        n: Tamaño de los n-gramas (default: 3 para trigramas)
    
    Returns:
        Similitud de Jaccard (0 a 100)
    """
    # Extraer n-gramas de ambos textos
    ngramas1 = extraer_ngramas(texto1, n)
    ngramas2 = extraer_ngramas(texto2, n)
    
    # Calcular intersección y unión
    interseccion = ngramas1 & ngramas2
    union = ngramas1 | ngramas2
    
    # Calcular similitud
    if len(union) == 0:
        return 0.0
    
    similitud = len(interseccion) / len(union) * 100
    
    return similitud


def similitud_jaccard_ponderada(texto1, texto2, n=3):
    """
    Calcula la similitud de Jaccard ponderada por frecuencia.
    En lugar de conjuntos, usa la frecuencia de cada n-grama.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        n: Tamaño de los n-gramas
    
    Returns:
        Similitud de Jaccard ponderada (0 a 100)
    """
    ngramas1 = extraer_ngramas_con_frecuencia(texto1, n)
    ngramas2 = extraer_ngramas_con_frecuencia(texto2, n)
    
    # Calcular intersección mínima (para cada n-grama común, tomar el mínimo de frecuencias)
    todos_ngramas = set(ngramas1.keys()) | set(ngramas2.keys())
    
    suma_minimos = 0
    suma_maximos = 0
    
    for ngrama in todos_ngramas:
        freq1 = ngramas1.get(ngrama, 0)
        freq2 = ngramas2.get(ngrama, 0)
        suma_minimos += min(freq1, freq2)
        suma_maximos += max(freq1, freq2)
    
    if suma_maximos == 0:
        return 0.0
    
    similitud = suma_minimos / suma_maximos * 100
    
    return similitud


def analisis_multingrama(texto1, texto2, tamaños=[2, 3, 4, 5]):
    """
    Analiza la similitud con diferentes tamaños de n-gramas.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        tamaños: Lista de tamaños de n-gramas a probar
    
    Returns:
        Diccionario con resultados para cada tamaño
    """
    resultados = {}
    
    for n in tamaños:
        similitud_simple = similitud_jaccard(texto1, texto2, n)
        similitud_ponderada = similitud_jaccard_ponderada(texto1, texto2, n)
        
        ngramas1 = extraer_ngramas(texto1, n)
        ngramas2 = extraer_ngramas(texto2, n)
        
        resultados[n] = {
            'similitud_simple': similitud_simple,
            'similitud_ponderada': similitud_ponderada,
            'ngramas_texto1': len(ngramas1),
            'ngramas_texto2': len(ngramas2),
            'ngramas_comunes': len(ngramas1 & ngramas2)
        }
    
    return resultados


def jaccard_con_bloques(texto1, texto2, n=3, tamaño_bloque=50000):
    """
    Aplica Jaccard a bloques de texto para manejar textos muy grandes.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        n: Tamaño de los n-gramas
        tamaño_bloque: Tamaño de cada bloque
    
    Returns:
        Diccionario con resultados de similitud
    """
    # Para textos pequeños, calcular directamente
    if len(texto1) <= tamaño_bloque and len(texto2) <= tamaño_bloque:
        similitud = similitud_jaccard(texto1, texto2, n)
        similitud_ponderada = similitud_jaccard_ponderada(texto1, texto2, n)
        return {
            'similitud': similitud,
            'similitud_ponderada': similitud_ponderada,
            'tamaño_ngrama': n,
            'metodo': 'directo'
        }
    
    # Para textos grandes, dividir en bloques
    bloques1 = [texto1[i:i+tamaño_bloque] for i in range(0, len(texto1), tamaño_bloque)]
    bloques2 = [texto2[i:i+tamaño_bloque] for i in range(0, len(texto2), tamaño_bloque)]
    
    # Limitar comparaciones (Jaccard es más rápido, puede manejar más)
    max_comparaciones = 100
    total_comparaciones = len(bloques1) * len(bloques2)
    
    if total_comparaciones > max_comparaciones:
        step1 = max(1, len(bloques1) // 10)
        step2 = max(1, len(bloques2) // 10)
        bloques1_muestra = bloques1[::step1]
        bloques2_muestra = bloques2[::step2]
    else:
        bloques1_muestra = bloques1
        bloques2_muestra = bloques2
    
    similitudes = []
    similitudes_ponderadas = []
    mejor_similitud = 0
    mejor_similitud_ponderada = 0
    mejor_par = (0, 0)
    
    total = len(bloques1_muestra) * len(bloques2_muestra)
    actual = 0
    
    for i, bloque1 in enumerate(bloques1_muestra):
        for j, bloque2 in enumerate(bloques2_muestra):
            actual += 1
            print(f"   Jaccard {n}-grama: {actual}/{total} ({actual*100//total}%)...", end='\r')
            
            sim = similitud_jaccard(bloque1, bloque2, n)
            sim_pond = similitud_jaccard_ponderada(bloque1, bloque2, n)
            
            similitudes.append(sim)
            similitudes_ponderadas.append(sim_pond)
            
            if sim > mejor_similitud:
                mejor_similitud = sim
                mejor_similitud_ponderada = sim_pond
                mejor_par = (i, j)
    
    print()  # Nueva línea
    
    return {
        'similitud': mejor_similitud,
        'similitud_ponderada': mejor_similitud_ponderada,
        'similitud_promedio': sum(similitudes) / len(similitudes),
        'similitud_ponderada_promedio': sum(similitudes_ponderadas) / len(similitudes_ponderadas),
        'mejor_par': mejor_par,
        'total_bloques': (len(bloques1_muestra), len(bloques2_muestra)),
        'tamaño_ngrama': n,
        'metodo': 'bloques'
    }


def ngramas_comunes_frecuentes(texto1, texto2, n=3, top_k=10):
    """
    Encuentra los n-gramas comunes más frecuentes entre dos textos.
    
    Args:
        texto1: Primer texto
        texto2: Segundo texto
        n: Tamaño de los n-gramas
        top_k: Número de n-gramas top a retornar
    
    Returns:
        Lista de tuplas (ngrama, frecuencia_texto1, frecuencia_texto2)
    """
    ngramas1 = extraer_ngramas_con_frecuencia(texto1, n)
    ngramas2 = extraer_ngramas_con_frecuencia(texto2, n)
    
    # Encontrar n-gramas comunes
    comunes = set(ngramas1.keys()) & set(ngramas2.keys())
    
    # Ordenar por frecuencia total
    comunes_ordenados = sorted(
        comunes,
        key=lambda ng: ngramas1[ng] + ngramas2[ng],
        reverse=True
    )
    
    # Retornar top-k
    resultado = []
    for ngrama in comunes_ordenados[:top_k]:
        resultado.append((ngrama, ngramas1[ngrama], ngramas2[ngrama]))
    
    return resultado
