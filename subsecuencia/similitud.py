try:
    from subsecuencia.lcs import lcs
except ModuleNotFoundError:
    from lcs import lcs


def calcSimilitud(S1, S2):

    if len(S1) == 0 and len(S2) == 0:
        return 100.0
    
    if len(S1) == 0 or len(S2) == 0:
        return 0.0
    
    longitud_lcs, _ = lcs(S1, S2)  # lcs ahora retorna tupla (longitud, fragmento)
    
    # Fórmula de similitud basada en LCS
    similitud = (2 * longitud_lcs) / (len(S1) + len(S2)) * 100
    
    return similitud

def reporteSimilitud(S1, S2):
    """
    Genera un reporte completo de similitud con diferentes métricas.
    
    Args:
        S1: Primer string
        S2: Segundo string
    
    Returns:
        dict: Diccionario con múltiples métricas de similitud
    """
    longitud_lcs, _ = lcs(S1, S2)  # lcs ahora retorna tupla (longitud, fragmento)
    
    return {
        'longitud_lcs': longitud_lcs,
        'longitud_s1': len(S1),
        'longitud_s2': len(S2),
        'similitud_promedio': calcSimilitud(S1, S2),
        'cobertura_s1': (longitud_lcs / len(S1) * 100) if len(S1) > 0 else 0,
        'cobertura_s2': (longitud_lcs / len(S2) * 100) if len(S2) > 0 else 0
    }
