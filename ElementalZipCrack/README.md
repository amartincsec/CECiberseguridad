## elementalzipcrack.py


**elementalzipcrack.py** es una herramienta educativa que permite averiguar la contraseña de un fichero zip mediante el uso de un diccionario. No debe usarse en entornos de producción.



---
### Uso: 
---

`python elementalzipcrack.py [-h] [-z ZIP] [-d DICCIONARIO]`

usage: 

	options:
	-h, --help            show this help message and exit
	-z, --zip ZIP         Archivo ZIP a crackear (por defecto: test.zip)
	-d, --diccionario DICCIONARIO
                          Diccionario a usar (por defecto: /usr/share/wordlists/rockyou.txt)

### Ejemplos:
---
- **Para probar con las palabras de rockyou.txt (en kali) el fichero test.zip**

    ```python elementalzipcrack.py```


- **Para probar con las palabras de rockyou.txt (en kali) el fichero secreto.zip**

	```python elementalzipcrack.py --zip secreto.zip```
	
	
- **Para probar con las palabras de MIDICCIONARIO.TXT el fichero secreto.zip**

	```python elementalzipcrack.py -d MIDICCIONARIO.TXT --zip secreto.zip```



**Resultado:**

	python elementalzipcrack.py -z test.zip

	python elementalzipcrack.py --help

	Ejercicio de la asignatura de hacking ético. Curso 2024-2025.

	Probando por fuerza bruta la contraseña del archivo: test.zip,
	con las palabras del diccionario: /usr/share/wordlists/rockyou.txt

	Contraseñas: 124,634, tiempo transcurrido: 6.13 segundos
	Total probadas: 124,801 en 6.14 segundos (20,344.5 P/s)

	Contraseña encontrada (entre corchetes):[esternocleidomastoideo]


---
### Notas:
---
- Si el diccionario tiene extensión **gz** se descomprime primero.
- **rockyou.txt** contiene aproximadamente 14 millones de palabras que se recorren en menos de 10 minutos.
- A la vista está que no es buena idea utilizar claves que figuren en algún diccionario.

