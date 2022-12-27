# -*- coding: utf-8 -*-
import PySimpleGUI as gui
import imp



gui.theme('Dark Amber')
_VARS = {'window': False}
layout = [[gui.Text('Первая лаба, выбираем задачку:')],
          [gui.Button('Первая')],
          [gui.Button('Вторая')],
          [gui.Button('Третья')],
          [gui.Exit('Выход')]]
_VARS['window'] = gui.Window('Lab_One.exe', layout, resizable=True, finalize=True)
while True:
    event, values = _VARS['window'].read()
    if event == 'Третья':
        #exec(open("OpenLab.py").read())
        import OpenLab
        imp.reload(OpenLab)
        #gui.Window.read(_VARS['window'])
    if event == 'Первая':
        #exec(open("NMfirstLab1.py").read())
        import NMfirstLab1
        imp.reload((NMfirstLab1))
        #gui.Window.read(_VARS['window'])
    if event == 'Вторая':
        #exec(open("Lab_1_NM_second_task.py").read())
        import Lab_1_NM_second_task
        imp.reload((Lab_1_NM_second_task))
        #gui.Window.read(_VARS['window'])
    if event == gui.WIN_CLOSED or event == 'Выход':
        break
_VARS['window'].close()