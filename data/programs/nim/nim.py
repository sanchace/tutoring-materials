import PySimpleGUI as sg
import json
import game
from math import sqrt
from time import sleep

DEBUG = False

MAX_PILES = 20

saved_positions = {
    'demo -- win' : {
        'state' : [3,4,5],
        'hardcore' : True,
    },
    'demo -- loss' : {
        'state' : [1,2,3],
        'hardcore' : True,
    },
}
try:
    with open('nimsaves.json') as f:
        saved_positions.update(json.load(f))
except FileNotFoundError:
    pass

layout1 = [[sg.Text('Main Menu')],
           [sg.Button('New Game', key='1->6'), sg.Button('Positions Menu', key='1->2')]]
layout2 = [[sg.Text('Positions Menu')],
           [sg.Listbox(list(saved_positions.keys()), default_values=[list(saved_positions.keys())[0]], select_mode='LISTBOX_SELECT_MODE_SINGLE', horizontal_scroll=True, size=(50, 15), key='-LIST-'), sg.Button('Delete', key='-DELETE_POSITION-')],
           [sg.Button('Play Position', key='-LOAD_POSITION-'), sg.Button('Analyze Position', key='2->5'), sg.Button('Main Menu', key='2->1')]]
layout3 = [[sg.Text('Play Screen')],
           [sg.Graph((700,500), (0,0), (2048,2048), pad=50, enable_events=True, drag_submits=True, background_color='white', key='-GRAPH-'),
            sg.Button('Take', key='-TAKE-')],
           [sg.Button('Save', key='-TO_SAVE_SCREEN-'), sg.Button('Main Menu', key='3->1')]]
layout4 = [[sg.Text('Congratulations! You won!')],
           [sg.Button('Main Menu', key='4->1')]]
layout5 = [[sg.Text('Game Analysis (coming soon)')],
           [sg.Button('Main Menu', key='5->1')]] 
layout6 = [[sg.Text('Game Parameters')],
           [sg.Checkbox('hardcore', key='-HARDCORE_MODE-'), sg.Text(f'How many piles? (max {MAX_PILES})'), sg.Input(key='-NUM_PILES-'), sg.Button('Submit', key = '-SET_PILES-')]] +\
           [[sg.Text(f'#dots in pile {i}', key=f'-PARAM{i}-', visible=False), sg.Input(0, key=f'-PILE{i}-', visible=False)] for i in range(MAX_PILES)] +\
           [[sg.Button('Play', key='-INIT_NEW_GAME-')]]
layout7 = [[sg.Text('Save Game Screen')],
           [sg.Input('[default game name]', key='-SAVE_NAME-')],
           [sg.Button('Save Game', key='-SAVE_GAME-')]]
layout = [[sg.Column(layout1, key='-COL1-'),
           sg.Column(layout2, key='-COL2-', visible=False),
           sg.Column(layout3, key='-COL3-', visible=False),
           sg.Column(layout4, key='-COL4-', visible=False),
           sg.Column(layout5, key='-COL5-', visible=False),
           sg.Column(layout6, key='-COL6-', visible=False),
           sg.Column(layout7, key='-COL7-', visible=False)],
          [sg.Exit('Exit')]]

window = sg.Window('Nim Game', layout, finalize=True)
#window.maximize()
graph = window['-GRAPH-']

dots = [] #piles of nim tokens in canvas
lines = [] #dividing lines
g = game.Game()

row_selected = None
num_selected = set()

def circle_center(position, row, column):
    x = max(position)
    y = len(position)
    return (int(2048 * ((2 * column + 1) / (2 * x + 1))), int(2048 * ((2 * row + 1) / (2 * y + 1))))

def circle_radius(position):
    return int(1024 / (2 * max(max(position), len(position)) + 1))

def line_coords(position, row, margin):
    h = int(2048 * ((2 * row + 2) / (2 * len(position) + 1)))
    start = (margin, h)
    end = (2048 - margin, h)
    return (start, end)

def redraw(position):
    dots = []
    lines = []
    scale = 128
    graph.erase()
    graph.set_size(size=(int(scale * sqrt(max(g.state))), int(scale * sqrt(len(g.state)))))
    r = circle_radius(position)
    for idx, num in enumerate(position):
        dots.append([graph.draw_circle(circle_center(position, idx, i), r, fill_color='black') for i in range(num)])
    for i in range(len(position)-1):
        start, end = line_coords(position, i, r//2)
        lines.append(graph.draw_line(start, end, width = 8))
    window.refresh()
    if (DEBUG):
        print(dots, lines)
    return dots, lines

while True:
    event, values = window.read()
    if DEBUG:
        print('<Frame>')
        print('GUI STATE:')
        print(f'event: {event}')
        print(f'values: {values}')
        print(f'dots: {dots}')
        print(f'lines: {lines}')
        print('')
        print('GAME STATE:')
        print(f'game state: {g}')
        print(f'g.state value: {g.state}')
        print('</Frame>')
        print('\n')

    if event == sg.WIN_CLOSED or event == 'Exit':
        with open('nimsaves.json', 'w') as f:
            f.write(json.dumps(saved_positions, indent=4))
        break

    if '->' in event:
        x,y = list(map(int, event.rsplit('->')))
        window[f'-COL{x}-'].update(visible=False)
        window[f'-COL{y}-'].update(visible=True)

    if event == '-LOAD_POSITION-':
        if len(saved_positions) != 0:
            selected_position = saved_positions[window['-LIST-'].get()[0]]
            g = game.Game(state=selected_position['state'], hardcore=selected_position['hardcore'])
            window.write_event_value('2->3', None)
            dots, lines = redraw(g.state)

    if event == '-DELETE_POSITION-':
        saved_positions.pop(window['-LIST-'].get()[0])
        window['-LIST-'].update(values=list(saved_positions.keys()))
        if len(saved_positions) != 0:
            window['-LIST-'].set_value([list(saved_positions.keys())[0]])

    if event == '-TO_SAVE_SCREEN-':
        if g.on_move:
            window['-SAVE_NAME-'].update(value=g.__str__())
            window.write_event_value('3->7', None)

    if event == '-SAVE_GAME-':
        saved_positions[window['-SAVE_NAME-'].get()] = {
            'state' : g.state,
            'hardcore' : g.opp.hardcore,
        }
        window['-LIST-'].update(values=list(saved_positions.keys()))
        window['-LIST-'].set_value([list(saved_positions.keys())[0]])
        window.write_event_value('7->1', None)

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
                window.write_event_value('6->3', None)
                # initialize
                ns = [int(window[f'-PILE{i}-'].get()) for i in range(int(window['-NUM_PILES-'].get()))]
                g = game.Game(ns, hardcore=window['-HARDCORE_MODE-'].get())
                # reset state
                dots, lines = redraw(ns)

    if event == '-GRAPH-':
        x, y = values['-GRAPH-']
        position = g.state
        for row, col in [(i,j) for i in range(len(position)) for j in range(position[i])]:
            a, b = circle_center(position, row, col)
            r = circle_radius(position)
            if (x - a) ** 2 + (y - b) ** 2 <= r ** 2:
                if row_selected == None or row == row_selected:
                    row_selected = row
                    num_selected.add(col)
                    graph.delete_figure(dots[row][col])
                    dots[row][col] = graph.draw_circle((a, b), r, fill_color='gray')
                else:
                    dots, lines = redraw(position)
                    row_selected = row
                    num_selected = set()
                    num_selected.add(col)
                    graph.delete_figure(dots[row][col])
                    dots[row][col] = graph.draw_circle((a, b), r, fill_color='gray')

    if event == '-TAKE-':
        if row_selected != None and len(num_selected) > 0:
            g.take(game.Move(row_selected, len(num_selected)))
            if g.over():
                window.write_event_value('3->4', None)
            else:
                row_selected = None
                num_selected = set()
                redraw(g.state)
                # indicate the that computer is playing now
                thinking = graph.draw_text("Computer thinking...", (1024, 1024), color='red', text_location=sg.TEXT_LOCATION_CENTER)
                window.refresh()
                sleep(1)
                graph.delete_figure(thinking)
                g.update()
                if g.over():
                    window.write_event_value('3->5', None)
                else:
                    dots, lines = redraw(g.state)

window.close()
