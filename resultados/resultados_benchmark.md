# Reporte de Benchmark y Respuestas: LLMOps Lab 1

Este documento detalla las respuestas completas obtenidas por cada modelo cuantizado frente a los prompts de prueba, acompañadas de sus métricas de rendimiento.

---

## Prueba 1: qwen2.5:1.5b-instruct-q4_K_M

- **Categoría de Prompt:** Corto (Definición)
- **Métricas:** `TTFT: 254.79 ms` | `Velocidad: 30.54 TPS` | `Tokens: 552` | `Tiempo Total: 18.09 s`

### Prompt Enviado:
> Explica en exactamente 3 viñetas qué es la cuantización en modelos de lenguaje.

### Respuesta Generada:
~~~~text
La cuantización en modelos de lenguaje es un proceso fundamental en la representación de la información en redes neuronales y otros algoritmos de aprendizaje automático. Aquí te explico en tres viñetas lo que es la cuantización:

1. **Interpretación de la Representación Cuantizada**:
   - **Definición**: La cuantización implica la transformación de una representación de datos en un conjunto de números enteros, o cuantizados, para su procesamiento y análisis.
   - **Aplicación**: En modelos de lenguaje, la cuantización se utiliza para reducir la dimensionalidad de los datos, lo que permite la implementación de algoritmos más eficientes y la reducción de la memoria necesaria.
   - **Ejemplo**: En un modelo de texto, los caracteres de texto se pueden cuantizar a una cantidad limitada de valores, como 0, 1, 2, etc., lo que permite la representación de la información en un espacio más pequeño.

2. **Reducción de Dimensiones**:
   - **Concepto**: La cuantización es una técnica de reducción de la dimensionalidad de los datos, donde se eliminan las variables más altas en la representación de datos.
   - **Beneficios**: Reduce la complejidad del modelo y mejora la velocidad de entrenamiento y la capacidad de generalización.
   - **Aplicación**: En modelos de lenguaje, la cuantización puede ser utilizada para reducir la cantidad de características que se deben considerar, lo que es especialmente útil en problemas de clasificación o regresión.

3. **Aplicación en Modelos de Lenguaje**:
   - **Concepto**: En modelos de lenguaje, la cuantización se utiliza para representar la información de manera más eficiente y reducir la cantidad de datos necesarios para la inferencia.
   - **Ejemplo**: En un modelo de texto, la cuantización de los caracteres puede reducir la cantidad de información necesaria para representar un texto, lo que puede mejorar significativamente la velocidad de procesamiento.
   - **Beneficios**: Mejora la eficiencia del modelo, lo que puede llevar a una mejora en la precisión del modelo y a una reducción de los recursos necesarios para su entrenamiento.

En resumen, la cuantización en modelos de lenguaje es una técnica fundamental que permite la representación de la información de manera más eficiente, reduciendo la dimensionalidad del problema y mejorando la eficiencia del modelo.
~~~~

---

## Prueba 2: qwen2.5:1.5b-instruct-q4_K_M

- **Categoría de Prompt:** Medio (Razonamiento)
- **Métricas:** `TTFT: 842.65 ms` | `Velocidad: 28.92 TPS` | `Tokens: 556` | `Tiempo Total: 19.81 s`

### Prompt Enviado:
> Tengo un servidor con 16 GB de RAM y sin GPU. Quiero desplegar un asistente interno para 5 empleados. ¿Qué arquitectura y tamaño de modelo me recomiendas y por qué?

### Respuesta Generada:
~~~~text
Para un asistente interno para 5 empleados, considerando un servidor con 16 GB de RAM y sin GPU, aquí te recomendaría una arquitectura y tamaño de modelo:

1. **Modelo de Conversación de Chatbot (Chatbot)**:
   - **Tamaño de Modelo**: 150M (Micro)
   - **Arquitectura**: Transformer (Hugging Face)

   **Razonamiento**:
   - Este tamaño es adecuado para una conversación interactiva y permite una respuesta rápida y precisa.
   - La arquitectura Transformer es eficiente y puede manejar grandes cantidades de texto.

2. **Tecnología de Entrenamiento y Despliegue**:
   - **Entrenamiento**: Utiliza una plataforma como Hugging Face o Anthropic para entrenar el modelo.
   - **Despliegue**: Puedes usar una plataforma como Anthropic o Hugging Face para desplegar el modelo en la nube.
   - **Reducción de Redes**: Considera la posibilidad de usar una red de chatbot pre-entrenada para reducir el tamaño del modelo y mejorar la velocidad de respuesta.

3. **Configuración del Servidor**:
   - **RAM**: 16 GB es suficiente para manejar el modelo de chatbot.
   - **CPU**: 2-4 núcleos de CPU de alta gama (por ejemplo, Intel Core i7 o AMD Ryzen 7).
   - **Storage**: 1-2 TB de almacenamiento SSD para almacenar el modelo y los datos de entrenamiento.

4. **Implementación**:
   - **Backend**: Implementa el modelo en una aplicación backend en la nube.
   - **Frontend**: Puedes usar una interfaz web simple para la interacción con el usuario.
   - **API**: Configura una API REST para permitir la comunicación entre el backend y el frontend.

5. **Pruebas y Optimización**:
   - Realiza pruebas de rendimiento para asegurarte de que el modelo responde en tiempo real.
   - Optima la configuración del servidor para maximizar la eficiencia.

6. **Seguridad y Privacidad**:
   - Implementa medidas de seguridad y privacidad para proteger la información de los empleados y la base de datos del modelo.

Recuerda que este modelo es para una conversación interactiva y no para tareas de procesamiento de imágenes o grandes cantidades de texto. Además, considera la necesidad de mantener actualizado el modelo para mejorar la precisión y la eficiencia.
~~~~

---

## Prueba 3: qwen2.5:1.5b-instruct-q4_K_M

- **Categoría de Prompt:** Largo (Generación de Código)
- **Métricas:** `TTFT: 401.82 ms` | `Velocidad: 29.91 TPS` | `Tokens: 664` | `Tiempo Total: 22.27 s`

### Prompt Enviado:
> Escribe una función en Python bien documentada que implemente búsqueda binaria sobre una lista ordenada, incluyendo manejo de excepciones y 3 casos de prueba.

### Respuesta Generada:
~~~~text
Aquí tienes una función bien documentada en Python que implementa la búsqueda binaria sobre una lista ordenada. La función incluye manejo de excepciones y 3 casos de prueba:

```python
def binary_search(arr, target):
    """
    Realiza una búsqueda binaria en una lista ordenada.

    Parámetros:
    arr (list): Lista ordenada de números.
    target: Número a buscar.

    Retorna:
    int: Indice del elemento si se encuentra en la lista, -1 si no se encuentra.

    Excepciones:
    ValueError: Si la lista no está ordenada.
    TypeError: Si el target no es un número.

    Casos de prueba:
    >>> binary_search([1, 2, 3, 4, 5], 3)
    2
    >>> binary_search([1, 2, 3, 4, 5], 6)
    -1
    >>> binary_search([1, 2, 3, 4, 5], 'a')
    TypeError: 'target' debe ser un número.
    >>> binary_search([1, 2, 3, 4, 5], 3)
    2
    >>> binary_search([1, 2, 3, 4, 5], 3)
    2
    """
    if not arr:
        raise ValueError("La lista no puede estar vacía.")

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Casos de prueba
print(binary_search([1, 2, 3, 4, 5], 3))  # 2
print(binary_search([1, 2, 3, 4, 5], 6))  # -1
print(binary_search([1, 2, 3, 4, 5], 'a'))  # TypeError: 'target' debe ser un número.
print(binary_search([1, 2, 3, 4, 5], 3))  # 2
print(binary_search([1, 2, 3, 4, 5], 3))  # 2
```

Esta función `binary_search` se encarga de buscar un elemento `target` en una lista `arr` ordenada. La búsqueda se realiza de manera binaria, es decir, se divide la lista en dos mitades y se busca en cada mitad hasta encontrar el elemento o determinar que no está presente. La función incluye un manejo de excepciones para casos específicos:

1. Si la lista está vacía, se lanza una `ValueError`.
2. Si el `target` no es un número, se lanza una `TypeError`.

El código incluye 3 casos de prueba para asegurarse de que la función funcione correctamente en diferentes situaciones.
~~~~

---

## Prueba 4: qwen2.5:1.5b-instruct-q8_0

- **Categoría de Prompt:** Corto (Definición)
- **Métricas:** `TTFT: 258.25 ms` | `Velocidad: 19.92 TPS` | `Tokens: 280` | `Tiempo Total: 14.1 s`

### Prompt Enviado:
> Explica en exactamente 3 viñetas qué es la cuantización en modelos de lenguaje.

### Respuesta Generada:
~~~~text
1. **Definición y Concepto**: La cuantización en modelos de lenguaje es un proceso que reduce la cantidad de información original en un texto o frase a una cantidad más pequeña y más simple. Esto se logra al eliminar o simplificar los elementos no esenciales del texto, manteniendo solo lo que es realmente relevante para el propósito del modelo.

2. **Aplicaciones y Beneficios**: Esta técnica se utiliza ampliamente en la generación de texto, especialmente en aplicaciones como chatbots, asistentes virtuales y sistemas de traducción automática. Al cuantizar el texto, se pueden procesar y generar respuestas más rápidas y eficientes, ya que se eliminan los elementos innecesarios que podrían llevar tiempo de procesamiento.

3. **Impacto en la Precisión y Eficiencia**: La cuantización puede mejorar la precisión del modelo al eliminar elementos que no contribuyen significativamente a la comprensión del texto. Sin embargo, también puede tener un impacto negativo en la precisión, ya que puede eliminar información relevante que podría ser útil para entender el contexto o la intención del texto original. Es importante encontrar un equilibrio entre cuantizar y mantener la información relevante para maximizar la eficiencia y precisión del modelo.
~~~~

---

## Prueba 5: qwen2.5:1.5b-instruct-q8_0

- **Categoría de Prompt:** Medio (Razonamiento)
- **Métricas:** `TTFT: 407.28 ms` | `Velocidad: 19.58 TPS` | `Tokens: 424` | `Tiempo Total: 21.74 s`

### Prompt Enviado:
> Tengo un servidor con 16 GB de RAM y sin GPU. Quiero desplegar un asistente interno para 5 empleados. ¿Qué arquitectura y tamaño de modelo me recomiendas y por qué?

### Respuesta Generada:
~~~~text
Para un asistente interno para 5 empleados con un servidor de 16 GB de RAM y sin GPU, aquí te recomendaría una arquitectura y tamaño de modelo:

1. Arquitectura: Un modelo de asistente interno puede ser una combinación de un modelo de conversación basado en texto y un modelo de reconocimiento de voz.

2. Tamaño de modelo: Para un asistente interno, un modelo de 124M a 350M de parámetros sería adecuado. Esto proporcionará una buena capacidad de aprendizaje y conversación, pero no requiere una gran cantidad de recursos.

3. Razonamiento: Para un asistente interno, es importante que el modelo sea capaz de razonar y entender el contexto de la conversación. Por lo tanto, un modelo de razonamiento basado en lenguaje natural (LLM) sería ideal.

4. Entrenamiento: Para un modelo de 124M a 350M de parámetros, necesitarás al menos 16 GB de RAM para entrenarlo. Esto se debe a que el modelo necesita almacenar y procesar grandes cantidades de datos durante el entrenamiento.

5. Despliegue: Para un asistente interno, es importante que el modelo sea fácil de desplegar y mantener. Por lo tanto, un modelo de 124M a 350M de parámetros sería una buena opción.

6. Actualización: Para un asistente interno, es importante que el modelo sea fácil de actualizar. Por lo tanto, un modelo de 124M a 350M de parámetros sería una buena opción.

En resumen, un modelo de 124M a 350M de parámetros sería una buena opción para un asistente interno para 5 empleados con un servidor de 16 GB de RAM y sin GPU.
~~~~

---

## Prueba 6: qwen2.5:1.5b-instruct-q8_0

- **Categoría de Prompt:** Largo (Generación de Código)
- **Métricas:** `TTFT: 471.93 ms` | `Velocidad: 19.33 TPS` | `Tokens: 678` | `Tiempo Total: 34.98 s`

### Prompt Enviado:
> Escribe una función en Python bien documentada que implemente búsqueda binaria sobre una lista ordenada, incluyendo manejo de excepciones y 3 casos de prueba.

### Respuesta Generada:
~~~~text
Aquí tienes una función en Python que implementa la búsqueda binaria sobre una lista ordenada. La función está bien documentada y incluye manejo de excepciones y 3 casos de prueba.

```python
def binary_search(arr, target):
    """
    Realiza una búsqueda binaria en una lista ordenada.

    Parámetros:
    arr (list): Lista ordenada en la que se realizará la búsqueda.
    target (int): El valor objetivo que se busca en la lista.

    Retorna:
    int: El índice del elemento objetivo en la lista, o -1 si no se encuentra.

    Excepciones:
    ValueError: Si la lista no está ordenada.

    Casos de prueba:
    >>> binary_search([1, 2, 3, 4, 5], 3)
    2
    >>> binary_search([1, 2, 3, 4, 5], 6)
    -1
    >>> binary_search([], 1)
    -1
    >>> binary_search([1], 1)
    0
    """
    if not arr:
        raise ValueError("La lista no puede estar vacía.")

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = arr[mid]

        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Casos de prueba
if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

### Explicación de la función:

1. **Parámetros**:
   - `arr`: Es la lista ordenada en la que se realizará la búsqueda.
   - `target`: Es el valor objetivo que se busca en la lista.

2. **Retorno**:
   - El índice del elemento objetivo en la lista, o -1 si no se encuentra.

3. **Excepciones**:
   - `ValueError`: Si la lista no está ordenada.

4. **Casos de prueba**:
   - Se utilizan `doctest` para probar la función con diferentes casos de prueba.

5. **Función `doctest.testmod()`**:
   - Este método ejecuta todas las pruebas de doctest en la función y muestra los resultados.

### Ejemplos de uso:

- `binary_search([1, 2, 3, 4, 5], 3)` devuelve `2` porque el elemento `3` está en el índice `2`.
- `binary_search([1, 2, 3, 4, 5], 6)` devuelve `-1` porque el elemento `6` no está en la lista.
- `binary_search([], 1)` devuelve `-1` porque la lista está vacía.
- `binary_search([1], 1)` devuelve `0` porque el elemento `1` está en el índice `0`.

Este código proporciona una implementación clara y documentada de la búsqueda binaria, incluyendo manejo de excepciones y casos de prueba.
~~~~

---

