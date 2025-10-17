"""
    Algoritmo con programación dinámica para encontrar:
        - Las subcadenas comunes más largas entre dos textos.
    
    Pseudo-código (Subsecuencia común más larga) con O(n * m):
        lcs(S_1, S_2):
            Entrada: Dos strings S_1 y S_2 de tamaños n y m
            Salida: El tamaño de la subsecuencia común más larga entre S_1 y S_2
            
            Sea lcs una matriz de n x m
            
            Si S_1[0] == S_2[0]:
                lcs[0][0] = 1
            De lo contrario:
                lcs[0][0] = 0
                
            Repetir para i = 1 hasta n - 1:
                Si S_1[i] == S_2[0]:
                    lcs[i][0] = 1
                De lo contrario:
                    lcs[i][0] = lcs[i - 1][0]
            Repetir para j = 1 hasta m - 1:
                Si S_1[0] == S_2[j]:
                    lcs[0][j] = 1
                De lo contrario:
                    lcs[0][j] = lcs[0][j - 1]
            Repetir para i = 1 hasta n - 1:
                Repetir para j = 1 hasta m - 1:
                    Si S_1[i] == S_2[j]:
                        lcs[i][j] = lcs[i - 1][j - 1] + 1
                    De lo contrario:
                        lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
            Regresa lcs[n - 1][m - 1]
"""

def lcs(S1, S2):
    n, m = len(S1), len(S2)
    
    # Crear la matriz lcs de tamaño n x m
    lcs = [[0] * m for _ in range(n)]
    
    # Inicializar la primera celda
    if S1[0] == S2[0]:
        lcs[0][0] = 1
    else:
        lcs[0][0] = 0
        
    # Inicializar la primera columna
    for i in range(1, n):
        if S1[i] == S2[0]:
            lcs[i][0] = 1
        else:
            lcs[i][0] = lcs[i - 1][0]
    # Inicializar la primera fila
    for j in range(1, m):
        if S1[0] == S2[j]:
            lcs[0][j] = 1
        else:
            lcs[0][j] = lcs[0][j - 1]
    # Llenar la matriz lcs
    for i in range(1, n):
        for j in range(1, m):
            if S1[i] == S2[j]:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
            else:
                lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
    
    # Reconstruir la subsecuencia
    i, j = n - 1, m - 1
    resultado = []
    while i >= 0 and j >= 0:
        if S1[i] == S2[j]:
            resultado.append(S1[i])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or lcs[i - 1][j] >= lcs[i][j - 1]):
            i -= 1
        else:
            j -= 1
    
    lcs_string = ''.join(reversed(resultado))
    longitud_lcs = lcs[n - 1][m - 1]
    return longitud_lcs, lcs_string