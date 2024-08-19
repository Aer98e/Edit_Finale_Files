import General_Operation

Wizard = General_Operation.Finale_Wizard()

def Profile_All(Verses_Number:int, Have_Chorus:bool):
    Wizard.Change_Align_Verses(Verses_Number, 'Standar', Adjusting_Chorus=Have_Chorus)
    Wizard.Change_Lyrics_Size('14', Verses_Number, Have_Chorus)
    Wizard.Add_Text_Item('Lyrisist_P', Element='Lyrisist')
    Wizard.Add_Text_Item('Voice_P', Text = 'Voz')
    Wizard.Align_Element('Subtitle', 'Subtitle_M')
    Wizard.Align_Element('Title', 'Title_M')
    Wizard.Align_Element('Author', 'Author_M')
    
