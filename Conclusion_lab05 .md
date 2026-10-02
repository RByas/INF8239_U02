# Conclusión · U02.LAB05 · Clasificación de texto

## Cierre interpretativo

**Resultado principal:** se entrenaron tres pipelines (baseline, Complement Naive Bayes y regresión logística) sobre DBpedia14, con una partición estratificada 75/25 y semilla 42. El F1 macro fue 0.0095, 0.9696 y 0.9844, respectivamente.

**Modelo seleccionado y evidencia:** regresión logística con TF-IDF de 1 a 2 gramas y `min_df=5`. Supera a Naive Bayes en 0.015 de F1 macro y reduce el error de 3.0% a 1.6%.

**Clase con mayor dificultad:** Company (recall 0.960; precision 0.962).

**Tipo de error más frecuente:** confusión entre pares de clases cercanas, OfficeHolder↔Artist y Company↔Building.

**Impacto en el contexto:** un catálogo automático mezclaría organizaciones con edificios y personas con más de un rol.

**Limitación del dataset:** inglés, Wikipedia de 2014, 14 tipos de entidad y etiquetas automáticas con ruido.

**Decisión antes del despliegue:** aprobar solo para uso demostrativo, con advertencia de alcance y revisión humana en los cruces señalados.

## Conclusión (borrador, 400 a 600 palabras)

El proyecto responde a una pregunta concreta: ¿puede un clasificador clásico de texto asignar un artículo de Wikipedia a una de 14 clases de la ontología de DBpedia? Usamos DBpedia14, con licencia CC BY-SA 3.0 y GNU FDL, descargado desde su fuente original en Hugging Face con una revisión fijada para que otra persona obtenga la misma versión.

La auditoría mostró 630,000 filas, ningún nulo en el texto ni en la etiqueta y 138 textos duplicados, que se eliminaron antes de dividir los datos. Las 14 clases tienen la misma proporción, por lo que el balance es artificial y no refleja la frecuencia real de cada tipo de entidad. El contenido tiene una longitud mediana de 282 caracteres, con unos pocos textos extremadamente largos.

La regresión logística obtuvo el mejor F1 macro, 0.9844, frente a 0.9696 de Naive Bayes y 0.0095 del baseline. La mejora sobre Naive Bayes es pequeña en términos absolutos, pero reduce el error casi a la mitad, de 3.0% a 1.6%. El soporte por clase es equilibrado (11,229 a 11,250 casos), por lo que accuracy y F1 macro coinciden y no hace falta tratar un desbalance.

Sin embargo, un solo número oculta diferencias entre clases. Company presentó el menor recall (0.960, con 446 falsos negativos de 11,249) y la menor precision (0.962, con 428 falsos positivos). Los errores no se reparten al azar: los cruces más frecuentes fueron OfficeHolder hacia Artist (172 casos), Artist hacia OfficeHolder (120), Company hacia Building (113) y Building hacia Company (104).

Revisamos 20 de los 2,452 errores, elegidos con semilla 42 sobre esos cruces. Nueve se explican por ambigüedad entre clases (un hospital, una cervecería o un museo son a la vez institución y edificio). Cinco corresponden a etiquetas discutibles, como una cafetería etiquetada como edificio. Cinco son errores claros del modelo y uno responde a un texto insuficiente. Como la muestra no es aleatoria, no permite estimar proporciones sobre todos los errores. Sí sugiere una hipótesis verificable: una parte importante del error proviene de la ontología y de etiquetas automáticas, no solo del modelo.

El impacto depende del uso. Si el modelo ordenara un catálogo de entidades, confundir empresas con edificios mezclaría organizaciones con estructuras físicas, y confundir cargos públicos con artistas afectaría a personas reales con más de un rol. Para un uso demostrativo el costo es bajo; para decisiones automáticas sobre personas sería inaceptable.

Tres limitaciones deben comunicarse. Primera, el corpus está en inglés y es de 2014, por lo que no representa otros idiomas, entidades recientes ni texto informal. Segunda, las etiquetas se generaron automáticamente y tienen ruido observado. Tercera, el F1 de 0.984 es muy alto y probablemente refleja una tarea fácil, porque muchos resúmenes nombran el tipo de entidad en la primera frase. Es una inferencia que debe comprobarse, y el resultado no garantiza el mismo desempeño con textos menos explícitos.

Por eso la decisión es aprobar el modelo solo para uso demostrativo. La aplicación debe advertir su alcance y presentar la etiqueta como una predicción, no como una verdad. Antes de cualquier despliegue real proponemos tres verificaciones: validar el modelo con textos de otra fuente, medir los duplicados entre los conjuntos originales de entrenamiento y prueba, y revisar manualmente una muestra aleatoria de errores por clase para confirmar la proporción de ambigüedad.