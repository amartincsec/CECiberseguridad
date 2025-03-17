###################################################################################
# Código generado con la ayuda de modelos AI de OpenAI y/o Google y/o Antrophic.###
##################################################################################
# Modificado y adaptado por amartin.
# No se garantiza su exactitud, seguridad o idoneidad para cualquier propósito en particular.
# No utilizar en entornos de producción.
# El usuario es responsable de verificar la licencia y el cumplimiento con derechos de terceros.
#################################################################################################

# MIT License
#
# Copyright (c) 2025 amartin.
#
# Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
# de este software y los archivos de documentación asociados (el "Software"), para
# utilizar el Software sin restricciones, incluyendo sin limitación los derechos
# a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender
# copias del Software, y permitir a las personas a quienes se les proporcione el
# Software hacerlo, sujeto a las siguientes condiciones:
#
# Se debe incluir la presente nota de copyright y permiso en todas las copias o
# partes sustanciales del Software.
#
# EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
# IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN,
# IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
# AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES POR NINGUNA RECLAMACIÓN,
# DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE
# OTRO TIPO, QUE SURJA DEL SOFTWARE O EL USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.

# Este es un script rápido y sucio para incluir direcciones de correo electrónico reales en informes
# de ciberseguridad sin vulnerar la privacidad de los propietarios de las direcciones.

# En un archivo de texto sustituye por asteriscos los caracteres del nombre de usuario excepto primero y 
# último, igualmente del dominio de segundo nivel. Se puede cambiar ese valor (opciones --usuario y --dominio).

# Se pueden extraer sólo los correos, uno por linea (opción --extraer) o se puede generar un fichero igual al de entrada
# con los correos anonimizados.

# Probar: 
# python asteriskmail.py  --help 

__author__ = "$Author: amartin$"
__version__ = "$Version: 1.0.1$"
__date__ = "$Date: 2025-03-17 21:47:37$"

import re
import argparse
import chardet
import sys

def anonimizar_correo(correo, num_chars_usuario, num_chars_dominio, anonimizar=True):
    """Anonimiza una dirección de correo electrónico."""
    partes = correo.split('@')
    if len(partes) != 2:
        return correo

    usuario, dominio = partes
    dominio_partes = dominio.split('.')
    if len(dominio_partes) < 2:
        return correo

    # Anonimizar usuario (sin dividir por puntos)
    if anonimizar:
        if len(usuario) <= 2 * num_chars_usuario:
            usuario_anonimo = usuario
        else:
            usuario_anonimo = usuario[:num_chars_usuario] + '*' * (len(usuario) - 2 * num_chars_usuario) + usuario[-num_chars_usuario:]
    else:
        usuario_anonimo = usuario

    # Anonimizar dominio (manteniendo los puntos)
    if anonimizar:
        subdominio = '.'.join(dominio_partes[:-1])  # Reconstruye el subdominio
        if len(subdominio) <= 2 * num_chars_dominio:
            dominio_anonimo = subdominio
        else:
            dominio_anonimo = subdominio[:num_chars_dominio] + '*' * (len(subdominio) - 2 * num_chars_dominio) + subdominio[-num_chars_dominio:]
        dominio_anonimo += '.' + dominio_partes[-1] # Añade el dominio de nivel superior sin anonimizar
    else:
        dominio_anonimo = dominio

    return usuario_anonimo + '@' + dominio_anonimo

def obtener_codificacion(archivo_entrada):
    """Detecta la codificación del archivo."""
    try:
        with open(archivo_entrada, 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            return result['encoding']
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_entrada} no fue encontrado.", file=sys.stderr)
        return None

def extraer_correos_anonimos(archivo_entrada, num_chars_usuario, num_chars_dominio, encoding=None, anonimizar=True):
    """Extrae y devuelve una lista de correos electrónicos anonimizados."""
    correos_anonimizados = []
    if encoding is None:
        encoding = obtener_codificacion(archivo_entrada) or 'utf-8' # Auto detección.

    try:
        with open(archivo_entrada, 'r', encoding=encoding, errors='ignore') as f_entrada:
            for linea in f_entrada:
                correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linea)
                for correo in correos:
                    correos_anonimizados.append(anonimizar_correo(correo, num_chars_usuario, num_chars_dominio, anonimizar))
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_entrada} no fue encontrado.", file=sys.stderr)

    return correos_anonimizados

def anonimizar_archivo(archivo_entrada, archivo_salida, num_chars_usuario, num_chars_dominio, encoding=None, anonimizar=True):
    """Lee un archivo, anonimiza correos y escribe en otro archivo."""
    if encoding is None:
        encoding = obtener_codificacion(archivo_entrada) or 'utf-8' # Auto detección.

    try:
        with open(archivo_entrada, 'r', encoding=encoding, errors='ignore') as f_entrada, open(archivo_salida, 'w', encoding='utf-8') as f_salida:
            for linea in f_entrada:
                correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linea)
                for correo in correos:
                    linea = linea.replace(correo, anonimizar_correo(correo, num_chars_usuario, num_chars_dominio, anonimizar))
                f_salida.write(linea)
        print(f"Archivo anonimizado guardado en: {archivo_salida}")

    except FileNotFoundError:
        print(f"Error: El archivo {archivo_entrada} no fue encontrado.", file=sys.stderr)

if __name__ == "__main__":

    print(f"\nAsteriskMail.py  {__author__}, {__version__} ({__date__})")

    parser = argparse.ArgumentParser(description="Anonimiza direcciones de correo electrónico en un archivo de texto.")
    parser.add_argument("input", type=str, help="Archivo de entrada con las direcciones de correo.") # Eliminado el argumento opcional
    parser.add_argument("--output", type=str, help="Archivo de salida para el resultado anonimizado. Si no se especifica, se usa la salida estándar.")
    parser.add_argument("-e", "--extraer", action="store_true", help="Extraer solo los correos anonimizados.")
    parser.add_argument("-u", "--usuario", type=int, default=1, help="Número de caracteres visibles del usuario (por defecto: 1).")
    parser.add_argument("-d", "--dominio", type=int, default=1, help="Número de caracteres visibles del dominio (por defecto: 1).")
    parser.add_argument("--encoding", type=str, default=None, help="Codificación del archivo de entrada (detección automática si no se especifica). Codificaciones comunes: utf-8, latin1, cp1252. Ver lista completa: https://docs.python.org/3/library/codecs.html#standard-encodings")
    parser.add_argument("--noanon", action="store_true", help="Desactiva la anonimización de las direcciones de correo.")
    parser.add_argument("--resumen", action="store_true", help="Muestra un resumen de los correos encontrados al final.")

    args = parser.parse_args()

    # Entrada y salida
    try:
        with open(args.input, 'r', encoding=args.encoding) as f_entrada:
            lineas = f_entrada.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo {args.input} no fue encontrado.", file=sys.stderr)
        sys.exit(1)

    correos_anonimizados = [] # Inicializar la lista de correos anonimizados

    if args.extraer:
        print()  # Línea en blanco antes de la salida
        for linea in lineas:
            correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linea)
            for correo in correos:
                correos_anonimizados.append(anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon))
                print(anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon))
        print()  # Línea en blanco después de la salida
    else:
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f_salida:
                    for linea in lineas:
                        correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linea)
                        for correo in correos:
                            linea = linea.replace(correo, anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon))
                            correos_anonimizados.append(anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon)) # Agregar a la lista de correos anonimizados
                        f_salida.write(linea)
                print(f"Archivo anonimizado guardado en: {args.output}")
            except FileNotFoundError:
                print(f"Error: No se pudo crear el archivo {args.output}.", file=sys.stderr)
                sys.exit(1)
        else:
            for linea in lineas:
                correos = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', linea)
                for correo in correos:
                    linea = linea.replace(correo, anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon))
                    correos_anonimizados.append(anonimizar_correo(correo, args.usuario, args.dominio, not args.noanon)) # Agregar a la lista de correos anonimizados
                sys.stdout.write(linea)

    # Resumen de correos (solo una línea)
    if args.resumen:
        print(f"\nSe han procesado {len(correos_anonimizados)} correos.", file=sys.stderr)
