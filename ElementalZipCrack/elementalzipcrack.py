###################################################################################
# Código generado con la ayuda de modelos AI de OpenAI y/o Google y/o Antrophic.###
###################################################################################
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

# Rápido y sucio para averiguar la contraseña de archivos ZIP por fuerza bruta con diccionario.
# Pensado para ejecutar en Kali, pero funciona en W10,11.
# Prueba:
# python elementalzipcrack.py --help
__author__ = "$Author: amartin$"
__version__ = "$Version: 1.0.1$"
__date__ = "$Date: 2025-03-17 21:47:37$"

import zipfile
import time
import sys
import os
import gzip
import shutil
import argparse

def decompress_gz(file_path):
    decompressed_path = file_path[:-3]  # Remove .gz extension
    print(f"Descomprimiendo {file_path}...")
    with gzip.open(file_path, 'rb') as f_in:
        with open(decompressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return decompressed_path

def check_and_decompress_if_needed(wordlist):
    # Si el archivo existe tal cual, lo usamos
    if os.path.exists(wordlist):
        return wordlist
    # Si existe la versión comprimida, la descomprimimos
    elif os.path.exists(wordlist + '.gz'):
        return decompress_gz(wordlist + '.gz')
    # Si no existe ninguna versión
    else:
        print(f"El diccionario '{wordlist}' no existe. Cancelando.")
        sys.exit(1)

def crack_zip(zip_filename, wordlist):
    # Si el diccionario termina en .gz, lo descomprimimos
    if wordlist.endswith('.gz'):
        wordlist = decompress_gz(wordlist)
    else:
        # Verificar si necesitamos descomprimir una versión .gz
        wordlist = check_and_decompress_if_needed(wordlist)
    
    elapsed_time = 0.01  # Necesario por si encuentra la solución justo al principio.
    
    print(f"Ejercicio de la asignatura de hacking ético. Curso 2024-2025.\n")
    try:
        print(f"Probando por fuerza bruta la contraseña del archivo: {zip_filename},")
        print(f"con las palabras del diccionario: {wordlist}\n")
        
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            with open(wordlist, 'r', encoding='latin-1') as f:
                count = 0
                start_time = time.time()
                last_update_time = time.time()
                found_password = None
                for line in f:
                    password = line.strip().encode('latin-1')
                    count += 1
                    
                    if time.time() - last_update_time >= 0.01:
                        elapsed_time = time.time() - start_time
                        sys.stdout.write(f"\rContraseñas: {count:,.0f}, tiempo transcurrido: {elapsed_time:.2f} segundos")
                        sys.stdout.flush()
                        last_update_time = time.time()
                    
                    try:
                        zip_file.extractall(pwd=password)
                        found_password = password.decode('latin-1')
                        break
                    except (RuntimeError, zipfile.BadZipFile):
                        pass
                
                print(f"\nTotal probadas: {count:,.0f} en {0.01 + elapsed_time:.2f} segundos ({count/elapsed_time:,.1f} P/s)")
                if found_password:
                    print(f"\nContraseña encontrada (entre corchetes):[{found_password}]\n")
                else:
                    print("No se encontró la contraseña en el diccionario.")
    except FileNotFoundError:
        print("El archivo ZIP o el diccionario no fueron encontrados.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(f"\nElementalZipCrack.py  {__author__}, {__version__} ({__date__})\n")
    print(f"python elementalzipcrack.py --help\n")
	
    parser = argparse.ArgumentParser(description="Crackeo de ZIP por fuerza bruta con un diccionario")
    parser.add_argument("-z", "--zip", type=str, default="test.zip", help="Archivo ZIP a crackear (por defecto: test.zip)")
    parser.add_argument("-d", "--diccionario", type=str, default="/usr/share/wordlists/rockyou.txt", help="Diccionario a usar (por defecto: /usr/share/wordlists/rockyou.txt)")
    args = parser.parse_args()
    
    if not os.path.exists(args.zip):
        print(f"El archivo ZIP '{args.zip}' no existe. Cancelando.")
        sys.exit(1)
    
    crack_zip(args.zip, args.diccionario)
