import Optimization_Correction as Op
import Finale_Objects as FinOb
import glob
import os
import pickle
from typing import Union, Literal
import Utilities as Util
import pyautogui

dict_Tools = {}
dict_Tab = {}

class ObjectFinder:
    @staticmethod
    def File_Finder(path:str, name:str):
        """Busca archivos con parte de un nombre en un directorio.

        Args:
            path (str): Directorio donde se buscara los archivos.
            name (str): Nombre parcial para buscar los archivos.

        Return:
            Una lista con las direcciones de los archivos encontrados.
        """
        return glob.glob(f'{path}/*{name}*')

    @staticmethod
    def Clear_FilePath(file_path:str):
        """ Limpia las direccion de un archivo.

        Args:
            file_path (str): Direccion completa de un archivo.

        Return:
            Un str con solo el nombre del archivo.

        """
        return os.path.basename(file_path)
    
    @staticmethod
    def Remove_FileExtension(file_name:str):
        """Quita la extension del nombre de un archivo.

        Args:
            file_name (str): Solo el nombre de un archivo.
        
        Return:
            Un str con el nombre de un archivo sin su exteción.
        
        """
        return os.path.splitext(file_name)[0]
    
    @staticmethod
    def Clear_FileName(file:str): 
        """Limpia el nombre de un archivo de my_object.

        Los objetos guardados tienen un nombre: '[TYPE OBJECT]_[NAME OBJECT]'
        la funcion retorna solo el NAME OBJECT.

        Args:
            file (str): Nombre del archivo sin la extensión.

        Return:
            Un str con el nombre del objeto del archivo.
        """

        return file.split('_')[1].strip()
    
    @staticmethod
    def Show_ObjectsSaved(path:str, type_ob:Literal['IList', 'Button']):
        """Imprime en pantalla los nombres de un typo de objeto especifico guardado en un directorio.

        Busca en un directorio un tipo de objeto y luego lipia sus nombres para solo obtener el nombre dl objeto y mostrarlo en la pantalla.

        Args:
            path (str): Directorio donde se realizara la busqueda.
            type_ob (str): Tipo de objeto buscado.
        
        """

        lista_ob = ObjectFinder.File_Finder(path, f'{type_ob}_')
        if not lista_ob:
            raise ValueError(f"No se encontro ningun archivo de tipo {type_ob}")
        lista_ob = list(map(ObjectFinder.Clear_FilePath, lista_ob))
        lista_ob = list(map(ObjectFinder.Remove_FileExtension, lista_ob))
        lista_ob = list(map(lambda file: ObjectFinder.Clear_FileName(file), lista_ob))
        
        for num, name in enumerate(lista_ob, 1):
            print(f'{num}) {name}')
        
        return lista_ob
    
    @staticmethod
    def Select_Object(path:str, type_ob:Literal['IList', 'Button']):
        """Muestra una lista de objetos de un tipo especifico y pide un nombre que sera retornado.
        
        Para interaccion con un usuario que quiera pedir un tipo de objeto especifico.

        Args:
            path (str): Directorio donde se realizara la busqueda de los objetos.
            type_ob (str): Typo de objeto buscado.

        Return:
            (str): Nombre de uno de los objetos (ingresado por el usuario).
        """
        lista_ob = ObjectFinder.Show_ObjectsSaved(path, type_ob)
        
        while(True):
            name = input(f"Nombre de {type_ob}: ").strip()
            if name in lista_ob:
                return name
            else:
                print("Este nombre no corresponde a uno de los objetos mostrados.")
                input("vuelva a intentar.")
                Util.Clear_Console(lines = 3)

pathMyOb = 'Utilities_Objects'
class Menu:
    @staticmethod
    def Main_Menu(name_object:str) -> None:
            print("")
            print("_________________________________________________________")
            print("")
            print(f"================MANAGER {name_object}=====================")
            print("")
            print(f"    1) Crear {name_object}    (c).")
            print(f"    2) Editar {name_object}   (e).")
            print(f"    3) Eliminar {name_object} (d).")
            print("")

    @staticmethod
    def Ask_OptionMenu(options: tuple) -> Union[str, int]: 
        while True:
            mode = input("Que desea hacer: ").strip()

            if mode not in options:#('c', 'e', 'd', 1, 2, 3)
                input('Opcion invalida. Vuelve a intentar')
                Util.Clear_Console(lines = 2)
                continue

            break

        return mode
    

def Saved_MyObject(myobject:object , type_ob:Literal['IList', 'Button'], path:str) -> None:
    current_path = os.getcwd()
    path_objects = path
    name = myobject.name
    name = f"{type_ob}_{name}"
    
    if not os.path.exists(path_objects):
        os.mkdir(path_objects)
    os.chdir(path_objects)
    
    Op.Saved_Object(myobject, name, "")
    os.chdir(current_path)

class ManagerMyObject:
    def __init__(self, type_ob: Literal['IList', 'Button']) -> None:
        if type_ob not in ('IList', 'Button', 'ListItem'):
            raise ValueError(f"No se admite {type_ob}, como objeto valido.")
        self.type_ob = type_ob

        Menu.Main_Menu(type_ob)
        mode = Menu.Ask_OptionMenu(('c', 'e', 'd', '1', '2', '3'))
        
        self.Start(mode)
    
    def Start(self, mode:str):
        if mode in ('c', '1'):
            self.Create_MyObject()

        elif mode in ('e', '2'):
            self.Edit_MyObject()

        elif mode in ('d', '3'):
            self.Delete_MyObject()
        
    def Create_MyObject(self):
        print("\n_________________________________________________________")
        print(f"========== CREAR {self.type_ob.upper()}==========")
        name, keyshort = Util.Consult_Data(f"Nueva {self.type_ob}")
        starting = Util.Consult_Starting(name = name)

        my_object = ManagerMyObject._InPrss_Create(self.type_ob, name, keyshort, starting)

        Saved_MyObject(my_object, self.type_ob, pathMyOb)
        print('______________________________')
        print(f'Se creo {self.type_ob}: {name}')
        print('______________________________')

    def Edit_MyObject(self):
        
        print("\n_________________________________________________________")
        print(f"===========EDITAR {self.type_ob.upper()}===========")

        name = ObjectFinder.Select_Object(pathMyOb, self.type_ob)
        my_object = Op.Recover_Object(name, self.type_ob, pathMyOb)
        
        n_update = ManagerMyObject.Confirm_Version(my_object)
        
        if n_update == 'Update':
            c_update = input(f'Desea actualizar {my_object.name}...')
            if c_update.upper() in ('S, SI, Y, YES'):
                my_object = ManagerMyObject.Update_MyObjects(my_object)
         
        elif n_update == 'Obsolete':
            input()
            return False
        
        # if self.type_ob == 'ListItem':
        #     ManagerMyObject.Edit_Item(my_object)

        my_object.Show()
        
        ManagerMyObject._InPrss_Delete(my_object.type_ob, name)
        Saved_MyObject(my_object, my_object.type_ob, pathMyOb)

    def Delete_MyObject(self):
        print("\n_________________________________________________________")
        print(f"===========ELIMINAR {self.type_ob.upper()}===========")
        name = ObjectFinder.Select_Object(pathMyOb, self.type_ob)
        ManagerMyObject._InPrss_Delete(self.type_ob, name)
        print('________________________________')
        print(f'Se eliminó {self.type_ob}:{name}')
        print('________________________________')

    @staticmethod
    def _InPrss_Create(type_ob:str, name:str, keyshort:Union[str, tuple], starting:list, complete : True) -> object:
        my_object = FinOb.__dict__[type_ob](name, keyshort, starting)
        
        if not complete:
            return my_object
        
        if type_ob == 'ListItem':
            pass
        
        elif type_ob == 'IList':
            my_object.Add_Items()
            
        elif type_ob == 'Button':            
            option = input('Agregar lista(si, no): ').strip()
            if option.upper() == 'SI':
                my_object.Add_IList()
        
        return my_object
    
    @staticmethod
    def _InPrss_Delete(type_ob:str, name:str):
        file_name = f'{pathMyOb}/{type_ob}_{name}.pkl'
        os.remove(file_name)

    @staticmethod
    def Confirm_Version( my_object):
        try:
            current_version = FinOb.BasicElement.c_version
            if my_object.version < current_version:
                print('\n==========OBJETO DESACTUALIZADO==========')
                print(f'Version de {my_object.name}: {my_object.version}')
                print(f'Version actual: {current_version}\n')
                return('Update')
            return('Pass')
            #Se supone que nunca existira una version menor a la del objeto.
        except:
            print('\n=============== ERRROR ==================')
            print('El objeto no tiene version, esta desfasado.')
            print('No se puede trabajar con este objeto.\n')
            return 'Obsolete'
    
    @staticmethod
    def Update_MyObjects(old_object):
        name = old_object.name
        keyshort = old_object.keyshort
        starting = old_object.starting[:-1]
        type_ob = old_object.type_ob

        new_object = ManagerMyObject._InPrss_Create(type_ob, name, keyshort, starting, complete = False)

        if type_ob == 'IList':
            diccionary = old_object.diccionary
            for key, value in diccionary.items():
                value = ManagerMyObject.Update_MyObjects(value)
                new_object.diccionary[key] = value

        elif type_ob == 'Button':
            if old_object._i_list:
                i_list = ManagerMyObject.Update_MyObjects(old_object._i_list)
                new_object._i_list = i_list
        
        return new_object
    @staticmethod
    def Edit_Item(item:FinOb.ListItem):
        item.Show (message = 'Valores iniciales')
        
        n_name = input('Ingrese el nuevo nombre: ').strip()
        n_keyshort = input('Ingrese el nuevo keyshort: ').strip()
        n_starting = input('Ingrese el nuevo starting: ').strip()
        
        n_keyshort = FinOb.Starting.FilterKeyshort(n_keyshort)
        n_starting = FinOb.Starting.FilterKeyshort(n_starting, pack = True)

        item.name = n_name if n_name else item.name
        item.keyshort = n_keyshort if n_keyshort else item.keyshort
        item.starting = n_starting if n_starting else item.starting[:-1]
        
        item.Show (message = "Valores actualizados")
    


