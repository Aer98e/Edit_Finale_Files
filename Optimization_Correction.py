import os
import pyautogui
from pynput import mouse, keyboard
import pickle
from typing import Union

def Find_Image_Coordinates(Image_Path:str) -> dict:
    Coordinate={}

    nombre_base, extension = os.path.splitext(os.path.basename(Image_Path))
    if os.path.isfile(Image_Path):
        while True:
            try:
                Image_Coordinate=pyautogui.locateCenterOnScreen(Image_Path, grayscale=True)
                if Image_Coordinate:
                    Coordinate[f'{nombre_base}']=((Image_Coordinate.x, Image_Coordinate.y))
                    return Coordinate
            except pyautogui.ImageNotFoundException:
                pyautogui.confirm(text=f'No se pudo identifica {nombre_base}\nVuelva a intentar.', title='Ayudante', buttons=['OK'])

def Find_FolderImage_Coordinates(Path:str) -> dict:
    Coordinates={}

    Current_Rute=os.getcwd()
    os.chdir(Path)
    for Archivo in os.listdir():
        Coordinates.update(Find_Image_Coordinates(Archivo))
    os.chdir(Current_Rute)
    return Coordinates

def Requester_Click(Order:str, Package:bool = True) -> Union[dict, tuple[int, int]]:
    Coordinates = {}

    def on_click(x, y, button, pressed):
        if pressed:
            Coordinates[Order]=((x, y))
            return False

    pyautogui.confirm(text=f'Haga click en {Order}...', title='Ayudante', buttons=['OK'])
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
    listener.stop()
    if Package:
        return Coordinates
    return Coordinates[Order]

def Requester_List_Click(Order_List:list) -> dict:
    Coordinates = {}

    for Order in Order_List:
        Coordinates.update(Requester_Click(Order))
    return Coordinates

def Motions_Recorder() -> tuple:
    Key_Counter = {'up':0, 'down':0, 'right':0, 'left':0}

    def on_press(key):
        if key == keyboard.Key.enter:
            return False
        try:
            Key_Counter[str(key.name)]+=1
        except:
            pass
    with keyboard.Listener(on_press=on_press) as listener_keyboard:
        listener_keyboard.join()
    
    x = Key_Counter['right']-Key_Counter['left']
    y = Key_Counter['down']-Key_Counter['up']

    return (x, y)

def Saved_Coordinates(Coordinates:dict, Filename:str) -> None:    
    with open(f"{Filename}.coor", "w") as File:
        File.write(str(Coordinates))

def Read_Coordinates(FileName:str) -> dict:
    Coordinates={}

    with open(FileName, "r") as File:
        Coordinates = eval(File.read())
    return Coordinates

def Reset_Coordiantes(Coordinates:dict, Filename:str = "Uselful_coordinates", Keep:bool = True) -> dict:
    Coordinates = Requester_List_Click(list(Coordinates.keys()))
    if Keep:
        Saved_Coordinates(Coordinates, Filename)
    return Coordinates

def Coordinate_Updater(Dict_Coordinates:dict, Key:str):
        message = f'Selecciona {Key} y muevelo hasta el lugar correcto, al terminar preciona enter'
        pyautogui.confirm(text = message, title = 'Asistente', buttons = ['OK'])
        
        Rectificador = Motions_Recorder()
        
        Dict_Coordinates[Key] = (
        Dict_Coordinates[Key][0]+Rectificador[0],
        Dict_Coordinates[Key][1]+Rectificador[1]
        )

def Saved_Object(Ob:object, name:str, path:str):
    if path:
        name=f"{path}/{name}"    
    with open(f'{name}.pkl', 'wb') as file:
        pickle.dump(Ob, file)

def Recover_Object(name:str, type_ob:str, path:str) -> object:#CORREGIR QUE SEA MUY ESPECIFICO
    with open(f'{path}/{type_ob}_{name}.pkl', 'rb') as file:
        Ob = pickle.load(file)
    return Ob

