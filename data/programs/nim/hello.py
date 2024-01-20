import PySimpleGUI as sg
import game
from math import sqrt

MAX_PILES = 20

layout1 = [[sg.Text('Main Menu')],
           [sg.Button('New Game', key='1->6'), sg.Button('Positions Menu', key='1->2')]]
layout2 = [[sg.Text('Positions Menu')],
           [sg.Button('Select Position', key='2->3'), sg.Button('Analyze Position', key='2->5'), sg.Button('Main Menu', key='2->1')]]
layout3 = [[sg.Text('Play Screen')],
           [sg.Graph((700,500), (0,0), (2048,2048), pad=50, enable_events=True, drag_submits=True, background_color='white', key='-GRAPH-'),
            sg.Button('Take', key='-TAKE-')],
           [sg.Button('Win', key='3->4'), sg.Button('Lose', key='3->5'), sg.Button('Main Menu', key='3->1')]]
layout4 = [[sg.Text('Congrats!')],
           [sg.Button('Main Menu', key='4->1')]]
layout5 = [[sg.Text('Analysis')],
           [sg.Button('Main Menu', key='5->1')]] 
layout6 = [[sg.Text('Game Parameters')],
           [sg.Text(f'How many piles? (max {MAX_PILES})'), sg.Input(key='-NUM_PILES-'), sg.Button('Submit', key = '-SET_PILES-')]] +\
           [[sg.Text(f'#dots in pile {i}', key=f'-PARAM{i}-', visible=False), sg.Input(0, key=f'-PILE{i}-', visible=False)] for i in range(MAX_PILES)] +\
           [[sg.Button('Play', key='-INIT_NEW_GAME-')]]
layout = [[sg.Column(layout1, key='-COL1-'),
           sg.Column(layout2, key='-COL2-', visible=False),
           sg.Column(layout3, key='-COL3-', visible=False),
           sg.Column(layout4, key='-COL4-', visible=False),
           sg.Column(layout5, key='-COL5-', visible=False),
           sg.Column(layout6, key='-COL6-', visible=False)],
          [sg.Exit('Exit')]]

window = sg.Window('Nim Game', layout, finalize=True)
#window.maximize()
graph = window['-GRAPH-']

dots = [] #piles of nim tokens in canvas
lines = [] #dividing lines
g = game.Game()

while True:
    event, values = window.read()
    print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if '->' in event:
        x,y = list(map(int, event.rsplit('->')))
        window[f'-COL{x}-'].update(visible=False)
        window[f'-COL{y}-'].update(visible=True)

    if event == '-SET_PILES-':
        n = window['-NUM_PILES-'].get()
        if n.isdigit():
            n = int(n)
            if n > 0 and n < MAX_PILES:
                visibility = True
                for i in range(MAX_PILES):
                    if i == n:
                       visibility = False 
                    window[f'-PARAM{i}-'].update(visible=visibility)
                    window[f'-PILE{i}-'].update(visible=visibility)

    if event == '-INIT_NEW_GAME-':
        n = window['-NUM_PILES-'].get()
        if n.isdigit():
            n = int(n)
            valid_state = True
            for i in range(n):
                m = window[f'-PILE{i}-'].get()
                if m.isdigit():
                    m = int(m)
                    valid_state = valid_state and m > 0
                else:
                    valid_state = False
            if valid_state:
                window['-COL6-'].update(visible=False)
                window['-COL3-'].update(visible=True)

                scale = 128
                ns = [int(window[f'-PILE{i}-'].get()) for i in range(int(window['-NUM_PILES-'].get()))]
                g = game.Game(ns)
                x = max(ns)
                y = len(ns)
                r = int(1024 / (2 * max(x,y) + 1))
                graph.erase()
                graph.set_size(size=(int(scale * sqrt(x)), int(scale * sqrt(y))))
                for idx, num in enumerate(ns):
                    dots.append([graph.draw_circle((int(2048 * ((2 * i + 1) / (2 * x + 1))),
                                                    int(2048 * ((2 * idx + 1) / (2 * y + 1)))),
                                                    r, fill_color='black') for i in range(num)])
                for i in range(y-1):
                    margin = r//2
                    h = int(2048 * ((2 * i + 2) / (2 * y + 1)))
                    start = (margin, h)
                    end = (2048 - margin, h)
                    w = 8
                    lines.append(graph.draw_line(start, end, width = w))

window.close()
