## asteriskmail.py 


**lsasteriskmail.py** es una herramienta educativa que anonimiza direcciones de correo electrónico en un fichero de texto reemplazando caracteres con asteriscos. Útil para informes de ciberseguridad, no debe usarse en entornos de producción.

---
### Uso: 
---
`python asteriskmail.py [-h] [--output OUTPUT] [-e] [-u USUARIO] [-d DOMINIO] [--encoding ENCODING] [--noanon] [--resumen] input`

	positional arguments:
	
	input                 Archivo de entrada con las direcciones de correo.

	options:
	
	-h, --help            show this help message and exit
	--output OUTPUT       Archivo de salida para el resultado anonimizado. Si no se especifica, se usa la salida estándar.
	-e, --extraer         Extraer solo los correos anonimizados.
	-u, --usuario USUARIO
                          Número de caracteres visibles del usuario a cada lado del nombre( por defecto: 1 ).
	-d, --dominio DOMINIO
                          Número de caracteres visibles del dominio (por defecto: 1, incluye todos los niveles salvo el uno).
	--encoding ENCODING   Codificación del archivo de entrada (detección automática si no se especifica). Codificaciones
                          comunes: utf-8, latin1, cp1252. Ver lista completa:
                          https://docs.python.org/3/library/codecs.html#standard-encodings
	--noanon              Desactiva la anonimización de las direcciones de correo.
	--resumen             Muestra un resumen de los correos encontrados al final.
---
### Ejemplos:
---
- **Para ver los correos ya anonimizados de un fichero de texto (uno por linea) y que muestre cuantos al final:**

    ```python asteriskmail.py --resumen --extraer fichero.txt```


- **Para ver los correos de un fichero de texto sin anonimizar ( uno por linea )**

    ```python asteriskmail.py --extraer --noanon fichero.txt```


- **Para generar un fichero idéntico a fichero.txt pero con los correos anonimizados:**

     ```python asteriskmail.py --output fichero.anonimo fichero.txt```


- **o también:**

    ```python asteriskmail.py fichero.txt > fichero.anonimo```


- **Para anonimizar (no tanto) las direcciones de correo de fichero.txt**

    ```python asteriskmail.py --dominio 3 --usuario 2 fichero.txt```

**Resultado:**

Convierte en asteriscos la dirección de correo exepto los 3 primeros y últimos caracteres 
del dominio de segundo nivel y siguientes y también los 2 primeros y últimos del usuario. 
No se modifica el dominio de primer nivel.

`este-es-el-usuario@dominio-de-tercer-nivel.dominio-de-segundo-nivel.dominio-de-primer-nivel`  

pasa a ser:  

`es**************io@dom******************************************vel.dominio-de-primer-nivel`

o también:

`jhondoedoe@un-dominio.com`  

pasa a ser:

`jh******oe@un-****nio.com`  

---
### Notas:
---
-Una vez que se ha anonimizado un correo no funcionará sobre el resultado porque 
los asteriscos impiden que se reconozca como una dirección válida.

-A partir de 4 ó 5 direcciones empieza a ser práctico, sobre todo si hay muchas mezcladas con el resto del texto.

-Necesita ser probado con ficheros largos y distintas codificaciones.
