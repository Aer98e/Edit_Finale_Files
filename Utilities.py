import pyautogui
from typing import Union, Optional
import time
import Finale_Objects as FinOb
import sys


Afirmative = ('SI', 'S', 'Y', 'YES', '1')
Negative = ('NO', 'N', '0')

def Consult_Data(peticion:str = 'Elemento') -> tuple[str, Union[str, tuple]]:
        """Solicita un nombre y un atajo de teclado que los retorna al terminar.

            Args:
                peticion (str): Razon de los datos para ser mas personalizable el proceso.
            
            Return:
                Retorna una tupla con un nombre y un keyshort.
        """
        
        name = input(f'Nombre de {peticion}: ').strip()
        keyshort = input(f'Ingresa el keyshort de {name}: ').strip()
        keyshort = FinOb.Starting.FilterKeyshort(keyshort)

        return name, keyshort

def Consult_Starting(name:str = 'Elemento') -> Optional[list]:
    """Consulta si se añadira starting a {name} = 'Elemento'

    Args:
        name (str): Solo se usa para personalizar la petición.

    Return:
        Retorna una lista de keyshorts, o None segun la eleccion.
    """
    while True: 
        consult = input(f"Desea agregar un starting a {name}: ").strip()
        consult = consult.upper()
        
        if consult in ('S', 'SI'):
            str_keyshots = input(f"Escriba el starting de {name}: ").strip()
            return FinOb.Starting.FilterKeyshort(str_keyshots)
        
        elif consult in ('N', 'NO'):
            return None

        input("Opcion no valida!, vuelve a intentar.")
        Clear_Console(lines = 2)

def Clear_Console(lines:int = 1):

    def borrar_ultima_linea():
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')
    
    for _ in range(lines):
        borrar_ultima_linea()
