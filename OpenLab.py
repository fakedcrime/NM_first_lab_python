import numpy as np
import matplotlib.pyplot as plt
import math
import random
from tabulate import tabulate
import PySimpleGUI as gui
import pandas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#print("Введите правую границу вычислений по времени")
#print("b=",end="")
maxN=100000
#b=float(input())
text = ""
def max(a,b):
    if a>b:
        return a
    else:
        return b

#print("Введите параметр ε" )
#e=float(input())
#print("Введите шаг")
#h1=float(input())
def f(x, u1, u2, num):  
    a = 3
    b = 4
    if num == 1:
        return u2
    elif num == 2:
        return -a*u2+b*math.sin(u1)
def rk4ForSyst(x, u1, u2,h):
    k11 = f(x, u1, u2, 1)
    k12 = f(x, u1, u2, 2)

    k21 = f(x + 0.5 * h, u1 + 0.5 * h * k11, u2 + 0.5*h * k12, 1,)
    k22 = f(x + 0.5 * h, u1 + 0.5*h * k11, u2 + 0.5 * h * k12, 2,)

    k31 = f(x + 0.5 * h, u1 + 0.5 * h * k21, u2 + 0.5*h * k22, 1)
    k32 = f(x + 0.5 * h, u1 + 0.5*h * k21, u2 + 0.5 * h * k22, 2)

    k41 = f(x + h, u1 + h * k31, u2 + h * k32, 1)
    k42 = f(x + h, u1 + h * k31, u2 + h * k32, 2)

    x = x + h
    v1 = u1 + h * (k11 + 2*(k21 + k31) + k41)/6
    v2 = u2 + h * (k12 + 2*(k22 + k32) + k42)/6
    return x,v1,v2
def rk4ForSystWithDblHop(x, u1, u2, h):
    x,v1,v2 = rk4ForSyst(x,u1,u2, 0.5*h)
    x,v1,v2 = rk4ForSyst(x,v1,v2, 0.5*h)
    return x,v1,v2
def correctHop(x, u1, u2, e, h):
    x1,w1,w2 = rk4ForSystWithDblHop(x, u1, u2, h)
    x,u1, u2 = rk4ForSyst(x, u1, u2, h)
    
    s = ((((u2-w2)**2)+((u1-w1)**2))**0.5)/15
    #lec = s * 2**4
    if abs(s) > e: 

       return correctHop(x, u1,u2,e,h/2)
    #if abs(s) >= e/(2**5) and abs(s)<=e:
      #  return h
    if abs(s) <= e:

        return h
def Correct2Hop(x, u1, u2, e, h):
    x1,w1,w2 = rk4ForSystWithDblHop(x, u1, u2, h)
    x,u1, u2 = rk4ForSyst(x, u1, u2, h)
    s = ((((u2-w2)**2)+((u1-w1)**2))**0.5)/15
    if abs(s)<=e/(2**5):
        return 2*h
    else: 
        return h
def rk4ForSystWithCorrectHop(x, u1, u2, h):
    #j = h
    j = correctHop(x, u1, u2, e, h)

    k11 = f(x, u1, u2, 1)
    k12 = f(x, u1, u2,2)

    k21 = f(x + 0.5 * j, u1 + 0.5 * j * k11, u2 + 0.5 * j * k12, 1)
    k22 = f(x + 0.5 * j, u1 + 0.5 * j * k11, u2 + 0.5 * j * k12, 2)
                                                        
    k31 = f(x + 0.5 * j, u1 + 0.5 * j * k21, u2 + 0.5 * j * k22, 1)
    k32 = f(x + 0.5 * j, u1 + 0.5 * j * k21, u2 + 0.5 * j * k22, 2)
                                                        
    k41 = f(x + j, u1 + j * k31, u2 + j * k32, 1)
    k42 = f(x + j, u1 + j * k31, u2 + j * k32, 2)

    x = x + j
    v1 = u1 + j * (k11 + 2*(k21 + k31) + k41)/6
    v2 = u2 + j * (k12 + 2*(k22 + k32) + k42)/6
    j=Correct2Hop(x, u1, u2, e, j)
    return x,v1,v2,j

def Total(x0,u0,v0,h):
    xO = []
    xO.append(x0)
    yO = []
    yO.append(u0)
    zO = []
    zO.append(v0)
    y1=[]
    y1.append(u0)
    z1=[]
    z1.append(v0)
    y2=[]
    y2.append(u0)
    z2=[]
    z2.append(v0)
    #maxN = 1001
    i = 0
    Table=[]
    C1=0
    C2=0
    minh=h
    maxh=correctHop(x0,u0,v0,e,h)
    maxS=0
    minS=1
    q1=0
    q2=0
    Table=[[0,correctHop(x0,u0,v0,e,h),x0,u0,v0,"","","",0,0]]
    while xO[i] < b and i < maxN:
        H=correctHop(x0,u0,v0,e,h)
        x, u1, u2 = rk4ForSyst(x0,u0,v0,H)
      
        x1, w1, w2 = rk4ForSystWithDblHop(x0,u0,v0,H)
        x0,u0,v0,j = rk4ForSystWithCorrectHop(x0,u0,v0,h)
       
        if j>h:
            C2+=1
        if j<h:
            C1+=1
        h=j
        if j>=maxh:
            maxh=j
            q1=xO[i]
        if j<=minh:
            minh=j
            q2=xO[i]   
        # print(i,") ","(xi:",x," v(1)i:",u1," v(2)i:",u2)
        #print(tabulate([i,x,u1,u2],["i","x","u","v"],tablefmt="fancy_grid"))
        S=abs(((u2-w2)**2+(u1-w1)**2)**(0.5))*16/15
        if S>maxS:
            maxS=S
        if S<minS:
            minS=S
    
        if x0>b:
            del xO[len(xO)-1]
            del yO[len(yO)-1]
            del zO[len(zO)-1]
            del y1[len(y1)-1]
            del z1[len(z1)-1]
            del y2[len(y1)-1]
            del z2[len(z2)-1]
            break
        else:
            xO.append(x0)
            yO.append(u0)
            zO.append(v0)
            y1.append(w1)
            z1.append(w2)
            y2.append(u1)
            z2.append(u2) 
        i+=1
        Table.append([i,j,xO[i],yO[i],zO[i],y2[i],z2[i],S,C1,C2]) 
    d=b-Table[len(Table)-1][2]
    return xO,yO,zO,Table,maxh,minh,q1,q2,S,d,maxS,minS

    
def reference():
    T=Total(0,1,1,h1)
    text = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    text[0] = "              Справка:              "
    text[1] = " Метод Рунге-Кутта 4 порядка"
    text[2] = " начальный шаг: ", h1
    text[3] = "Nmax=",maxN
    text[4] = "x0=0", "  u0=7.5","   v0=0"
    text[5] = "b=",b
    text[6] = "N=",len(T[0])
    text[7] = "b-xn",b-T[3][len(T[3])-1][2]
    text[8] = "xn=",T[3][len(T[3])-1][2]
    text[9] = "un=",T[3][len(T[3])-1][3]
    text[10] = "vn=",T[3][len(T[3])-1][4]
    text[11] = "maxS*=",T[10], "minS*=",T[11]
    text[12] = "Всего ум. шага=",T[3][len(T[3])-1][8]
    text[13] = "Всего ув. шага=",T[3][len(T[3])-1][9]
    text[14] = "hmax=",T[4], "  при x=",T[6]
    text[15] = "hmin=",T[5], "  при x=",T[7]
    return text

def cnv(tup):
    str = ''
    if type(tup) == tuple:
        for item in tup:
            str = str + "% s" % item
        return str
    else:
        return tup

_VARS = {'window': False}
headers = {'i':[], 'hi':[], 'xi':[], 'ui':[], 'vi':[], 'u2i':[], 'v2i':[], 'S*':[], 'C1':[], 'C2':[]}
headings = list(headers)
table = pandas.DataFrame(columns=headers)
values = table.values.tolist()
layout = [
          [gui.Text('Введите правую границу вычислений по времени'),gui.HSeparator(pad=(50,0)), gui.Text(key='Help'), gui.HSeparator(pad=(50,0)),gui.Table(values = values, expand_x=True, headings = headings, key='Table', expand_y=True, auto_size_columns=True, col_widths=list(map(lambda x:len(x)+1, headings)))],
          [gui.Input(key='b')],
          [gui.Text('Введите параметр ε')],
          [gui.Input(key='e')],
          [gui.Text('Введите шаг')],
          [gui.Input(key='h1')],
          [gui.Exit('Exit')],
          [gui.Submit('Enter')],
          [gui.Canvas(key='figCanvas', expand_x=True, expand_y=True)],
]

#print(tabulate(T[3],["i","hi","xi","ui","vi","u2i","v2i","S*","C1","C2"],tablefmt="fancy_grid"))
_VARS['window'] = gui.Window('First', layout, resizable=True, finalize=True)
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(fill = 'x', side='left', expand=True)
    return figure_canvas_agg
while True:
    event, values = _VARS['window'].read()
    if event == 'Enter':
        b = float(values['b'])
        e = float(values['e'])
        h1 = float(values['h1'])
        T = Total(0, 1, 1, h1)
        fig1 = plt.figure()
        plt.subplot(1, 3, 1)
        plt.plot(T[0], T[1], 'r')  # x, u ось
        plt.title("Численное решение (u(t))")
        fig2 = plt.figure()
        plt.subplot(1, 3, 2)
        plt.plot(T[0], T[2], 'r')  # x, u' ось
        plt.title("Численное решение (v(t))")
        fig3 = plt.figure()
        plt.subplot(1, 3, 3)
        plt.plot(T[1], T[2], 'r')  # фазовое пространство
        plt.title("Фазовый портрет")
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig1)
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig2)
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig3)
        Values = T[3]
        gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table'), Values)
        Help = reference()
        for i in range(16):
            text = text + cnv(Help[i]).strip() + "\n"
        gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
        gui.Window.refresh(_VARS['window'])
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
_VARS['window'].close()

#reference()
#plt.show()