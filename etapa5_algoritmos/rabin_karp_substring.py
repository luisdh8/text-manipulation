"""
Algoritmo de Rabin-Karp con Ventana Deslizante
Para encontrar el substring común más largo entre dos textos

Justificación:
El algoritmo de Rabin-Karp utiliza hashing (rolling hash) para comparar
substrings de forma eficiente. En lugar de comparar carácter por carácter,
calcula un hash de cada substring y solo compara los strings cuando los
hashes coinciden. Esto reduce significativamente el tiempo de comparación.

Ventajas sobre LCS tradicional:
1. Más eficiente en promedio: O(n+m) vs O(n*m) del algoritmo clásico
2. Usa ventana deslizante con rolling hash (actualización en O(1))
3. Mejor para textos muy grandes
4. Detecta múltiples coincidencias de forma natural
5. Menos uso de memoria (no requiere matriz n×m)

Desventajas:
- Posibles colisiones de hash (falsos positivos)
- Requiere implementar función de hash adecuada
- Menos preciso que el método de programación dinámica en casos de colisión

Pseudo-código:

    RabinKarp_LongestSubstring(S1, S2):
        Entrada: Dos strings S1 y S2
        Salida: Longitud del substring común más largo
        
        max_len = 0
        mejor_substring = ""
        
        // Búsqueda binaria en la longitud
        Para longitud de min(|S1|, |S2|) hasta 1:
            hashes_S1 = calcular_hashes(S1, longitud)
            hashes_S2 = calcular_hashes(S2, longitud)
            
            // Buscar coincidencias
            Para cada hash en hashes_S1:
                Si hash está en hashes_S2:
                    // Verificar que no es colisión
                    Si los substrings realmente coinciden:
                        max_len = longitud
                        mejor_substring = substring
                        Salir
            
            Si se encontró coincidencia:
                Salir
        
        Regresar max_len, mejor_substring
    
    calcular_hashes(texto, longitud):
        Usar rolling hash para eficiencia O(n)

Complejidad:
- Tiempo: O(n+m) en promedio, O(n*m) en peor caso (muchas colisiones)
- Espacio: O(n+m) para almacenar los hashes
"""

import time
from pathlib import Path


def leer_archivo(nombre_archivo):
    """Lee un archivo de texto desde books/procesados"""
    ruta_base = Path(__file__).parent.parent
    ruta_archivo = ruta_base / 'books' / 'procesados' / nombre_archivo
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            print(f"Archivo leído: {nombre_archivo} ({len(contenido):,} caracteres)")
            return contenido
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_archivo}")
        return None
    except Exception as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        return None


class RollingHash:
    """
    Implementación de Rolling Hash (Rabin fingerprint)
    Permite calcular hashes de substrings en tiempo constante O(1)
    """
    
    def __init__(self, base=256, mod=10**9 + 7):
        """
        Args:
            base: Base para el hash (usualmente 256 para ASCII)
            mod: Módulo para evitar overflow (número primo grande)
        """
        self.base = base
        self.mod = mod
    
    def hash_string(self, s):
        """Calcula el hash de un string completo"""
        hash_value = 0
        for char in s:
            hash_value = (hash_value * self.base + ord(char)) % self.mod
        return hash_value
    
    def rolling_hash(self, texto, longitud):
        """
        Calcula todos los hashes de substrings de tamaño 'longitud'
        usando rolling hash para eficiencia O(n)
        
        Args:
            texto: String del cual extraer substrings
            longitud: Tamaño de cada substring
        
        Returns:
            Dict con {hash: [(posición, substring)]}
        """
        if len(texto) < longitud:
            return {}
        
        hashes = {}
        
        # Calcular hash inicial (primera ventana)
        hash_value = 0
        for i in range(longitud):
            hash_value = (hash_value * self.base + ord(texto[i])) % self.mod
        
        # Guardar primer hash
        substring = texto[0:longitud]
        if hash_value not in hashes:
            hashes[hash_value] = []
        hashes[hash_value].append((0, substring))
        
        # Precalcular base^(longitud-1) % mod para rolling hash
        base_pow = pow(self.base, longitud - 1, self.mod)
        
        # Deslizar la ventana y calcular hashes siguientes
        for i in range(1, len(texto) - longitud + 1):
            # Remover carácter anterior y agregar nuevo carácter
            hash_value = (hash_value - ord(texto[i-1]) * base_pow) % self.mod
            hash_value = (hash_value * self.base + ord(texto[i + longitud - 1])) % self.mod
            
            # Asegurar que el hash sea positivo
            hash_value = (hash_value + self.mod) % self.mod
            
            substring = texto[i:i + longitud]
            if hash_value not in hashes:
                hashes[hash_value] = []
            hashes[hash_value].append((i, substring))
        
        return hashes


def rabin_karp_longest_substring(S1, S2):
    """
    Encuentra el substring común más largo usando Rabin-Karp
    
    Args:
        S1: Primer string
        S2: Segundo string
    
    Returns:
        Tupla (longitud, substring)
    """
    if not S1 or not S2:
        return 0, ""
    
    n, m = len(S1), len(S2)
    max_posible = min(n, m)
    
    # Usar búsqueda binaria para encontrar la longitud máxima
    izquierda, derecha = 1, max_posible
    mejor_longitud = 0
    mejor_substring = ""
    
    hasher = RollingHash()
    
    while izquierda <= derecha:
        longitud = (izquierda + derecha) // 2
        
        # Calcular hashes para esta longitud
        hashes_S1 = hasher.rolling_hash(S1, longitud)
        hashes_S2 = hasher.rolling_hash(S2, longitud)
        
        # Buscar coincidencias
        encontrado = False
        for hash_value, substrings_S1 in hashes_S1.items():
            if hash_value in hashes_S2:
                # Verificar que no sea colisión comparando los strings reales
                for pos1, substr1 in substrings_S1:
                    for pos2, substr2 in hashes_S2[hash_value]:
                        if substr1 == substr2:
                            encontrado = True
                            mejor_longitud = longitud
                            mejor_substring = substr1
                            break
                    if encontrado:
                        break
            if encontrado:
                break
        
        if encontrado:
            # Intentar con longitud mayor
            izquierda = longitud + 1
        else:
            # Intentar con longitud menor
            derecha = longitud - 1
    
    return mejor_longitud, mejor_substring


def rabin_karp_simple(S1, S2, max_longitud=None):
    """
    Versión más simple sin búsqueda binaria - busca de mayor a menor
    Más fácil de entender pero potencialmente más lento
    
    Args:
        S1: Primer string
        S2: Segundo string
        max_longitud: Longitud máxima a buscar (None = min(len(S1), len(S2)))
    
    Returns:
        Tupla (longitud, substring)
    """
    if not S1 or not S2:
        return 0, ""
    
    if max_longitud is None:
        max_longitud = min(len(S1), len(S2))
    
    hasher = RollingHash()
    
    # Buscar desde la longitud mayor a la menor
    for longitud in range(max_longitud, 0, -1):
        hashes_S1 = hasher.rolling_hash(S1, longitud)
        hashes_S2 = hasher.rolling_hash(S2, longitud)
        
        # Buscar coincidencias de hash
        for hash_value, substrings_S1 in hashes_S1.items():
            if hash_value in hashes_S2:
                # Verificar coincidencias reales (no solo de hash)
                for pos1, substr1 in substrings_S1:
                    for pos2, substr2 in hashes_S2[hash_value]:
                        if substr1 == substr2:
                            return longitud, substr1
    
    return 0, ""


def analizar_textos_rabin_karp(texto1, texto2, nombre1, nombre2, usar_binaria=True):
    """
    Analiza dos textos usando Rabin-Karp con bloques para textos grandes
    
    Args:
        texto1, texto2: Textos a comparar
        nombre1, nombre2: Nombres de los textos
        usar_binaria: Si True, usa búsqueda binaria (más rápido)
    """
    print(f"\n=== ANÁLISIS CON RABIN-KARP (ROLLING HASH) ===")
    print(f"Texto 1: {nombre1} ({len(texto1):,} caracteres)")
    print(f"Texto 2: {nombre2} ({len(texto2):,} caracteres)")
    print(f"Método: {'Búsqueda binaria' if usar_binaria else 'Búsqueda lineal'}")
    
    TAMAÑO_BLOQUE = 5000
    
    # Si los textos son pequeños, procesar directamente
    if len(texto1) <= TAMAÑO_BLOQUE and len(texto2) <= TAMAÑO_BLOQUE:
        print(f"\nTextos suficientemente pequeños - análisis directo")
        
        tiempo_inicio = time.time()
        
        if usar_binaria:
            longitud, substring = rabin_karp_longest_substring(texto1, texto2)
        else:
            longitud, substring = rabin_karp_simple(texto1, texto2)
        
        tiempo_ejecucion = time.time() - tiempo_inicio
        
        if len(texto1) > 0 and len(texto2) > 0:
            porcentaje_similitud = (2 * longitud) / (len(texto1) + len(texto2)) * 100
        else:
            porcentaje_similitud = 0
        
        metodo = "directo"
        total_bloques = None
        mejor_par = None
    else:
        # Dividir en bloques para textos grandes
        print(f"\nTextos grandes - usando división en bloques de {TAMAÑO_BLOQUE:,} caracteres")
        
        bloques1 = [texto1[i:i+TAMAÑO_BLOQUE] for i in range(0, len(texto1), TAMAÑO_BLOQUE)]
        bloques2 = [texto2[i:i+TAMAÑO_BLOQUE] for i in range(0, len(texto2), TAMAÑO_BLOQUE)]
        
        print(f"Bloques de texto 1: {len(bloques1)}")
        print(f"Bloques de texto 2: {len(bloques2)}")
        
        # Limitar comparaciones
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
        mejor_substring = ""
        mejor_par = (0, 0)
        
        tiempo_inicio = time.time()
        
        total = len(bloques1_muestra) * len(bloques2_muestra)
        actual = 0
        
        for i, bloque1 in enumerate(bloques1_muestra):
            for j, bloque2 in enumerate(bloques2_muestra):
                actual += 1
                print(f"   Rabin-Karp: {actual}/{total} ({actual*100//total}%)...", end='\r')
                
                if usar_binaria:
                    longitud_actual, substring_actual = rabin_karp_longest_substring(bloque1, bloque2)
                else:
                    longitud_actual, substring_actual = rabin_karp_simple(bloque1, bloque2)
                
                if longitud_actual > mejor_longitud:
                    mejor_longitud = longitud_actual
                    mejor_substring = substring_actual
                    mejor_par = (i, j)
        
        print()
        
        tiempo_ejecucion = time.time() - tiempo_inicio
        
        longitud = mejor_longitud
        substring = mejor_substring
        
        if TAMAÑO_BLOQUE > 0:
            porcentaje_similitud = (2 * longitud) / (TAMAÑO_BLOQUE + TAMAÑO_BLOQUE) * 100
        else:
            porcentaje_similitud = 0
        
        total_bloques = (len(bloques1_muestra), len(bloques2_muestra))
        metodo = "bloques"
    
    # Mostrar resultados
    print(f"\nRESULTADOS:")
    print(f"• Algoritmo: Rabin-Karp con rolling hash")
    print(f"• Longitud del substring común más largo: {longitud:,} caracteres")
    print(f"• Porcentaje de similitud: {porcentaje_similitud:.2f}%")
    print(f"• Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
    print(f"• Método usado: {metodo}")
    
    if metodo == "bloques":
        print(f"• Total de bloques comparados: {total_bloques}")
        print(f"• Mejor coincidencia encontrada en: bloque {mejor_par}")
    
    if longitud > 0:
        if len(substring) <= 300:
            print(f"• Fragmento encontrado: \"{substring}\"")
        else:
            print(f"• Fragmento encontrado (primeros/últimos 150 chars):")
            print(f"  \"{substring[:150]}...{substring[-150:]}\"")
    else:
        print("• No se encontró substring común")
    
    return {
        'longitud': longitud,
        'porcentaje': porcentaje_similitud,
        'tiempo': tiempo_ejecucion,
        'fragmento': substring,
        'metodo': metodo,
        'algoritmo': 'Rabin-Karp'
    }


def buscar_archivos_limpios():
    """Busca todos los archivos *_limpio.txt en books/procesados"""
    ruta_base = Path(__file__).parent.parent
    carpeta_procesados = ruta_base / 'books' / 'procesados'
    
    print(f"Buscando en: {carpeta_procesados.absolute()}")
    
    if not carpeta_procesados.exists():
        print(f"Error: No se encontró la carpeta {carpeta_procesados}")
        return []
    
    archivos_limpios = list(carpeta_procesados.glob('*_limpio.txt'))
    nombres_archivos = [archivo.name for archivo in archivos_limpios]
    
    return nombres_archivos


def main():
    """Función principal"""
    
    print("="*70)
    print("ALGORITMO RABIN-KARP CON VENTANA DESLIZANTE")
    print("="*70)
    print("\nJustificación:")
    print("Rabin-Karp usa hashing (rolling hash) para comparar substrings de")
    print("forma más eficiente que el algoritmo clásico O(n²). En lugar de")
    print("comparar cada carácter, calcula un hash de cada ventana y solo")
    print("compara strings cuando los hashes coinciden.")
    print("\nVentajas esperadas:")
    print("• Más rápido en promedio: O(n+m) vs O(n*m)")
    print("• Usa menos memoria (no requiere matriz n×m)")
    print("• Rolling hash permite actualización en O(1)")
    print("• Ideal para textos muy grandes")
    print("="*70)
    
    # Buscar archivos
    archivos = buscar_archivos_limpios()
    
    if not archivos:
        print("Error: No se encontraron archivos de texto limpios")
        return
    
    print("\nArchivos de texto limpios encontrados:")
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo}")
    
    # Leer textos
    textos = {}
    for archivo in archivos:
        contenido = leer_archivo(archivo)
        if contenido:
            textos[archivo] = contenido
    
    if len(textos) < 2:
        print("Error: Se necesitan al menos 2 archivos para la comparación")
        return
    
    print(f"\nSe cargaron {len(textos)} archivos correctamente")
    
    # Analizar cada par de textos
    nombres = list(textos.keys())
    resultados_todos = []
    
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            archivo1, archivo2 = nombres[i], nombres[j]
            resultado = analizar_textos_rabin_karp(
                textos[archivo1], textos[archivo2],
                archivo1, archivo2,
                usar_binaria=True  # Usar búsqueda binaria para mayor velocidad
            )
            resultados_todos.append(resultado)
    
    print("\n" + "="*70)
    print("ANÁLISIS COMPLETADO")
    print("="*70)


if __name__ == "__main__":
    main()
