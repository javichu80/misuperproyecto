import os

# 1. Ruta de destino exacta según tu Blueprint
RUTA_DESTINO = "courses/matematicas_1eso/tema_01_numeros_naturales/"

# 2. Diccionario con todas las lecciones del bloque (de la 4 a la 9) en formato Raw String r"""
lecciones = {
    "lesson_04.md": r"""---
pregunta_test: "¿Cuál es el redondeo a las decenas de millar del número 538.298?"
opciones_test:
  - "A) 530.000 unidades"
  - "B) 540.000 unidades"
  - "C) 500.000 unidades"
  - "D) 538.000 unidades"
opcion_correcta: "B) 540.000 unidades"
feedback_correcto: "¡Excelente! 🌟 Como la cifra de las unidades de millar es 8 (mayor o igual que 5), sumamos uno a las decenas de millar."
---

# Lección 4: Aproximaciones y redondeo

## Objetivo
Aprender a aproximar números naturales mediante truncamiento y redondeo a un orden de unidades determinado.

## Conceptos clave
* **Aproximar**: Sustituir un número por otro cercano y más sencillo de manejar.
* **Truncamiento**: Eliminar todas las cifras a la derecha del orden elegido sustituyéndolas por ceros.
* **Redondeo**: Observar la primera cifra eliminada; si es menor que 5 se mantiene la cifra anterior, si es 5 o mayor se le suma uno.

## Explicación
En la vida real, a menudo usamos datos aproximados. Por ejemplo, si el solucionario indica que la producción pesquera es de $886.811$ toneladas, podemos decir de forma aproximada que es de unas $890.000$ toneladas.

Reglas para el Redondeo:
1. Identifica el orden de unidades al que vas a aproximar (ej: centenas).
2. Mira la cifra que está justo a su derecha.
3. Si es un $0, 1, 2, 3$ o $4$, deja la cifra igual.
4. Si es un $5, 6, 7, 8$ o $9$, aumenta esa cifra en una unidad.
5. Cambia el resto de cifras de la derecha por ceros.

## Ejemplo
* El precio de una vivienda en el solucionario es de $293.528 \text{ €}$. 
* Si aproximamos por **truncamiento** a las centenas de millar, obtenemos: $200.000 \text{ €}$.
* Si aproximamos por **redondeo** a las decenas de millar, miramos el 3 (unidades de millar). Como $3 < 5$, el redondeo es: $290.000 \text{ €}$.

## Errores frecuentes
* **Sumar siempre uno**: Sumar uno a la cifra de redondeo aunque la siguiente sea menor que 5. Recuerda: en $43.210$, el redondeo a las decenas de millar es $40.000$, no $50.000$.

## Actividades prácticas
1. Redondea a los millares el número de capturas pesqueras: $886.811$ toneladas.
2. Trunca a las centenas el número de teléfono del ejercicio: $9900$.
3. Escribe un ejemplo del solucionario donde sea más útil usar un número aproximado que un número exacto.

## Resumen
Las aproximaciones facilitan el cálculo mental y la comprensión de cantidades grandes, siendo el redondeo el método más exacto ya que minimiza el error cometido.""",

    "lesson_05.md": r"""---
pregunta_test: "En una operación $A - B = C$, si el minuendo $A$ es 1.500 y el sustraendo $B$ es 400, ¿cuál es la diferencia $C$?"
opciones_test:
  - "A) 1.900"
  - "B) 1.100"
  - "C) 1.000"
  - "D) 900"
opcion_correcta: "B) 1.100"
feedback_correcto: "¡Correcto! 📉 Has aplicado la resta correctamente: $1.500 - 400 = 1.100$."
---

# Lección 5: Suma y resta

## Objetivo
Dominar las operaciones fundamentales de la suma y la resta con números naturales, comprendiendo sus términos y propiedades básicas.

## Conceptos clave
* **Suma (Sumandos)**: Operación de agrupar o añadir cantidades. Tiene propiedad conmutativa ($a+b = b+a$) y asociativa.
* **Resta**: Operación de quitar o hallar la diferencia entre dos cantidades. Sus términos son Minuendo, Sustraendo y Diferencia.
* **Prueba de la resta**: Se cumple estrictamente que: $\text{Minuendo} = \text{Sustraendo} + \text{Diferencia}$.

## Explicación
La suma y la resta son las herramientas principales para gestionar inventarios o flujos de caja en los ejercicios de tu solucionario. 
* Sumar es añadir. Si un camión de reparto descarga $450$ kilos de fruta en un supermercado y luego añade $300$ kilos más en otro, realizamos una suma.
* Restar es comparar o quitar. No tiene propiedad conmutativa (no es lo mismo $10 - 4$ que $4 - 10$, de hecho, este último no tiene solución en los números naturales).

## Ejemplo
* Si un ganadero tiene un rebaño de $1.200$ ovejas y vende $350$, planteamos la resta:
  $$1.200 \text{ (Minuendo)} - 350 \text{ (Sustraendo)} = 850 \text{ (Diferencia)}$$
* Comprobamos con la prueba de la resta: $850 + 350 = 1.200$.

## Errores frecuentes
* **Intentar conmutar la resta**: Cambiar el orden de los términos en una resta. El minuendo siempre debe ser mayor o igual que el sustraendo dentro del conjunto de los números naturales.

## Actividades prácticas
1. Si realizas la operación $2.307.037 - 300.000$, ¿qué término cambia en el valor de posición?
2. Un almacén tiene $5.000$ cajas. Si por la mañana salen $1.250$ y por la tarde entran $800$, ¿cuántas cajas quedan al final del día?
3. Aplica la propiedad asociativa para resolver de dos formas diferentes: $150 + 25 + 75$.

## Resumen
La suma y la resta son operaciones inversas. Dominar sus términos permite realizar comprobaciones rápidas y asegurar la exactitud de cualquier cálculo financiero o de reparto.""",

    "lesson_06.md": r"""---
pregunta_test: "¿Qué expresión representa la propiedad distributiva para $5 \times (10 + 2)$?"
opciones_test:
  - "A) $(5 \times 10) + 2"
  - "B) $5 \times 12"
  - "C) $(5 \times 10) + (5 \times 2)"
  - "D) $50 + 2"
opcion_correcta: "C) $(5 \times 10) + (5 \times 2)"
feedback_correcto: "¡Perfecto! 🧠 La propiedad distributiva indica que el factor multiplica a cada uno de los sumandos de forma independiente."
---

# Lección 6: Multiplicación

## Objetivo
Comprender el concepto de la multiplicación como suma abreviada de sumandos iguales y dominar la propiedad distributiva para agilizar el cálculo mental.

## Conceptos clave
* **Multiplicación (Factores y Producto)**: Operación abreviada. Los números que se multiplican se llaman factores y el resultado es el producto.
* **Propiedad Conmutativa**: El orden de los factores no altera el producto ($a \times b = b \times a$).
* **Propiedad Distributiva**: Multiplicar un número por una suma es igual a la suma de los productos de dicho número por cada uno de los sumandos:
  $$a \times (b + c) = (a \times b) + (a \times c)$$

## Explicación
Multiplicar nos ahorra tiempo cuando sumamos la misma cantidad muchas veces. En el solucionario, si compramos $12$ cajas de bombones y cada caja cuesta $6 \text{ €}$, en lugar de hacer $6+6+6...$ doce veces, multiplicamos $12 \times 6$.

La propiedad distributiva es el gran truco del cálculo mental. Si tienes que multiplicar $7 \times 102$, puedes descomponerlo como $7 \times (100 + 2)$ y resolver mentalmente: $700 + 14 = 714$.

## Ejemplo
* Desglose de un pedido industrial usando la propiedad distributiva:
  $$8 \times (20 + 5) = (8 \times 20) + (8 \times 25) = 160 + 40 = 200$$

## Errores frecuentes
* **Olvidar multiplicar el segundo sumando**: En la expresión $3 \times (10 + 4)$, cometer el error de escribir $(3 \times 10) + 4 = 34$. Recuerda que el factor exterior debe multiplicar obligatoriamente a **todos** los elementos de dentro del paréntesis: $30 + 12 = 42$.

## Actividades prácticas
1. Resuelve aplicando la propiedad distributiva para agilizar el cálculo mental: $6 \times 99$ (Pista: usa $6 \times (100 - 1)$).
2. Si un hotel tiene $4$ plantas y cada planta tiene $25$ habitaciones, ¿cuántas habitaciones tiene en total? Aplica la propiedad conmutativa para verificarlo.
3. Identifica los factores y el producto en el ejercicio de las cajas de manzanas del solucionario: $15 \times 20 = 300$.

## Resumen
La multiplicación es una herramienta de escala fundamental. Conocer sus propiedades asociativa, conmutativa y distributiva es clave para simplificar operaciones algebraicas complejas.""",

    "lesson_07.md": r"""---
pregunta_test: "En una división, si el divisor es 12, el cociente es 10 y el resto es 3, ¿cuál es el Dividendo?"
opciones_test:
  - "A) 120"
  - "B) 123"
  - "C) 15"
  - "D) 36"
opcion_correcta: "B) 123"
feedback_correcto: "¡Excelente! 🎉 Has aplicado la propiedad fundamental: $D = d \times c + r \rightarrow 12 \times 10 + 3 = 123$."
---

# Lección 7: División

## Objetivo
Comprender la división como la operación inversa a la multiplicación, diferenciando divisiones exactas e inexactas, y asimilando su propiedad fundamental.

## Conceptos clave
* **División**: Operación de repartir una cantidad en partes iguales. Sus componentes son Dividendo ($D$), Divisor ($d$), Cociente ($c$) y Resto ($r$).
* **División Exacta**: Aquella en la que el resto es igual a cero ($r = 0$).
* **División Entera (Inexacta)**: Aquella en la que el resto es diferente de cero ($r \neq 0$). El resto siempre debe ser menor que el divisor ($r < d$).
* **Propiedad Fundamental**: En toda división se cumple que:
  $$D = d \times c + r$$

## Explicación
Dividir es hacer partes. Si el solucionario plantea que disponemos de $445.115$ kilos de pescado congelado y queremos empaquetarlos en cajas de $5$ kilos, realizamos una división para saber cuántas cajas obtendremos.
* Si el reparto no deja ningún elemento suelto, la división es exacta.
* Si sobran elementos que ya no se pueden repartir de forma equitativa, esos elementos constituyen el resto.

## Ejemplo
* Repartir $47$ lápices entre $4$ alumnos:
  $$47 = 4 \times 11 + 3$$
  Donde el Dividendo es $47$, el divisor es $4$, cada alumno recibe $11$ lápices (cociente) y sobran $3$ lápices (resto). Como $3 < 4$, la operación es correcta.

## Errores frecuentes
* **Permitir un resto mayor que el divisor**: Terminar una división dejando un resto igual o superior al divisor. Si al dividir entre $6$ te sobra $7$, significa que podías haberle dado una unidad más al cociente.

## Actividades prácticas
1. Realiza la división e indica si es exacta o entera: $840 \div 12$.
2. Averigua el dividendo de una operación matemática del solucionario donde el divisor es $25$, el cociente es $8$ y el resto es $12$.
3. Si repartes $120 \text{ €}$ entre 0 personas, ¿qué ocurre? Explica por qué está prohibido dividir entre cero en matemáticas.

## Resumen
La multiplicación es una herramienta de escala fundamental. Conocer sus propiedades asociativa, conmutativa y distributiva es clave para simplificar operaciones algebraicas complejas.""",

    "lesson_08.md": r"""---
pregunta_test: "¿Cuál es el resultado correcto de la operación combinada: $20 - 4 \\times 3 + 2$?"
opciones_test:
  - "A) 50"
  - "B) 10"
  - "C) 6"
  - "D) 14"
opcion_correcta: "B) 10"
feedback_correcto: "¡Impecable! 🎯 Primero resolviste la multiplicación ($4 \\times 3 = 12$), luego restaste ($20 - 12 = 8$) y finalmente sumaste ($8 + 2 = 10$)."
---

# Lección 8: Operaciones combinadas

## Objetivo
Aprender a resolver expresiones numéricas donde aparecen varias operaciones mezcladas, aplicando con total rigurosidad la jerarquía de operaciones.

## Conceptos clave
* **Prioridad / Jerarquía**: Orden obligatorio en el que deben resolverse las operaciones matemáticas para evitar resultados erróneos.
* **Orden de prioridad universal**:
  1. Paréntesis, corchetes y llaves (desde dentro hacia fuera).
  2. Multiplicaciones y Divisiones (de izquierda a derecha si coinciden en el mismo nivel).
  3. Sumas y Restas (de izquierda a derecha).

## Explicación
Cuando en un mismo ejercicio del solucionario se juntan sumas, restas, paréntesis y multiplicaciones, no podemos resolver en el orden en que leemos las palabras (de izquierda a derecha). Si lo hacemos de forma lineal, el resultado será incorrecto. Las matemáticas tienen una ley de prioridades estricta para que una misma expresión valga exactamente lo mismo en cualquier lugar del mundo.

Si ves $5 + 3 \times 2$, la multiplicación tiene más "fuerza" o prioridad que la suma. Por tanto, primero calculamos $3 \times 2 = 6$, y luego sumamos $5 + 6 = 11$.

## Ejemplo
* Resolución paso a paso de una operación combinada compleja del tema:
  $$3 \times (12 - 4) + 18 \div 3$$
  1. Resolvemos el paréntesis primero: $12 - 4 = 8$. La expresión queda: $3 \times 8 + 18 \div 3$.
  2. Resolvemos multiplicaciones y divisiones a la vez: $3 \times 8 = 24$ y $18 \div 3 = 6$. La expresión queda: $24 + 6$.
  3. Resolvemos la suma final: $24 + 6 = 30$.

## Errores frecuentes
* **Resolver de izquierda a derecha de forma ciega**: En la expresión $10 - 2 \times 4$, hacer la resta primero: $8 \times 4 = 32$. ¡Error! La multiplicación va antes: $10 - 8 = 2$.

## Actividades prácticas
1. Resuelve respetando la prioridad de operaciones: $(8 + 2) \times 5 - 12 \div 4$.
2. Introduce un paréntesis en la expresión $5 + 3 \times 2$ para conseguir que el resultado final sea exactamente $16$.
3. Explica los pasos necesarios del solucionario para calcular el valor de: $50 - [4 \times (3 + 2)]$.

## Resumen
La jerarquía de operaciones ordena el cálculo numérico. Seguir sus reglas paso a paso es la única forma de garantizar la validez del resultado en expresiones algebraicas.""",

    "lesson_09.md": r"""---
pregunta_test: "Un tren sale con 120 pasajeros. En la primera estación bajan 30 y suben 15. ¿Qué operación planifica este problema?"
opciones_test:
  - "A) $120 + 30 + 15"
  - "B) $120 - 30 + 15"
  - "C) $120 - (30 + 15)"
  - "D) $120 \\times 30 \\div 15"
opcion_correcta: "B) $120 - 30 + 15"
feedback_correcto: "¡Extraordinario! 🚀 Has interpretado que 'bajan' resta pasajeros ($ -30 $) y 'suben' añade pasajeros ($ +15 $)."
---

# Lección 9: Problemas con números naturales

## Objetivo
Desarrollar una estrategia sistemática para abordar y resolver problemas matemáticos de la vida cotidiana utilizando operaciones combinadas con números naturales.

## Conceptos clave
* **Método de Polya**: Estrategia de 4 pasos para resolver cualquier problema:
  1. **Comprender el enunciado**: Leer con atención, identificar la pregunta y extraer los datos útiles.
  2. **Trazar un plan**: Pensar qué operaciones (suma, resta, etc.) relacionan los datos con la incógnita.
  3. **Ejecutar el plan**: Realizar los cálculos numéricos de forma ordenada y limpia.
  4. **Examinar la solución**: Verificar si el resultado tiene sentido lógico y responde a la pregunta.

## Explicación
El objetivo final de aprender a sumar, restar, aproximar o dividir es poder solucionar problemas reales como los que plantea el solucionario de Anaya (distribución de presupuestos, recuento de mercancías, cálculo de distancias o repartos de herencias).

La mayor dificultad no suele estar en el cálculo numérico, sino en la fase de traducción: pasar el enunciado en lenguaje de texto a una expresión matemática formal.

## Ejemplo
* *Problema*: Un colegio compra $8$ diccionarios a $25 \text{ €}$ cada uno y $15$ atlas a $12 \text{ €}$ cada uno. Si pagan con un billete de $500 \text{ €}$, ¿cuánto dinero les sobra?
* *Plan y Ejecución*: Planteamos la operación combinada completa del dinero que se gasta y lo restamos del total:
  $$\text{Dinero restante} = 500 - (8 \times 25 + 15 \times 12)$$
  $$\text{Dinero restante} = 500 - (200 + 180) = 500 - 380 = 120 \text{ €}$$
  *Respuesta*: Al colegio le devuelven exactamente $120 \text{ €}$. El resultado es lógico porque el gasto es menor que el billete aportado.

## Errores frecuentes
* **Operar números sin entender su significado**: Empezar a multiplicar o sumar todos los datos numéricos que aparecen en el texto sin haber razonado antes si la cantidad final debe ser mayor o menor que la inicial.

## Actividades prácticas
1. Un comerciante compra $50$ sacos de patatas de $5$ kilos por un total de $150 \text{ €}$. Si luego vende cada kilo a $1 \text{ €}$, ¿cuánto beneficio económico obtiene al vender toda la mercancía?
2. Aplica los 4 pasos de Polya para resolver el problema de las llamadas telefónicas de tu solucionario.
3. Inventa un problema matemático que se resuelva utilizando la siguiente expresión: $100 - 3 \times 25$.

## Resumen
Resolver problemas entrena el pensamiento crítico y el razonamiento lógico, conectando las operaciones matemáticas abstractas con soluciones útiles para el día a día."""}


# --- EJECUCIÓN SECUENCIAL DIRECTA (SINTAXIS BLINDADA) ---
os.makedirs(RUTA_DESTINO, exist_ok=True)
print(f"🚀 Iniciando creación directa en: {RUTA_DESTINO}")

for nombre_archivo, contenido in lecciones.items():
    ruta_completa = os.path.join(RUTA_DESTINO, nombre_archivo)
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido.strip())
        print(f"✅ Creado con éxito: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al escribir {nombre_archivo}: {e}")

print("\n🎉 ¡PROCESO COMPLETADO!")
