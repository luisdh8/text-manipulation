try:
    from subsecuencia.lcs import lcs
except ModuleNotFoundError:
    from lcs import lcs


def obtenerFragmentoLcs(S1, S2, max_length=500):
    longitud_lcs, fragmento = lcs(S1, S2)
    
    # Limitar longitud si es muy largo
    if len(fragmento) > max_length:
        fragmento = fragmento[:max_length] + "... [fragmento truncado]"
    
    return longitud_lcs, fragmento


def obtenerFragmentoContexto(S1, S2, max_length=300):
    longitud_lcs, fragmento = lcs(S1, S2)
    
    # Limitar longitud si es muy largo
    if len(fragmento) > max_length:
        fragmento_truncado = fragmento[:max_length] + "... [fragmento truncado]"
    else:
        fragmento_truncado = fragmento
    
    # Buscar dónde aparece el inicio del fragmento en los textos originales
    inicio_s1 = S1.find(fragmento[:min(50, len(fragmento))]) if fragmento else -1
    inicio_s2 = S2.find(fragmento[:min(50, len(fragmento))]) if fragmento else -1
    
    return {
        'fragmento': fragmento_truncado,
        'longitud': longitud_lcs,
        'posicion_s1': inicio_s1,
        'posicion_s2': inicio_s2
    }
