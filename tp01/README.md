## Trabajo Practico
## Tratamiento y Análisis del Texto

Bibliografía: [MIR] Capítulo 7, [TOL] Capítulo 3, [MAN] Capítulos 6 (parcial).
Paper: “What is a word, What is a sentence? Problems of Tokenization”, Gregory Grefenstette , Pasi Tapanainen.
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.28.5162&rep=rep1&type=pdf

1) Escriba un programa que realice operaciones simples de análisis léxico sobre la colección T12012-gr y calcule medidas básicas sobre la misma. Su programa debe recibir como parámetros el directorio donde se encuentran los documentos y un argumento que indica si se deben eliminar las palabras vacías (y en tal caso, el nombre del archivo que las contiene). Defina, además, una longitud mínima y máxima para los términos. Como salida, el programa debe generar:

* Un archivo (terminos.txt) con la lista de términos a indexar (ordenado), su frecuencia en la colección y su DF (Document Frequency).
* Un segundo archivo (estadisticas.txt) con los siguientes datos:
  * Cantidad de documentos procesados
  * Cantidad de tokens y términos extraídos
  * Promedio de tokens y términos de un documento
  * Largo promedio de un término
  * Cantidad de tokens y términos del documento más corto y del más largo
  * Cantidad de términos que aparecen sólo 1 vez en la colección
* Un tercer archivo con:
  * La lista de los 10 términos más frecuentes y su CF (Collection Frequency)
  * La lista de los 10 términos menos frecuentes y su CF.

Su programa debe utilizar llamadas a las siguientes funciones:

	lista_tokens = tokenizar(string)

La función “tokenizar” realiza la normalización del texto contenido en la variable (string) y la divide en tokens que inserta en la lista que retorna (con duplicados).

	lista_tokens2 = sacar_palabras_vacias(lista_tokens, lista_vacias)

En este caso, la función recibe dos listas: la primera a procesar y la segunda con la lista de palabras vacías (que generalmente se leen desde un archivo al inicio). Por ejemplo:

	import sys
	def tokenizar(string):
	…
	def sacar_palabras_vacias(lista_tokens, lista_vacias) :
	…
	if __name__ == "__main__":
	directory = sys.argv[1]
	…
	sys.exit(0)

2) Tomando como base su programa anterior, escriba un segundo Tokenizer que implemente los criterios del artículo de Grefenstette y Tapanainen para definir qué es una “palabra” (o término) y cómo tratar números y signos de puntuación. Luego, antes de tokenizar extraiga en listas separadas:

* Abreviaturas tal cual están escritas (por ejemplo, Dr., Lic., S.A., NASA, etc.)
* Direcciones de correo electrónico y URLs
* Números (por ejemplo, cantidades, teléfonos)
* Nombres propios (por ejemplo, Villa Carlos Paz, Manuel Belgrano, etc.) y los trate como un único token.

Genere y almacene la misma información que en caso anterior.

3) Repita el procesamiento del ejercicio 1 utilizando la colección T12012-qm. Verifique los resultados e indique las reglas que debería modificar para que el tokenizer responda al dominio del problema.

4) A partir de su programa del ejercicio 1, incluya un proceso de stemming1. Luego de modificar su programa, corra nuevamente el proceso del ejercicio 1 y analice los cambios en la colección. ¿Qué implica este resultado? Busque ejemplos de pares de términos que tienen la misma raíz pero que el stemmer los trató diferente y términos que son diferentes y se los trató igual.

Los siguientes ejercicios se deben realizar en una “notebook IPython” 2 para trabajar en un entorno interactivo que provee – además – capacidades gráficas.

5) En este ejercicio se propone verificar la predicción de ley de Zipf. Para ello, descargue desde Project Gutenberg el texto del Quijote de Cervantes 3 y escriba un programa que extraiga los términos y calcule las frecuencias (use las funciones de sus programas anteriores). Con dichos datos y los estimados por Zipf grafique en la notebook ambas distribuciones (haga 2 gráficos, uno en escala lineal y otro en log-log). ¿Cómo se comporta la predicción? ¿Qué conclusiones puede obtener? Repita el análisis podando un porcentaje x (use x = 5, 10 y 15%) de los términos más y menos frecuentes. ¿Con qué porcentaje de poda se mejora la predicción para este texto?

6) Suponga que tiene que construir un índice para recuperación y decide omitir aquellos términos cuya frecuencia es menor a 5. Usando los datos del ejercicios anterior y de acuerdo a la ley de Zipf, qué proporción del total de términos estaría omitiendo? Justifique.  ¿Qué proporción está realmente omitiendo si indexa el texto del ejercicio anterior?

7) Para el texto del ejercicio 5 procese cada palabra en orden y calcule los pares (#términos totales procesados, #términos únicos). Verifique en qué medida satisface la ley de Heaps. Grafique en la notebook los ajustes variando los parámetros de la expresión.


Puede utilizar la librería NLTK (Natural Language Toolkit). Revise qué algoritmos soporta para español e inglés.
http://ipython.org/notebook.html
http://www.gutenberg.org/cache/epub/2000/pg2000.txt (en UTF-8)

