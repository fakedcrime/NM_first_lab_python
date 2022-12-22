#coding=windows-1251
import pandas
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import PySimpleGUI as gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

c1 = c2 = 0

def f(x, u1, u2, num):
    a = 3
    b = 4
    if num == 1:
        return u2
    elif num == 2:
        return -a*u2+b*math.sin(u1)

def rk4ForSyst(x, u1, u2, h):
    k11 = f(x, u1, u2, 1)
    k12 = f(x, u1, u2, 2)

    k21 = f(x + 0.5 * h, u1 + 0.5 * h * k11, u2 + 0.5 * h * k12, 1)
    k22 = f(x + 0.5 * h, u1 + 0.5 * h * k11, u2 + 0.5 * h * k12, 2)

    k31 = f(x + 0.5 * h, u1 + 0.5 * h * k21, u2 + 0.5 * h * k22, 1)
    k32 = f(x + 0.5 * h, u1 + 0.5 * h * k21, u2 + 0.5 * h * k22, 2)

    k41 = f(x + 0.5 * h, u1 + 0.5 * h * k31, u2 + 0.5 * h * k32, 1)
    k42 = f(x + 0.5 * h, u1 + 0.5 * h * k31, u2 + 0.5 * h * k32, 2)

    x = x + h
    v1 = u1 + h * (k11 + 2*(k21 + k31) + k41)/6
    v2 = u2 + h * (k12 + 2*(k22 + k32) + k42)/6
    return x,v1,v2

def rk4ForSystWithDblHop(x, u1, u2, h):
    x,v1,v2 = rk4ForSyst(x,u1,u2, 0.5*h)
    x,v1,v2 = rk4ForSyst(x,u1,u2, 0.5*h)
    return x,v1,v2

def rk4ForSystWithCorrectHop(x, u1, u2, h):
    j = h
    j = correctHop(x, u1, u2, e, h)

    k11 = f(x, u1, u2, 1)
    k12 = f(x, u1, u2, 2)

    k21 = f(x + 0.5 * j, u1 + 0.5 * j * k11, u2 + 0.5 * j * k12, 1)
    k22 = f(x + 0.5 * j, u1 + 0.5 * j * k11, u2 + 0.5 * j * k12, 2)
                                                        
    k31 = f(x + 0.5 * j, u1 + 0.5 * j * k21, u2 + 0.5 * j * k22, 1)
    k32 = f(x + 0.5 * j, u1 + 0.5 * j * k21, u2 + 0.5 * j * k22, 2)
                                                        
    k41 = f(x + 0.5 * j, u1 + 0.5 * j * k31, u2 + 0.5 * j * k32, 1)
    k42 = f(x + 0.5 * j, u1 + 0.5 * j * k31, u2 + 0.5 * j * k32, 2)

    x = x + j
    v1 = u1 + j * (k11 + 2*(k21 + k31) + k41)/6
    v2 = u2 + j * (k12 + 2*(k22 + k32) + k42)/6
    return x,v1,v2,j

def lec(u2,w2):
    return w2 - u2

def correctHop(x, u1, u2, e, h):
    x1,w1,w2 = rk4ForSystWithDblHop (x, u1, u2, h)
    x,u1, u2 = rk4ForSyst(x, u1, u2, h)
    
    s = (w2 - u2)/(2**4 - 1)
    lec = s * 2**4
    if abs(s) > e: 
       global c1
       c1 +=1
       return correctHop(x, u1,u2,e,h/2)
    if abs(s) >= e/2**5 and abs(s)<=e:
        return h
    if abs(s) < e/2**5:
        global c2
        c2+=1
        return 2*h
    

x = x1 = x2 = 0
u1 = w1 = v1 = 1
u2 = w2 = v2 = 1
h = 0.1
j = h
_VARS = {'window': False,       #--------------------------------------------- Сюда все варики и ивенты пишем
         'table': False
         }

headers = {'i':[], 'xi':[], 'v(1)i':[], 'v(2)i':[], 'w(1)i':[], 'w(2)i':[], 'u(1)i-w(1)i':[], 'u(2)i-w(2)i':[], 'OLP':[], 'h':[], 'c1':[], 'c2':[]}
headings = list(headers)
table = pandas.DataFrame(columns=headers)
values = table.values.tolist()

layout = [                #--------------------------------------------- Здесь расстановка кнопок и прочего
          [gui.Text('Enter h:')],
          [gui.Input(key='h')],
          [gui.Text('Enter e:')],
          [gui.Input(key='e')],
          [gui.Text('Enter hop count:')],
          [gui.Input(key='hop_count')],
          [gui.Exit('Exit')],
          [gui.Submit('Enter')],
          [gui.Canvas(key='figCanvas')],
          [gui.Table(values = values, headings = headings, key='Table', expand_y=True, auto_size_columns=False, col_widths=list(map(lambda x:len(x)+1, headings)))]
]
e = 0.01
xO = []
xO.append(x)
yO = []
yO.append(u1)
zO = []
zO.append(u2)
maxN = 1001
c11 = c12 = c21 = c22 = 0
lec1 = lec2 = 0
i = 0
# Само окно: |
#            V
_VARS['window'] = gui.Window('First', layout, resizable=True, finalize=True)
# Нужно для рисунка в программе
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', expand=-2)
    return figure_canvas_agg
#
#def draw_table(canvas, table):

# Main loop, здесь основной движ
# |||||||||
# VVVVVVVVV
while True:
    event, values = _VARS['window'].read()
    if event == 'Enter':
        h = float(values['h'])
        e = float(values['e'])
        n = int(values['hop_count'])

        while i < n and i < maxN:
            x, u1, u2 = rk4ForSyst(x, u1, u2, h)
            x1, w1, w2 = rk4ForSystWithDblHop(x1, w1, w2, h)
            x2,v1,v2,j = rk4ForSystWithCorrectHop(x2,v1,v2,h)
            table.loc[i] = [i, x, u1, u2, w1, w2, (u1-w1), (u2-w2), lec(w2, v2), j, c1, c2]  #---------------- Вставляем ряды со значениями в таблицу
            xO.append(x)
            yO.append(u1)
            zO.append(u2)
            i+=1

        Values = table.values.tolist() #--------------------------------------------------------------------Так как таблица создана с помощью библиотеки Pandas, нужно извлечь из нее значения
        gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table'), Values) #-----------------------Подставляем значения в таблицу
        gui.Window.refresh(_VARS['window']) #---------------------------------------------------------------Обновляем окно, чтобы в таблице отобразились данные
        fig1 = plt.figure()
        plt.subplot(1,3,1)
        plt.plot(xO,yO,'r') # x, u ось
        plt.legend(['u', 'x'])
        fig2 = plt.figure()
        plt.subplot(1,3,2)
        plt.plot(xO,zO,'r') # x, u' ось
        plt.legend(['du', 'x'])
        fig3 = plt.figure()
        plt.subplot(1,3,3)
        plt.plot(yO,zO,'r') # фазовое пространство
        plt.legend(['Phase space'])
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig1)           #   <---
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig2)           #   <---  Рисунок
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig3)           #   <---

    if event == gui.WIN_CLOSED or event == 'Exit':
        break


_VARS['window'].close()