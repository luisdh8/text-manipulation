# Etapa 5 - Investigación de Alternativas Algorítmicas

## 📋 Descripción

Este módulo implementa tres nuevos algoritmos para análisis de similitud de textos, como parte de la Etapa 5 del proyecto de Análisis de Textos.

## 🔬 Algoritmos Implementados

### 1. **Algoritmo de Hirschberg** (`hirschberg.py`)

**Descripción:** Versión optimizada del algoritmo LCS (Longest Common Subsequence) que reduce el uso de memoria.

**Justificación:** Mientras que el LCS tradicional requiere O(n×m) de memoria, Hirschberg logra el mismo resultado con solo O(min(n,m)) de memoria usando la técnica de "divide y vencerás". Esto permite procesar textos mucho más grandes sin quedarse sin memoria.

**Ventajas:**
- ✅ Complejidad de espacio: O(min(n,m)) vs O(n×m) del LCS tradicional
- ✅ Misma precisión que el LCS tradicional
- ✅ Permite procesar textos grandes sin problemas de memoria
- ✅ Reconstruye la subsecuencia completa

**Desventajas:**
- ⚠️ Complejidad de tiempo sigue siendo O(n×m)
- ⚠️ Más complejo de implementar que el LCS tradicional

**Casos de uso ideales:**
- Textos muy grandes donde la memoria es limitada
- Cuando se necesita la subsecuencia común exacta
- Análisis científico que requiere máxima precisión

---

### 2. **Distancia de Levenshtein** (`levenshtein.py`)

**Descripción:** Mide el número mínimo de operaciones de edición (inserciones, eliminaciones, sustituciones) necesarias para transformar un texto en otro.

**Justificación:** A diferencia del LCS que solo cuenta coincidencias, Levenshtein considera también las diferencias. Esto lo hace ideal para detectar textos que son casi idénticos pero con pequeñas variaciones, errores tipográficos, o modificaciones menores.

**Ventajas:**
- ✅ Detecta diferencias sutiles entre textos
- ✅ Considera sustituciones además de inserciones/eliminaciones
- ✅ Ampliamente usado en corrección ortográfica
- ✅ Versión optimizada en espacio O(min(n,m))
- ✅ Fácil de interpretar (distancia = número de cambios)

**Desventajas:**
- ⚠️ Complejidad de tiempo O(n×m)
- ⚠️ No identifica subsecuencias específicas
- ⚠️ Puede ser lento con textos muy grandes

**Casos de uso ideales:**
- Detección de versiones modificadas de un texto
- Corrección ortográfica y autocompletado
- Verificación de duplicados casi exactos
- Análisis de plagio con modificaciones menores

---

### 3. **Similitud de Jaccard con N-gramas** (`jaccard_ngram.py`)

**Descripción:** Divide los textos en fragmentos de n caracteres consecutivos (n-gramas) y mide qué proporción de estos fragmentos se comparten entre ambos textos.

**Justificación:** Es extremadamente eficiente computacionalmente (O(n+m)) comparado con los otros métodos (O(n×m)). Además, no requiere que los fragmentos estén en el mismo orden, lo que lo hace robusto ante reordenamientos de texto. Es el método preferido en detección de plagio industrial.

**Ventajas:**
- ✅ Muy eficiente: O(n+m) vs O(n×m) de otros métodos
- ✅ Robusto ante reordenamientos de texto
- ✅ No requiere que los textos estén alineados
- ✅ Ajustable con diferentes tamaños de n-gramas
- ✅ Ampliamente usado en la industria
- ✅ Funciona bien con textos grandes

**Desventajas:**
- ⚠️ No encuentra subsecuencias específicas
- ⚠️ Sensible al tamaño de n-grama elegido
- ⚠️ No mantiene información de orden exacto

**Casos de uso ideales:**
- Detección rápida de plagio
- Comparación de muchos documentos
- Búsqueda de duplicados en grandes bases de datos
- Cuando el orden exacto no es crítico
- Análisis preliminar antes de métodos más costosos

**Tipos de n-gramas:**
- **Bigramas (n=2):** Muy sensible a cambios pequeños
- **Trigramas (n=3):** Balance ideal (valor por defecto)
- **4-gramas o más:** Más específico, menos tolerante a variaciones

---

## 📁 Estructura de Archivos

```
etapa5_algoritmos/
├── __init__.py                 # Módulo de inicialización
├── hirschberg.py              # Implementación de Hirschberg
├── levenshtein.py             # Implementación de Levenshtein
├── jaccard_ngram.py           # Implementación de Jaccard con n-gramas
├── main.py                    # Script principal para ejecutar los 3 algoritmos
├── comparacion_completa.py    # Comparación con etapas anteriores
└── README.md                  # Esta documentación
```

## 🚀 Uso

### Ejecutar solo los algoritmos de Etapa 5:

```powershell
cd etapa5_algoritmos
python main.py
```

### Ejecutar comparación completa (Etapas 3, 4 y 5):

```powershell
cd etapa5_algoritmos
python comparacion_completa.py
```

### Usar algoritmos individualmente:

```python
from etapa5_algoritmos.hirschberg import hirschberg
from etapa5_algoritmos.levenshtein import similitud_levenshtein
from etapa5_algoritmos.jaccard_ngram import similitud_jaccard

# Hirschberg
longitud, subsecuencia = hirschberg(texto1, texto2)

# Levenshtein
similitud = similitud_levenshtein(texto1, texto2)

# Jaccard
similitud = similitud_jaccard(texto1, texto2, n=3)
```

## 📊 Complejidad Comparativa

| Algoritmo | Tiempo | Espacio | Precisión | Velocidad |
|-----------|--------|---------|-----------|-----------|
| Hirschberg | O(n×m) | O(min(n,m)) | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Levenshtein | O(n×m) | O(min(n,m)) | ⭐⭐⭐⭐ | ⭐⭐ |
| Jaccard n-grama | O(n+m) | O(n+m) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 📈 Resultados Esperados

El script `main.py` genera:

1. **Análisis de Hirschberg:**
   - Longitud de la subsecuencia común más larga
   - Porcentaje de similitud
   - Fragmento encontrado
   - Tiempo de ejecución

2. **Análisis de Levenshtein:**
   - Distancia de edición (número de cambios necesarios)
   - Porcentaje de similitud
   - Tiempo de ejecución

3. **Análisis de Jaccard:**
   - Similitud con diferentes tamaños de n-gramas (2, 3, 4, 5)
   - Similitud ponderada por frecuencia
   - Top 10 n-gramas comunes más frecuentes
   - Tiempo de ejecución

4. **Comparación de Resultados:**
   - Tabla comparativa de similitudes
   - Algoritmo más rápido
   - Mayor similitud detectada
   - Análisis e interpretación

## 🎯 Recomendaciones de Uso

### Elige Hirschberg si:
- ✓ Necesitas la subsecuencia común exacta
- ✓ Tienes textos grandes y memoria limitada
- ✓ La precisión es más importante que la velocidad
- ✓ Necesitas resultados científicamente rigurosos

### Elige Levenshtein si:
- ✓ Buscas textos casi idénticos con pequeñas variaciones
- ✓ Necesitas saber cuántos cambios hay entre textos
- ✓ Trabajas con corrección ortográfica o autocompletado
- ✓ Los textos son de tamaño moderado

### Elige Jaccard n-grama si:
- ✓ Necesitas velocidad sobre todo
- ✓ Vas a comparar muchos documentos
- ✓ El orden exacto no es crítico
- ✓ Buscas detectar plagio o duplicados
- ✓ Quieres un análisis preliminar rápido

## 📝 Notas Técnicas

### Optimizaciones Implementadas:

1. **División en bloques:** Para textos muy grandes, se dividen en bloques más manejables
2. **Muestreo estratégico:** Si hay demasiados bloques, se muestrea para reducir comparaciones
3. **Versiones optimizadas en espacio:** Hirschberg y Levenshtein usan solo dos filas de memoria
4. **Progreso en tiempo real:** Todos los algoritmos muestran progreso durante la ejecución

### Limitaciones:

- Para textos de más de 100,000 caracteres, se recomienda usar división en bloques
- La comparación completa puede tomar varios minutos con textos muy grandes
- Los resultados de bloques son aproximados, no exactos

## 🔄 Integración con Etapas Anteriores

El script `comparacion_completa.py` integra:
- **Etapa 3:** Substring común más largo (LCSstr)
- **Etapa 4:** Subsecuencia común más larga (LCS)
- **Etapa 5:** Hirschberg, Levenshtein, y Jaccard

Esto permite una comparación directa de todos los métodos implementados en el proyecto.

## 📚 Referencias

- **Hirschberg's Algorithm:** Hirschberg, D. S. (1975). "A linear space algorithm for computing maximal common subsequences"
- **Levenshtein Distance:** Levenshtein, V. I. (1966). "Binary codes capable of correcting deletions, insertions, and reversals"
- **Jaccard Similarity:** Jaccard, P. (1912). "The distribution of the flora in the alpine zone"

## 👨‍💻 Autor

Luis - Instituto Tecnológico y de Estudios Superiores de Monterrey
Algoritmos - 5to Semestre
Noviembre 2025
