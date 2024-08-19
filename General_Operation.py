import os
import pyautogui
from typing import Literal, Optional
import time
import Finale_Controler
import Optimization_Correction as Op
import Finale_Objects as Ar

pyautogui.PAUSE = 0.4

class Finale_Wizard:
    Wait_Time = 0.3

    def Open_File(File_Path:str, Wait_Time:int) -> None:
        os.startfile(File_Path)
        time.sleep(Wait_Time)

    def Set_Standard_Guides(self) -> None:
        def New_Guide(Rule:str):
            pyautogui.click(self.Rule_C[Rule], button='right')
            pyautogui.press(self.Rule_KeyShort['New_Guide'])
        
        def Set_Guides(Guides_Positions:list, Rule:str):
            for Guide in Guides_Positions:
                New_Guide(Rule)
                pyautogui.write(str(Guide))
                pyautogui.press('enter')
        
        View.Select_Option(['Show', 'Rulers'])
        Set_Guides(self.HORIZONTAL_GUIDES,'Horizontal_Rule')
        Set_Guides(self.VERTICAL_GUIDES,'Vertical_Rule')

    def Add_Text_Item(self, Key:str, Element:str = None, Text:str = None, Correction_Mode:bool = False) -> Optional[dict]:
        
        def Add_Item(coordinate:tuple, alignment:str, element:str = None, text:str = None):
            pyautogui.press('pageup')
            Ar.Text_Tool.Activate()
            pyautogui.doubleClick(coordinate)
            pyautogui.write(text) if text else Text_Tool.tab.Select_Option(['Insert', element])
            Ar.Text_Tool.tab.Option(['Alignment', alignment])
        
        Add_Item(self.Add_Items_Text_C[Key], 'Position_From_Page_Edge', Element, Text)
        
        if Correction_Mode:
            self.Add_Items_Text_C.update(Op.Coordinate_Updater(self.Add_Items_Text_C, Key))
            
    def Change_Align_Verses(self ,Number_Verses:int, Profile:Literal['Standar', 'Bajo', 'Director'], Enumerate_Lyrics:bool=True, Adjusting_Chorus:bool = False) -> None:
        Value_Verses = self.ALIGNMENT_CONSTANT[Profile][0]
        Value_Choir = self.ALIGNMENT_CONSTANT[Profile][1]

        Ar.Lyrics_Tool.Activate()
        
        if Enumerate_Lyrics:
            Ar.Lyrics_Tool.tab.Option(['Auto_Number', 'Verse'])

        Finale_Controler.Specify_Current_Lyrics('Type_Verse','1')    

        for i in range(Number_Verses):
            pyautogui.write(str(i+1))
            pyautogui.press('tab')
            pyautogui.write(str(Value_Verses[i]))
            pyautogui.hotkey('shift', 'tab')
        
        if Adjusting_Chorus:
            pyautogui.hotkey('shift', 'tab')
            pyautogui.press(self.General_KeyShort['Chorus'])
            pyautogui.press('tab')
            for i in range(2):
                pyautogui.write(str(i+1))
                pyautogui.press('tab')
                pyautogui.write(str(Value_Choir[i]))
                pyautogui.hotkey('shift', 'tab')
        pyautogui.press('enter')

    def Align_Element(self, Coordinate_Key:str, Coordinates_Key_Move:str, Safe_Mode:bool = True, Correction_Mode:bool = False) -> Optional[dict]:
        pyautogui.press('pageup')
        pyautogui.click(self.Tools_C['Selection_Tool'])

        if Safe_Mode:
            self.Elements_C.update(Op.Requester_Click(Coordinate_Key))

        pyautogui.click(self.Elements_C[Coordinate_Key])
        pyautogui.dragRel(
            self.Add_Items_Text_C[Coordinates_Key_Move][0],
            self.Add_Items_Text_C[Coordinates_Key_Move][1],
            duration=0.3
        )

        self.Change_Size_Element('Subtitle', '12')

        if Correction_Mode:
            self.Add_Items_Text_C.update(Op.Coordinate_Updater(self.Add_Items_Text_C, Coordinates_Key_Move))

    def Eraser_Other_Instruments(self, Voice_Select:Literal['Soprano', 'Director', 'Alto',
    'Tenor', 'Clarinete', 'Bajo'], Wait_Time:float=0.5, Down_Octave:bool=False) -> None:

        Instrument_Voice = {'Soprano': 1, 'Director': 1, 'Alto': 2, 'Tenor': 3, 'Clarinete' : 3, 'Bajo': 4}
        
        Finale_Controler.Open_ScoreManager()

        for i in range(Instrument_Voice[Voice_Select]-1):#Esto funcionara mientras sean 4 intrumentos
            pyautogui.click(self.ScoreManager_Controls_C['Eliminar_Primero'])
            time.sleep(Wait_Time)
        for i in range(4 - Instrument_Voice[Voice_Select]):
            pyautogui.click(self.ScoreManager_Controls_C['Eliminar_Segundo'])
            time.sleep(Wait_Time)
        
        if Voice_Select=='Clarinete':
            pyautogui.click(self.ScoreManager_Controls_C['Instrument_Selector'])
            pyautogui.press('tab')
            pyautogui.press(self.ScoreManager_KeyShort['Woodwinds'])
            pyautogui.press('tab')
            pyautogui.press(self.ScoreManager_KeyShort['Clarinet'])
            pyautogui.press('enter')
            time.sleep(Wait_Time)
            if Down_Octave:
                pyautogui.click(self.ScoreManager_Controls_C['Clef_Type'])
                pyautogui.click(self.ScoreManager_Controls_C['Clef_OctB'])
        pyautogui.hotkey('alt', 'f4')

    def Change_Lyrics_Size(self, Size:Literal['14', '18'], Verses:int, Have_Chorus:bool):
        Sizes={'14':1, '18':8}
        pyautogui.click(self.Tools_C['Lyrics_Tool'])
        Finale_Controler.Open_Lyrics_Window()
        for i in range(Verses):
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Lyric'])
            pyautogui.press(self.General_KeyShort['Verse'])
            pyautogui.press('tab')
            pyautogui.write(str(i+1))
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Select_All'],interval=self.Wait_Time)
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Text'])
            pyautogui.press(self.LyricsWinsdow_KeyShort['Size'])
            pyautogui.press(str(Sizes[Size]))
            if Size == '18':
                pyautogui.press(str(Sizes[Size]))
                pyautogui.press('enter')
            time.sleep(self.Wait_Time)
            
        if Have_Chorus:
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Lyric'])
            pyautogui.press(self.General_KeyShort['Chorus'])
            pyautogui.press('tab')
            pyautogui.write('2')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Select_All'], interval=self.Wait_Time)
            pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Text'])
            pyautogui.press(self.LyricsWinsdow_KeyShort['Size'])
            pyautogui.press(str(Sizes[Size]))
            if Size == '18':
                pyautogui.press(str(Sizes[Size]))
                pyautogui.press('enter')
            time.sleep(self.Wait_Time)
        pyautogui.hotkey('alt', 'f4')

    def Change_Size_Element(self, Element:Literal['Title', 'Author', 'Subtitle'], Size:Literal['12', '14'], Foolproof:bool = False) -> None:
        Sizes = {'12': '2', '14': '1'}
        if Foolproof:
            Current_Position = Op.Requester_Click(Element)[Element]
        else:
            Current_Position = (
            self.Elements_C[Element][0]+self.Add_Items_Text_C[f'{Element}_M'][0],
            self.Elements_C[Element][1]+self.Add_Items_Text_C[f'{Element}_M'][1]
            )
        time.sleep(self.Wait_Time)
        pyautogui.click(self.Tools_C['Selection_Tool'])
        pyautogui.doubleClick(Current_Position)
        pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Select_All'], interval=self.Wait_Time)
        pyautogui.hotkey(self.LyricsWinsdow_KeyShort['Text'])
        pyautogui.press(self.LyricsWinsdow_KeyShort['Size'])
        pyautogui.press(Sizes[Size])
