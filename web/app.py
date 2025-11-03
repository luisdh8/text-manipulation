from flask import Flask, render_template, jsonify
from pathlib import Path
import re

app = Flask(__name__)

def leer_resultado(archivo):
    """Lee un archivo de resultados y extrae la información relevante"""
    ruta = Path(__file__).parent.parent / 'resultados' / archivo
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return contenido
    except Exception as e:
        return f"Error al leer {archivo}: {e}"

def extraer_metricas_lcs(texto):
    """Extrae métricas del archivo LCS"""
    metricas = {}
    
    # Longitud del LCS
    match = re.search(r'Longitud del LCS: ([\d,]+) caracteres', texto)
    if match:
        metricas['longitud'] = int(match.group(1).replace(',', ''))
    
    # Porcentaje de similitud
    match = re.search(r'Porcentaje de similitud: ([\d.]+)%', texto)
    if match:
        metricas['similitud'] = float(match.group(1))
    
    # Tiempo de ejecución
    match = re.search(r'Tiempo de ejecución: ([\d.]+) segundos', texto)
    if match:
        metricas['tiempo'] = float(match.group(1))
    
    # Fragmento
    match = re.search(r'Fragmento encontrado.*?:\n-+\n(.*?)\n-+', texto, re.DOTALL)
    if match:
        metricas['fragmento'] = match.group(1).strip()[:200]
    
    return metricas

def extraer_metricas_lcsstr(texto):
    """Extrae métricas del archivo LCSstr"""
    metricas = {}
    
    # Longitud
    match = re.search(r'Longitud del substring común más largo: ([\d,]+) caracteres', texto)
    if match:
        metricas['longitud'] = int(match.group(1).replace(',', ''))
    
    # Porcentaje
    match = re.search(r'Porcentaje de similitud: ([\d.]+)%', texto)
    if match:
        metricas['similitud'] = float(match.group(1))
    
    # Tiempo
    match = re.search(r'Tiempo de ejecución: ([\d.]+) segundos', texto)
    if match:
        metricas['tiempo'] = float(match.group(1))
    
    # Fragmento
    match = re.search(r'Fragmento encontrado.*?:\n\s*"(.*?)"', texto, re.DOTALL)
    if match:
        metricas['fragmento'] = match.group(1).strip()[:200]
    
    return metricas

def extraer_metricas_rk(texto):
    """Extrae métricas del archivo Rabin-Karp"""
    metricas = {}
    
    # Similar a LCSstr
    match = re.search(r'Longitud del substring común más largo: ([\d,]+) caracteres', texto)
    if match:
        metricas['longitud'] = int(match.group(1).replace(',', ''))
    
    match = re.search(r'Porcentaje de similitud: ([\d.]+)%', texto)
    if match:
        metricas['similitud'] = float(match.group(1))
    
    match = re.search(r'Tiempo de ejecución: ([\d.]+) segundos', texto)
    if match:
        metricas['tiempo'] = float(match.group(1))
    
    match = re.search(r'Fragmento encontrado.*?:\n\s*"(.*?)"', texto, re.DOTALL)
    if match:
        metricas['fragmento'] = match.group(1).strip()[:200]
    
    return metricas

def extraer_metricas_finales(texto):
    """Extrae todas las métricas del archivo de resultados finales"""
    resultados = {
        'hirschberg': {},
        'levenshtein': {},
        'jaccard': {},
        'rabin_karp': {},
        'lcs': {},
        'lcsstr': {}
    }
    
    # Hirschberg
    match = re.search(r'HIRSCHBERG.*?Longitud del LCS: ([\d,]+).*?Porcentaje de similitud: ([\d.]+)%.*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['hirschberg'] = {
            'longitud': int(match.group(1).replace(',', '')),
            'similitud': float(match.group(2)),
            'tiempo': float(match.group(3))
        }
    
    # Levenshtein
    match = re.search(r'LEVENSHTEIN.*?Mejor similitud encontrada: ([\d.]+)%.*?Mejor distancia encontrada: ([\d,]+).*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['levenshtein'] = {
            'similitud': float(match.group(1)),
            'distancia': int(match.group(2).replace(',', '')),
            'tiempo': float(match.group(3))
        }
    
    # Jaccard
    match = re.search(r'JACCARD.*?Mejor similitud encontrada: ([\d.]+)%.*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['jaccard'] = {
            'similitud': float(match.group(1)),
            'tiempo': float(match.group(2))
        }
    
    # Rabin-Karp
    match = re.search(r'RABIN-KARP.*?Longitud del substring común: ([\d,]+).*?Porcentaje de similitud: ([\d.]+)%.*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['rabin_karp'] = {
            'longitud': int(match.group(1).replace(',', '')),
            'similitud': float(match.group(2)),
            'tiempo': float(match.group(3))
        }
    
    # LCS Tradicional
    match = re.search(r'LCS TRADICIONAL.*?Longitud del LCS: ([\d,]+).*?Porcentaje de similitud: ([\d.]+)%.*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['lcs'] = {
            'longitud': int(match.group(1).replace(',', '')),
            'similitud': float(match.group(2)),
            'tiempo': float(match.group(3))
        }
    
    # Longest Common Substring
    match = re.search(r'LONGEST COMMON SUBSTRING.*?Longitud del substring común: ([\d,]+).*?Porcentaje de similitud: ([\d.]+)%.*?Tiempo de ejecución: ([\d.]+) segundos', texto, re.DOTALL)
    if match:
        resultados['lcsstr'] = {
            'longitud': int(match.group(1).replace(',', '')),
            'similitud': float(match.group(2)),
            'tiempo': float(match.group(3))
        }
    
    return resultados

@app.route('/')
def index():
    """Página principal"""
    # Leer todos los resultados
    lcs_texto = leer_resultado('lcs.txt')
    lcsstr_texto = leer_resultado('lcsstr.txt')
    rk_texto = leer_resultado('rk.txt')
    finales_texto = leer_resultado('resultados_finales.txt')
    
    # Extraer métricas
    lcs_metricas = extraer_metricas_lcs(lcs_texto)
    lcsstr_metricas = extraer_metricas_lcsstr(lcsstr_texto)
    rk_metricas = extraer_metricas_rk(rk_texto)
    finales_metricas = extraer_metricas_finales(finales_texto)
    
    # Usar datos de resultados_finales para todos los algoritmos
    # Solo usar archivos individuales para fragmentos adicionales
    datos = {
        'lcs': finales_metricas.get('lcs', lcs_metricas),
        'lcsstr': finales_metricas.get('lcsstr', lcsstr_metricas),
        'rabin_karp': finales_metricas.get('rabin_karp', rk_metricas),
        'todos': finales_metricas
    }
    
    # Agregar fragmentos de archivos individuales si existen
    if 'fragmento' in lcs_metricas:
        datos['lcs']['fragmento'] = lcs_metricas['fragmento']
    if 'fragmento' in lcsstr_metricas:
        datos['lcsstr']['fragmento'] = lcsstr_metricas['fragmento']
    if 'fragmento' in rk_metricas:
        datos['rabin_karp']['fragmento'] = rk_metricas['fragmento']
    
    return render_template('index.html', datos=datos)

@app.route('/api/resultados')
def api_resultados():
    """API para obtener resultados en JSON"""
    finales_texto = leer_resultado('resultados_finales.txt')
    metricas = extraer_metricas_finales(finales_texto)
    return jsonify(metricas)

@app.route('/detalle/<algoritmo>')
def detalle(algoritmo):
    """Página de detalle de un algoritmo específico"""
    if algoritmo == 'lcs':
        texto = leer_resultado('lcs.txt')
        metricas = extraer_metricas_lcs(texto)
    elif algoritmo == 'lcsstr':
        texto = leer_resultado('lcsstr.txt')
        metricas = extraer_metricas_lcsstr(texto)
    elif algoritmo == 'rabin-karp':
        texto = leer_resultado('rk.txt')
        metricas = extraer_metricas_rk(texto)
    else:
        return "Algoritmo no encontrado", 404
    
    return render_template('detalle.html', algoritmo=algoritmo, metricas=metricas, texto_completo=texto)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
