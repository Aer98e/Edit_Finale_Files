import pyautogui
from typing import Literal
import Finale_Objects as FinOb

Keyboard_Shortcuts={'Verse':'v','Chorus':'c', 'Section':'s','Auto_Number':'u', 'Specify_Current_Lyrics':'s',
                    'Adjust_Baselines':'b', 'Insert':'i', 'Lyrisist':'l','Alignment':'a', 'Position_From_Page_Edge':'e', 'Show':'h', 'Rulers':'u', 'ScoreManager':('ctrl', 'k'), 'Lyrics_Window':('ctrl', 'l'), 'Tab_Lyric':('alt','y'), 'Tab_Text':('alt', 'x'), 'Tab_View':('alt', 'v')}

pyautogui.PAUSE = 0.2

def Open_Tab_Lyrics() -> None:
    pyautogui.hotkey(Keyboard_Shortcuts['Tab_Lyric'])
    
def Open_Tab_Text() -> None:
    pyautogui.hotkey(Keyboard_Shortcuts['Tab_Text'])

def Open_ScoreManager() -> None:
    pyautogui.hotkey(Keyboard_Shortcuts['ScoreManager'])

def Open_Lyrics_Window() -> None:
    pyautogui.hotkey(Keyboard_Shortcuts['Lyrics_Window'])

def Show_Rules() -> None:
    pyautogui.hotkey(Keyboard_Shortcuts['Tab_View'])
    pyautogui.press(Keyboard_Shortcuts['Show'])
    pyautogui.press(Keyboard_Shortcuts['Rulers'])

def Auto_Number(Element:Literal['Verse', 'Chorus', 'Section']) -> None:
    Open_Tab_Lyrics()
    pyautogui.press(Keyboard_Shortcuts['Auto_Number'])
    pyautogui.press(Keyboard_Shortcuts[Element])

def Specify_Current_Lyrics(Option:Literal['Type_Verse','Type_Chorus', 'Type_Section'], Number:str) -> None:
    Ar.Specify_Current_Lyric.Open()
    Ar.Specify_Current_Lyric.Option(Option)
    Ar.Specify_Current_Lyric.Option('Number')
    Ar.Specify_Current_Lyric.Write_Text(Number)

def Open_Adjust_Baselines() -> None:
    Open_Tab_Lyrics()
    pyautogui.press(Keyboard_Shortcuts['Adjust_Baselines'])
    
def Insert(Element:str='Lyrisist') -> None:#AUN NO ESTA OPTIMIZADO PARA INSERTAR OTROS ELEMENTOS
    Open_Tab_Text()
    pyautogui.press(Keyboard_Shortcuts['Insert'])
    pyautogui.press(Keyboard_Shortcuts[Element])

def Alignment(Position:str='Position_From_Page_Edge') -> None:#AUN NO ESTA OPTIMIZADO PARA INSERTAR OTRAS POSICIONES
    Open_Tab_Text()
    pyautogui.press(Keyboard_Shortcuts['Alignment'])
    pyautogui.press(Keyboard_Shortcuts[Position])