import PySimpleGUI as gui

gui.theme('Dark Amber')
layout = [[gui.Text('Первая лаба, выбираем задачку:')],
          [gui.Button('Первая')],
          [gui.Button('Вторая')],
          [gui.Button('Третья')],
          [gui.Exit('Выход')]]
window = gui.Window('Lab_One.exe', layout)
event, values = window.read()
if event == 'Первая':
    exec(open("RK.py").read())