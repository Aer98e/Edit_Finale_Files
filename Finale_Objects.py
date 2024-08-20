import pyautogui
from typing import Literal, Callable, Union, Tuple, Dict
import inspect
import time
import Utilities as Util
from abc import ABC, abstractmethod

pyautogui.PAUSE = 0.4

class Starting:
    @staticmethod
    def FilterKeyshort(keyshorts:str, pack = False) -> Union[str, tuple, list]:
        """Divide un string por '/'
        Args:
            keyshorts (str): String que sera procesado, cada valor debe seperarse por '/'

        Returns:
            Retorna una lista con tuplas y strings.
        """
        if not keyshorts:
            return None

        elif Starting.IsKeyshortList(keyshorts):
            return keyshorts

        elif Starting.IsTupleValid(keyshorts):
            if pack:
                return [keyshorts]
            return keyshorts
        
        elif isinstance(keyshorts, str):
            list_keyshorts=[]
            
            leaked_keyshorts = map(str.strip, keyshorts.split('/'))

            for keyshort in leaked_keyshorts:
                if ',' in keyshort:
                    keyshort = tuple(map(str.strip, keyshort.split(',')))
                list_keyshorts.append(keyshort)  
            
            if len(list_keyshorts) == 1 and not pack:
                return list_keyshorts[0]
            
            return list_keyshorts
        
        else:
            raise TypeError(f'{keyshort} es un argumento no valido')

    @staticmethod
    def Add_Instruction(keyshort:str, list_starting:list) -> None:
        """Añade atajos a una lista.

        Args:
            keyshort (str): Atajos.
            list_starting (list): Lista a la que se agregara los nuevos atajos.
        """
        if isinstance(keyshort, str) and keyshort or Starting.IsTupleValid(keyshort):
            keyshort = Starting.FilterKeyshort(keyshort, pack = True)

        elif Starting.IsKeyshortList(keyshort):
            pass

        else:
            raise ValueError(f'({keyshort}), no es un argumento valido.')
        
        list_starting.extend(keyshort)

    @staticmethod
    def Execute_Instructions(list_starting:list, wait_time:float = 0.2) -> None:
        """Presiona una secuencia de teclas para ejecutan alguna accion.
        
        Args:
            list_starting (list):Lista de atajos de teclado.
            wait-time (float):Tiempo de espera entre instrucciones.
        """
        if Starting.IsKeyshortList(list_starting):
            for instruction in list_starting:
                if isinstance(instruction, str):
                    pyautogui.press(instruction)

                elif isinstance(instruction, tuple):
                    pyautogui.hotkey(instruction)
                time.sleep(wait_time)
        else:
            raise ValueError(f'({list_starting}), no es un argumento valido.')

    @staticmethod
    def IsTupleValid(keyshort:tuple):

        if isinstance(keyshort, tuple):
            return all(isinstance(content, str) for content in keyshort)
        
        return False
    
    @staticmethod
    def IsKeyshort(keyshort:Union[str, tuple]):
        if keyshort and isinstance(keyshort, str) or Starting.IsTupleValid(keyshort):
            return True
        else:
            return False

    @staticmethod
    def IsKeyshortList(keyshorts:list):
        rectifier = False
        
        if isinstance(keyshorts, list):
            # all(Starting.IsKeyshort(element) for element in keyshorts)
            for element in keyshorts:
                rectifier = Starting.IsKeyshort(element)

                if not rectifier:#rectifier == False
                    return rectifier
            
        return rectifier

class BasicElement(ABC):
    c_version = 1

    def __init__(self, name:str, keyshort:Union[str, tuple], starting:list = None, type_ob = 'BASIC') -> None:
        self._name = name
        self._keyshort = keyshort# Starting.FilterKeyshort(keyshort) || quité el filtro por que se supone que no crearemos elementos sin el filtro
        self._starting = [element for element in starting] if starting else []
        self._type_ob = type_ob
        self._version = BasicElement.c_version
        Starting.Add_Instruction(self._keyshort, self._starting) 
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def keyshort(self) -> Union[str, tuple]:
        return self._keyshort
    
    @property
    def starting(self) -> list:
        c_list = [element for element in self._starting]
        return c_list
    
    @property
    def version(self) -> float:
        return self._version

    @property
    def type_ob(self) -> str:
        return self._type_ob

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and new_name:
            self._name = new_name
        else:
            raise ValueError("new_name debe ser de tipo string.")

    @keyshort.setter
    def keyshort(self, new_keyshort):
        if Starting.IsKeyshort(new_keyshort):
            self._keyshort = Starting.FilterKeyshort(new_keyshort)
            self._Update_Starting(key = True)
        else:
            raise TypeError("keyshort_name debe ser de tipo string o tupla.")
    
    @starting.setter
    def starting(self, new_starting):
        key = False
        
        if Starting.IsKeyshortList(new_starting):
            self._starting  = [element for element in new_starting]
            
            if self._starting == ['0']:
                key = True
            
            self._Update_Starting(key = key)
        
        elif not new_starting:
            pass

        else:
            raise ValueError("La lista new_starting debe contener str o tuplas")
    
    @version.setter
    def version(self, new_version:float, passw:int):
        if passw == 9885223 and isinstance(new_version, (int, float)):
            self._version = new_version
        
        else:
            print("ACCESO DENEGADO.")

    def _Update_Starting(self, key:bool) -> None:
        if key and len(self._starting) > 0:
            del self._starting[-1]
        Starting.Add_Instruction(self._keyshort, self._starting)
    
    
    def Show_Basic(self, message = ''):
        description = f'\n**{message.upper()}**' if message else ''
        print(description)
        print("_____________________________")
        print(f"=========== {self._type_ob.upper()} ===========")
        print(f'name:     {self.name}')
        print(f'keyshort: {self.keyshort}')
        print(f'starting: {self.starting}')
        print("______________________________\n")
    
    def Show(self, message = ''):
        self.Show_Basic(message=message)

    def Open(self) -> None:
        """
            Seleciona este item de la lista.
        """    
        Starting.Execute_Instructions(self._starting)

class BasicDictionary:
    def __init__(self):
        self._diccionary = {}

    def __setitem__(self, key, value):
        self._diccionary[key] = value

    def __getitem__(self, key):
        return self._diccionary[key]

    def __delitem__(self, key):
        del self._diccionary[key]

    def __iter__(self):
        return iter(self._diccionary)

    def __len__(self):
        return len(self._diccionary)

    def __contains__(self, key):
        return key in self._diccionary
    
    def pop(self, name:str):
        if isinstance(name, str):
            return self._diccionary.pop(name)
    
    @property
    def diccionary(self):
        return self._diccionary.copy()
    
    @diccionary.setter
    def diccionary(self, new_diccionary:dict):
        if isinstance(new_diccionary, dict):
            self._diccionary = new_diccionary.copy()
        else:
            raise TypeError('El nuevo diccionario no es de un tipo valido.')
        
class ListItem(BasicElement):
    """Clase que representa un item de un IList.
    
    Atributos:
        name (str): Nombre del item.
        keyshort (str | tuple): Atajo de teclado para este item.
        starting (list): Lista de teclas para acceder al item.
    
    Métodos:
        Open(): Ejecuta "starting", para seleccionar este item.
    """

    def __init__(self, name:str, keyshort:Union[str, tuple[str, str]], starting_base:list = None) -> None:
        BasicElement.__init__(self, name, keyshort, starting_base, 'ListItem')
        self.Show()

class IList(BasicElement, BasicDictionary):
    """Clase que representa una lista de Items, funciona como un diccionario.
        
    Atributos:
        name (str): Nombre del item.
        keyshort (str | tuple): Atajo de teclado para este item.
        starting (list): Lista de teclas para acceder al item.
    
    Métodos:
        Open(): Ejecuta "starting", para seleccionar este item.

    """
    def __init__(self, name_l:str, keyshort_l:Union[str, tuple[str, str]], starting_l:list = None) -> None:
        """Construccton de la clase IList.

            Args:
                name_l (str): Nombre de la lista.
                keyshort_l (str | tuple): Atajo para acceder a la lista.
                starting_l (list): Lista de instrucciones para accerder a la lista.

        """
        BasicElement.__init__(self, name_l, keyshort_l, starting_l, 'IList')
        BasicDictionary.__init__(self)
        self.Show()
    
    def Add_Items(self) -> None:
        """Se encarga de cargar elementos a la lista.
        """
        
        print(f"ITEMS PARA {self._name}")
        
        while(True):
            type_item = input(f"\tQue tipo de elemento desea agregar a {self._name}('item' / 'lista')...").strip()
            type_item = type_item.upper()

            if type_item == 'LISTA':
                name, keyshort = Util.Consult_Data(peticion = "Lista")
                element = IList(name, keyshort, self._starting)
                element.Add_Items()
            
            elif type_item == 'ITEM':
                name, keyshort = Util.Consult_Data(peticion = "Item")
                element = ListItem(name, keyshort, self.starting)
            
            else:
                print('Opcion no valida.')
                continue

            self._diccionary[name] = element
            
            control = input(f'\tDesea agregar item más a {self._name}...')
            if control.upper() == 'NO':
                break

    def Show_Items(self):
        print(f"====**ITEMS DE {self.name.upper()}**====")
        for i, (key, value) in enumerate(self.diccionary.items(), 1):
            print(f"{i}) {key} ({value.type_ob}).")
        print()

    def Show(self, message = ''):
        self.Show_Basic(message=message)
        if self.diccionary:
            self.Show_Items()

    def _Update_Starting(self, key: bool) -> None:
        if key:
            del self._starting[-1]
        Starting.Add_Instruction(self._keyshort, self._starting)

        for key in self.diccionary.keys():
            self.diccionary[key].starting = self.starting

# class C_Window:
#     def __init__(self, win_name, method_open:Callable[[], None] ,method_close:Literal['saved', 'close']) -> None:
#         self._name = win_name
#         self._open = method_open
#         self._close = method_close
#         self._dictButtons:dict[str, Button] = {}

#     def Open_Window(self):
#         self._open()

#     def Close_Window(self) -> None:
#         if self._close == 'saved':
#             pyautogui.press('enter')
#         elif self._close == 'close':
#             pyautogui.hotkey('alt','f4')
    
#     def Add_Button(self, name_button:str, coordinates:tuple[int, int], keyshort:Union[str, tuple[str, str]]) -> None:
#         button = Button(name_button, coordinates)
#         button.Change_KeyShort(keyshort)
#         self._dictButtons[name_button] = button

#     def Press_Button(self, name_button:str):
#         self._dictButtons[name_button].Press()

#     def Write_Text(self, text:str) -> None:
#         pyautogui.write(text)
    

class Button(BasicElement):
    """Clase que representa un Boton.
        
    Atributos:
        name (str): Nombre del botón.
        keyshort (str | tuple): Atajo de teclado para este botón.
        coordinates
        starting (list): Lista de teclas para acceder al botón.
    
    Métodos:
        Open(): Ejecuta "starting", para seleccionar este botón.

    """
    def __init__(self, name:str, keyshort:Union[str, tuple], starting:list = None) -> None:
        BasicElement.__init__(self, name, keyshort, starting, 'Button')
        """Constructor de la clase Button.

        Args:
            name (str): Nombre del botón.
            keyshort (str | tuple): Atajo de teclado para este botón.
            starting (list): Lista de teclas para acceder al botón.
        """
        self._coordinates: tuple[int, int] = None
        self._i_list:IList = None
        self.Show()

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, new_coordinates:tuple):
        if isinstance(new_coordinates, tuple):
            if all(isinstance(element, int) for element in new_coordinates):
                self.coordinates = new_coordinates
            else:
                raise ValueError(f"{new_coordinates}, no contiene enteros")
        else:
            raise TypeError(f'{new_coordinates}, no es un argumento valido')

    def Add_IList(self):
        name, keyshort = Util.Consult_Data('Nueva Lista')
        self._i_list = IList(name, keyshort, self.starting)
        self._i_list.Add_Items()

    def Press(self) ->  None:
        """Click el boton."""

        if self._coordinates: 
            pyautogui.click(self._coordinates)
        else:
            raise ValueError("No existen coordenadas")

    def Show(self, message = ''):
        self.Show_Basic(message=message)
        if self._i_list:
            self._i_list.Show()
