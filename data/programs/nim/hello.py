import PySimpleGUI as sg

layout1 = [[sg.Text('Main Menu')],
           [sg.Button('New'), sg.Button('Load')]]
layout2 = [[sg.Text('Positions')],
           [sg.Button('Select'), sg.Button('Back'), sg.Button('Analyze')]]
layout3 = [[sg.Text('Play')],
           [sg.Button('Win'), sg.Button('Lose'), sg.Button('Quit')]]
layout4 = [[sg.Text('Congrats!')],
           [sg.Button('Restart')]]
layout5 = [[sg.Text('Analysis')],
           [sg.Button('Main')]] 
layout = [[sg.Column(layout1, key='-COL1-'),
           sg.Column(layout2, key='-COL2-', visible=False),
           sg.Column(layout3, key='-COL3-', visible=False),
           sg.Column(layout4, key='-COL4-', visible=False),
           sg.Column(layout5, key='-COL5-', visible=False)],
          [sg.Exit('Exit')]]

window = sg.Window('Nim Game', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Load':
        window['-COL1-'].update(visible=False)
        window['-COL2-'].update(visible=True)
    if event == 'Back':
        window['-COL2-'].update(visible=False)
        window['-COL1-'].update(visible=True)
    if event == 'New':
        window['-COL1-'].update(visible=False)
        window['-COL3-'].update(visible=True)
    if event == 'Quit':
        window['-COL3-'].update(visible=False)
        window['-COL1-'].update(visible=True)
    if event == 'Select':
        window['-COL2-'].update(visible=False)
        window['-COL3-'].update(visible=True)
    if event == 'Win':
        window['-COL3-'].update(visible=False)
        window['-COL4-'].update(visible=True)
    if event == 'Lose':
        window['-COL3-'].update(visible=False)
        window['-COL5-'].update(visible=True)
    if event == 'Analyze':
        window['-COL2-'].update(visible=False)
        window['-COL5-'].update(visible=True)
    if event == 'Restart':
        window['-COL4-'].update(visible=False)
        window['-COL1-'].update(visible=True)
    if event == 'Main':
        window['-COL5-'].update(visible=False)
        window['-COL1-'].update(visible=True)

window.close()
