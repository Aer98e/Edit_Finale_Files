import pyautogui
import General_Operation
import Finale_Objects as FinOb
import time
import New
import Utilities as Util

while(True):
    type_ob = input("Con que objeto trabajaras: ").strip()
    try:
        obj = New.ManagerMyObject(type_ob)
    except ValueError as e:
        input(e)
        continue
    opcion = input("Terminamos?: ").strip()
    opcion = opcion.upper()
    if opcion in ('SI', 'S'):
        break









