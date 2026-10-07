# Trabajo Práctico 1: Pruebas del Software - Uso de un Framework de Testing

**Materia:** Ingeniería de Software 1 (PU) - Ingeniería de Software 2 (LI / II)  
**Fecha:** Septiembre 2026  
**Problema:** *Sistema de Gestión de Productos en una Tienda*  
**Tecnologías:** Python 3.14, `pytest`, `pytest-cov`, `unittest.mock`

---

## 📋 Descripción del Proyecto

Este proyecto implementa y evalúa un sistema básico de gestión de productos en una tienda de comercio electrónico, diseñado para demostrar las mejores prácticas en pruebas de software:
- **Pruebas unitarias aisladas**
- **Pruebas con excepciones de dominio**
- **Aislamiento mediante dobles de prueba (Test Doubles / Mocks)**
- **Reutilización y preparación del entorno mediante Fixtures**
- **Pruebas de integración de flujo completo (Descuentos y Carrito de compras)**
- **Métricas de cobertura de código (Line & Branch Coverage al 100%)**

---

## 📁 Estructura del Repositorio

```text
TP1/
├── producto.py                  # Entidad Producto con validación y actualización de precio
├── tienda.py                    # Entidad Tienda con inventario, descuentos y carrito
├── excepciones.py               # Excepciones personalizadas del dominio de negocio
├── test_producto.py             # Punto de entrada directo para pruebas de Producto
├── test_tienda.py               # Punto de entrada directo para pruebas de Tienda
├── pytest.ini                   # Configuración del framework pytest
├── requirements.txt             # Dependencias del proyecto (pytest, pytest-cov)
├── .gitignore                   # Archivos y directorios excluidos de control de versiones
├── README.md                    # Documentación, instrucciones y respuestas teóricas
└── tests/                       # Suite modular de pruebas automatizadas
    ├── __init__.py
    ├── conftest.py              # Fixtures compartidos (tienda_con_productos, mocks, etc.)
    ├── test_producto.py         # Tests unitarios de Producto (básicos y excepciones)
    ├── test_tienda.py           # Tests de Tienda (CRUD, excepciones, fixtures, carrito)
    └── test_tienda_doubles.py   # Tests con Dobles de Prueba (Mocks, Stubs, Dummies)
```

---

## 🚀 Instrucciones para Clonar, Configurar y Correr los Tests

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TP1
```

### 2. Crear y Activar el Entorno Virtual
- **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Suite de Pruebas
Para ejecutar todas las pruebas en modo verboso:
```bash
pytest -v
```

Para ejecutar un archivo de pruebas en específico:
```bash
pytest tests/test_producto.py -v
pytest tests/test_tienda.py -v
pytest tests/test_tienda_doubles.py -v
```

### 5. Generar Reporte de Cobertura de Código
Para comprobar la cobertura completa de líneas y ramas de control de flujo (*Branch Coverage*):
```bash
pytest --cov=producto --cov=tienda --cov=excepciones --cov-branch --cov-report=term-missing
```

Para generar un reporte interactivo en HTML:
```bash
pytest --cov=producto --cov=tienda --cov=excepciones --cov-report=html
# Abre htmlcov/index.html en tu navegador
```

---

## 📊 Métricas de Cobertura Obtenidas

Ejecución auditada mediante `pytest-cov`:

```text
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
excepciones.py      14      0      0      0   100%
producto.py         18      0      6      0   100%
tienda.py           32      0     12      0   100%
------------------------------------------------------------
TOTAL               64      0     18      0   100%
```

> **Resultado:** 31 tests superados exitosamente (100% Pass Rate).  
> **Cobertura de Líneas:** 100%  
> **Cobertura de Ramas:** 100%  

---

## 📚 Respuestas a las Preguntas Conceptuales

---

### Sección 1: Configuración Inicial y Pruebas Básicas

#### ¿Puedes identificar pruebas de unidad y de integración en la práctica que se realizó?

**Respuesta:**
Sí, es posible diferenciar con claridad ambos tipos de pruebas según el nivel de aislamiento y los componentes involucrados:

1. **Pruebas de Unidad (Unit Tests):**
   - **Definición:** Tienen como propósito verificar el comportamiento de la unidad atómica más pequeña de software testeable (un método, función o clase) de forma aislada e independiente de cualquier colaborador externo.
   - **En nuestra práctica:**
     - Todas las pruebas de la clase `Producto` (`test_creacion_producto`, `test_representacion_cadena`, `test_actualizar_precio_valido`): verifican exclusivamente el estado interno y métodos de `Producto` sin interactuar con ningún otro objeto del sistema.
     - Las pruebas de la Sección 3 en `test_tienda_doubles.py` (`test_aplicar_descuento_calcula_precio_y_llama_actualizar_precio`): aquí la clase `Tienda` es probada aislando totalmente su dependencia de `Producto` mediante un *Test Double* (`MagicMock`). Por ende, se evalúa únicamente la unidad `Tienda`.

2. **Pruebas de Integración (Integration Tests):**
   - **Definición:** Evalúan la correcta interacción, comunicación, intercambio de mensajes y contratos de interfaz entre dos o más módulos o clases trabajando conjuntamente.
   - **En nuestra práctica:**
     - Las pruebas iniciales de `Tienda` (`test_agregar_producto`, `test_buscar_producto_existente`, `test_eliminar_producto_existente`): aunque son sencillas, utilizan instancias reales de `Producto`, validando que `Tienda` puede almacenar, leer atributos (`producto.nombre`) y manipular objetos reales `Producto`.
     - Las pruebas de la Sección 5 (`TestTiendaIntegracionCarrito`): constituyen pruebas de integración de flujo completo, donde una tienda precargada interactúa con objetos reales `Producto`, aplica descuentos modificando sus estados internos a través de `actualizar_precio`, y luego procesa un carrito sumando sus valores. Se valida que todo el subsistema funcione armónicamente.

---

### Sección 2: Pruebas con Excepciones

#### ¿Podría haber escrito las pruebas primero antes de modificar el código de la aplicación? ¿Cómo sería el proceso de escribir primero los tests? Describe el proceso con tus palabras.

**Respuesta:**
Sí, absolutamente. De hecho, escribir las pruebas antes que el código de producción es el pilar fundamental de la metodología **TDD (Test-Driven Development o Desarrollo Guiado por Pruebas)**, formalizada por Kent Beck.

El proceso sigue un ciclo iterativo y disciplinado conocido como **Red - Green - Refactor**:

```text
   ┌─────────────────────────────────────────────────────────┐
   │ 1. RED: Escribir una prueba que falle                   │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │ 2. GREEN: Escribir el código mínimo para hacerla pasar  │
   └────────────────────────────┬────────────────────────────┘
                                │
                                ▼
   ┌─────────────────────────────────────────────────────────┐
   │ 3. REFACTOR: Limpiar el diseño manteniendo los tests OK │
   └────────────────────────────┬────────────────────────────┘
                                │
                                └─────── Repetir ciclo
```

1. **Fase Roja (Red):**
   - Se redacta primero la prueba automatizada que describe el comportamiento deseado. Por ejemplo:
     ```python
     def test_buscar_producto_inexistente_lanza_excepcion():
         tienda = Tienda()
         with pytest.raises(ProductoNoEncontradoError):
             tienda.buscar_producto("Inexistente")
     ```
   - Al ejecutar `pytest`, la prueba falla de inmediato (porque `buscar_producto` devolvía `None` o la excepción `ProductoNoEncontradoError` ni siquiera estaba definida). Este fallo confirma que la prueba es efectiva y detecta la ausencia de la funcionalidad.

2. **Fase Verde (Green):**
   - Se implementa la cantidad mínima de código en `tienda.py` y `excepciones.py` estrictamente necesaria para que la prueba pase:
     ```python
     for producto in self.inventario:
         if producto.nombre == nombre:
             return producto
     raise ProductoNoEncontradoError(nombre)
     ```
   - Se corre la prueba y se verifica que ahora está en verde.

3. **Fase de Refactorización (Refactor):**
   - Con la prueba garantizando que no rompemos nada, se analiza si el código puede ser más limpio, legible o performante (por ejemplo, reutilizar excepciones de dominio, evitar duplicación de código en `eliminar_producto` llamando internamente a `buscar_producto`).
   - Se vuelve a ejecutar la suite para certificar que el comportamiento sigue intacto.

**Beneficios en este caso práctico:**
Escribir las pruebas primero nos obliga a pensar en la interfaz de uso (qué excepción lanzar, qué mensaje debe contener y cómo reacciona el llamador) antes de ensuciarnos con los detalles internos de la implementación.

---

### Sección 3: Uso de Dobles para Aislar Unidades bajo Prueba

#### En lo que va del trabajo práctico, ¿puedes identificar 'Controladores' y 'Resguardos'?

**Respuesta:**
En la arquitectura y metodología de pruebas de software:

- **Controlador (Test Driver):**
  - **Concepto:** Es un módulo, script o componente auxiliar de nivel superior que invoca y estimula a la unidad bajo prueba (CUT: *Component Under Test*), pasándole datos de entrada y comprobando sus resultados de salida. Reemplaza temporalmente a la interfaz de usuario o al módulo cliente superior que aún no está desarrollado o que se desea aislar.
  - **Identificación en el TP:** Las funciones de prueba de `pytest` (como `test_aplicar_descuento_calcula_precio_y_llama_actualizar_precio`) y el motor de ejecución de `pytest` actúan como **Controladores (Drivers)**, ya que ellos instancian `Tienda`, llaman a su método `aplicar_descuento(...)` y verifican las aserciones.

- **Resguardo (Test Stub / Mock):**
  - **Concepto:** Es un componente auxiliar de nivel inferior que reemplaza a un colaborador secundario del cual depende la unidad bajo prueba. Su propósito es simular respuestas controladas y evitar que la prueba dependa del comportamiento o posibles fallas del componente real.
  - **Identificación en el TP:** En la Sección 3, el objeto simulado creado con `MagicMock(spec=Producto)` actúa como un **Resguardo (Stub/Mock)**. Reemplaza a la clase real `Producto`, proveyendo valores fijos para `nombre` y `precio`, y registrando la invocación a `actualizar_precio` sin requerir la lógica real de `Producto`.

---

#### ¿Qué es un “test double”? ¿Hay otros nombres para los objetos/funciones simulados?

**Respuesta:**
Un **Test Double (Doble de Prueba)** es un término genérico acuñado por Gerard Meszaros (*xUnit Test Patterns*) para describir cualquier objeto o componente que reemplaza a un colaborador real en un entorno de pruebas con el objetivo de aislar la unidad bajo prueba, simplificar el escenario o verificar interacciones indirectas. La analogía proviene del "doble de acción / riesgo" en la cinematografía.

**Taxonomía formal de Dobles de Prueba (según Meszaros / Martin Fowler):**

| Tipo de Doble | Descripción y Propósito | Ejemplo en el Proyecto |
| :--- | :--- | :--- |
| **Dummy** | Objeto que se pasa únicamente para satisfacer firmas de métodos o parámetros requeridos, pero cuyos métodos o atributos nunca son leídos ni utilizados. | Objeto ficticio inyectado en `test_agregar_producto_con_dummy`. |
| **Stub** | Objeto que provee respuestas enlatadas o valores prefijados (hardcodeados) a las llamadas que recibe durante la prueba. No valida interacciones. | Doble que retorna `precio = 200.0` cuando `Tienda` lo consulta. |
| **Spy** | Es un Stub que además registra de forma encubierta información sobre cómo fue llamado (cantidad de llamadas, argumentos enviados) para permitir aserciones posteriores. | El mock utilizado donde verificamos `actualizar_precio.call_count`. |
| **Mock** | Objeto pre-programado con especificaciones y expectativas estrictas sobre las llamadas que debe recibir. Si no se cumplen exactamente, la prueba falla. | `mock.actualizar_precio.assert_called_once_with(150.0)`. |
| **Fake** | Objeto que posee una implementación funcional real pero simplificada o no apta para producción (ej. base de datos en memoria vs. SQL real). | Un almacén de datos temporal en un diccionario en vez de base de datos. |

---

### Sección 4: Uso de Fixtures para Reutilización de Datos

#### Defina usando palabras propias y según la práctica realizada qué es un fixture.

**Respuesta:**
Un **fixture** es una función o mecanismo provisto por el framework de testing cuya misión es preparar, estructurar y dejar en un estado inicial conocido y consistente (la llamada *línea base* o *baseline*) todos los recursos, datos y objetos que una prueba necesita antes de ejecutarse. 

En nuestra práctica, el fixture `tienda_con_productos` en `tests/conftest.py` inicializa una `Tienda` fresca y le agrega de antemano cuatro productos (`Laptop`, `Mouse`, `Teclado`, `Monitor`), permitiendo que cualquier prueba que lo declare como argumento comience inmediatamente a operar sobre esa tienda ya armada.

---

#### ¿Qué ventajas ve en el uso de fixtures? ¿Qué enfoque de diseño de pruebas estaríamos aplicando (caja negra/blanca)?

**Respuesta:**

**Ventajas clave:**
1. **Eliminación de Redundancia (Principio DRY):** Evita tener que repetir 5 a 10 líneas de instanciación manual de tienda y productos en cada test.
2. **Aislamiento e Independencia:** Cada prueba recibe una instancia totalmente nueva y limpia del fixture (en `pytest`, el ciclo de vida por defecto es `scope="function"`), de manera que si un test elimina o modifica un producto, el siguiente test no sufre efectos secundarios ni contaminación de estado.
3. **Facilidad de Mantenimiento:** Si mañana la clase `Producto` requiere un nuevo atributo obligatorio en su constructor (ej. `codigo_sku`), solo modificamos el fixture en un único archivo (`conftest.py`) en lugar de tener que reescribir docenas de tests.
4. **Legibilidad y Foco:** Los tests se vuelven concisos y expresivos, concentrándose únicamente en el estímulo y la verificación.

**Enfoque de diseño de pruebas aplicado:**
- **Caja Negra (Black-Box Testing):** Al consumir el fixture y realizar operaciones (`buscar_producto`, `agregar_producto`, `calcular_total_carrito`), probamos el sistema a través de su interfaz pública y contratos de comportamiento sin importarnos cómo está almacenado internamente el inventario (si es una lista, una tupla o un diccionario hash). Evaluamos entradas y salidas.
- **Caja Blanca (White-Box Testing):** Al mismo tiempo, el diseño exhaustivo de los casos de prueba (valores borde de precios 0, descuentos negativos, descuentos > 100%, productos no encontrados) se fundamentó en el conocimiento estructural de los caminos lógicos y ramas condicionales del código fuente para asegurar una cobertura del 100%.

---

#### Explique los conceptos de Setup y Teardown en testing.

**Respuesta:**
El ciclo de vida estándar de una prueba automatizada consta de 4 fases (fórmula *Arrange-Act-Assert-Cleanup*):

1. **Setup (Configuración / Preparación):**
   - Es la fase preliminar donde se crea el contexto de prueba: se reservan recursos, se instancian objetos, se configuran variables de entorno o se puebla una base de datos con datos de prueba.
   - En frameworks clásicos (`unittest`) se implementa en el método `setUp()`. En `pytest`, corresponde al código previo al `return` o `yield` dentro del fixture.

2. **Teardown (Limpieza / Desmantelamiento):**
   - Es la fase de cierre que se ejecuta incondicionalmente tras terminar la prueba (tanto si pasó como si falló). Su función es liberar memoria, borrar archivos temporales, cerrar conexiones de red o base de datos y restablecer el entorno a su estado original para no perjudicar a las demás pruebas.
   - En `unittest` se utiliza `tearDown()`. En `pytest`, se logra mediante fixtures generadores utilizando `yield`:
     ```python
     @pytest.fixture
     def recurso():
         # SETUP: Inicialización
         conexion = abrir_conexion()
         yield conexion
         # TEARDOWN: Limpieza
         conexion.cerrar()
     ```

---

### Sección 5: Pruebas de Integración y Cobertura

#### ¿Realizó una prueba de cobertura completa? ¿Qué tipo de cobertura utilizó?

**Respuesta:**
Sí, se realizó una prueba de cobertura integral utilizando el plugin `pytest-cov` (que instrumenta el código a través de la librería `coverage.py`).

Se analizaron dos tipos de cobertura:
1. **Cobertura de Sentencias / Líneas (Statement Coverage):**
   - Analiza la proporción de líneas ejecutables de código fuente que fueron visitadas al menos una vez por los tests.
   - **Resultado obtenido:** **100%** sobre todos los módulos de producción (`producto.py`, `tienda.py`, `excepciones.py`). Ninguna línea quedó sin ejecutar.
2. **Cobertura de Ramas (Branch Coverage - opción `--cov-branch`):**
   - Es una métrica más rigurosa que la cobertura de sentencias. Analiza si en cada punto de bifurcación condicional (estructuras `if`, operadores ternarios, bucles `for`) se ejecutaron todas las alternativas posibles (tanto la rama verdadera como la falsa).
   - **Resultado obtenido:** **100% de cobertura de ramas** (18 de 18 ramas evaluadas), garantizando que se probaron tanto los flujos normales como todas las condiciones de excepción y casos límite.

---

#### ¿Puede describir una situación de desarrollo para este caso en donde se plantee pruebas de integración ascendente? Describa la situación.

**Respuesta:**

**Estrategia de Integración Ascendente (Bottom-Up Integration):**
En esta estrategia, las pruebas de integración comienzan evaluando los módulos más elementales o de menor nivel de la jerarquía de dependencias (módulos hoja que no dependen de ningún otro componente de la aplicación) y progresan sucesivamente hacia los módulos de mayor nivel que los integran, utilizando **Drivers (Controladores)** en cada paso para simular a los niveles superiores.

**Escenario de desarrollo para este sistema:**
Imaginemos que estamos desarrollando un sistema de compras para un supermercado:

1. **Paso 1 - Nivel Base (Clase `Producto`):**
   - `Producto` no depende de ninguna otra clase del dominio. Se desarrollan y prueban a fondo sus métodos atómicos: validación de precio no negativo, actualización de precio, categorías y cálculo de impuestos propios del producto.
   - Se asegura que la unidad base sea 100% confiable y robusta.

2. **Paso 2 - Nivel Intermedio (Clase `Tienda` + `Producto`):**
   - Una vez que `Producto` está probado e integrado a nivel unitario, se construye e integra la clase `Tienda` (que gestiona colecciones de `Producto`).
   - Se diseñan pruebas de integración con drivers de prueba que verifican que `Tienda` pueda agregar productos reales, buscar productos, aplicar descuentos interactuando con `Producto.actualizar_precio` y procesar el carrito.

3. **Paso 3 - Nivel Superior (Servicio de Carrito y Pasarela de Pagos / API REST):**
   - Habiendo validado que la integración `Tienda` ↔ `Producto` es sólida, se integra el nivel superior: un controlador REST (`FastAPI`/`Flask`) o un servicio de facturación que recibe peticiones HTTP con listas de carritos, invoca a `Tienda.calcular_total_carrito` y procesa el cobro con un gateway de pagos (como Mercado Pago o Stripe).

**Ventajas de plantear la integración de forma ascendente en esta situación:**
- Los componentes de datos más críticos y fundamentales (`Producto`) son probados exhaustivamente al principio del ciclo.
- Si surge un error al calcular el total del carrito, sabemos de antemano que la lógica de cálculo individual de `Producto` ya está libre de fallos, acotando el diagnóstico a la interacción entre módulos en lugar de buscar errores en las unidades base.
- No se requiere crear resguardos complejos (stubs) de los componentes de datos, ya que estos ya existen y están totalmente probados.
