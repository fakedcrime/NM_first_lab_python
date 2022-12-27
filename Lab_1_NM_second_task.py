#coding=windows-1251
import matplotlib.pyplot as plt
import math
from tabulate import tabulate
import numpy as np
import PySimpleGUI as gui
import pandas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
x0 = 0
u0 = 1
h = 0.001
n = 30
eps = 0.00000001
def f(x, u):
    du = ((x / (1 + x ** 2)) * u ** 2) + u - (u ** 3) * math.sin(10 * x)
    return du


def Test(x, u):
    return u

text = ""


metod = 2  # метод для основной задачи
metodTest = 2  # метод для тестовой задачи
b = 2

Table = [["i", "x", "v", "   v2   ", "  v1-v2 ", "   S   ", "h", "C1", "C2"]]
TabetTest = [["i", "x", "v", "   v2   ", "  v1-v2 ", "   S   ", "h", "C1", "C2", "u", "u-v"]]


# метод для тестовой фунуции с постоянным шагом
def RungeKutt4Test(x1, v1, h, n, eps, b):
    i = 0
    v = [v1]
    x = [x1]
    U = [v1]
    maxL = 0
    while len(x) <= n:
        if x[i] > b:
            return x, v, U, TabetTest, maxL
        x.append(x[i] + h)

        k1 = Test(x[i], v[i])
        k2 = Test(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = Test(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = Test(x[i] + h, v[i] + h * k3)

        v.append(v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
        v1 = v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x2, v2 = halfh_v2Test(x[i], v[i], h / 2)

        S = (v1 - v2[2]) / ((2 ** 4) - 1)
        u = np.exp(x[i] + h)

        U.append(u)
        if abs(S) > maxL:
            maxL = S

        TabetTest.append([i, x[i], v[i], v2, abs(v1 - v2[2]), abs(S), h, u, abs(u - v1)])
        i += 1

    return x, v, U, TabetTest, maxL


# метод с постоянным шагом
def RungeKutt4(x1, v1, h, n, eps, b):
    i = 0
    v = [v1]
    x = [x1]
    maxL = 0
    while len(x) <= n:

        if x[i] > b:
            return x, v, Table, maxL
        x.append(x[i] + h)

        k1 = f(x[i], v[i])
        k2 = f(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = f(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = f(x[i] + h, v[i] + h * k3)

        v.append(v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
        v1 = v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x2, v2 = halfh_v2(x[i], v[i], h / 2)

        S = (v1 - v2[2]) / ((2 ** 4) - 1)

        if abs(S) > maxL:
            maxL = S

        Table.append([i, x[i], v[i], v2, abs(v1 - v2[2]), abs(S), h])
        i += 1

    return x, v, Table, maxL


# метод для тестовой фунуции с переменным шагом
def RungeKutt4hTest(x1, v1, h, n, eps, b):
    i = 0
    v = [v1]
    x = [x1]
    U = [v1]
    C1 = 0
    C2 = 0
    S_new = 1
    S_old = 1
    maxh = h
    minh = h
    q1 = [h, 0]
    q2 = [h, 0]
    maxL = 0
    while len(x) <= n:
        if x[i] > b or v[i] > 100 or v[i] < -100:
            return x, v, U, TabetTest, maxL, q1, q2

        v_old = v[i]
        S_old = S_new
        k1 = Test(x[i], v[i])
        k2 = Test(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = Test(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = Test(x[i] + h, v[i] + h * k3)
        v_new = v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x2, v2 = halfh_v2Test(x[i], v[i], h / 2)
        v_ = v2[2]

        S_new = (v_new - v_) / ((2 ** 4) - 1)

        if eps / (2 ** 5) <= abs(S_new) and abs(S_new) <= eps:
            x.append(x[i] + h)
            v.append(v_new)
            u = np.exp(x[i] + h)
            U.append(u)
            TabetTest.append([i + 1, x[i], v[i], v_, abs(v_new - v_), abs(S_new), h, C1, C2, u, abs(u - v1)])
            i += 1
        elif abs(S_new) < eps / (2 ** 5):
            x.append(x[i] + h)
            v.append(v_new)
            u = np.exp(x[i] + h)
            U.append(u)
            TabetTest.append([i + 1, x[i], v[i], v_, abs(v_new - v_), abs(S_new), h, C1, C2, u, abs(u - v1)])
            h = 2 * h
            C2 += 1
            i += 1
        else:
            h = h / 2
            C1 += 1
        if h > maxh:
            maxh = h
            q1 = [maxh, x[i]]
        if h < minh:
            minh = h
            q2 = [minh, x[i]]

        if abs(S_new) > maxL:
            maxL = S_new

    return x, v, U, TabetTest, maxL, q1, q2


# метод с переменным шагом
def RungeKutt4h(x1, v1, h, n, eps, b):
    i = 0
    v = [v1]
    x = [x1]
    C1 = 0
    C2 = 0
    S_new = 1
    S_old = 1
    maxh = h
    minh = h
    q1 = [h, 0]
    q2 = [h, 0]
    maxL = 0
    while len(x) <= n:

        if x[i] > b or v[i] > 100 or v[i] < -100:
            return x, v, Table, maxL, q1, q2

        v_old = v[i]
        S_old = S_new
        k1 = f(x[i], v[i])
        k2 = f(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = f(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = f(x[i] + h, v[i] + h * k3)
        v_new = v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x2, v2 = halfh_v2(x[i], v[i], h / 2)
        v_ = v2[2]

        S_new = (v_new - v_) / ((2 ** 4) - 1)

        if eps / (2 ** 5) <= abs(S_new) and abs(S_new) <= eps:
            x.append(x[i] + h)
            v.append(v_new)

            Table.append([i + 1, x[i], v[i], v_, abs(v_new - v_), abs(S_new), h, C1, C2])
            i += 1
        elif abs(S_new) < eps / (2 ** 5):
            x.append(x[i] + h)
            v.append(v_new)

            Table.append([i + 1, x[i], v[i], v_, abs(v_new - v_), abs(S_new), h, C1, C2])
            h = 2 * h
            C2 += 1
            i += 1
        else:
            h = h / 2
            C1 += 1
        if h > maxh:
            maxh = h
            q1 = [maxh, x[i]]

        if h < minh:
            minh = h
            q2 = [minh, x[i]]
        if abs(S_new) > maxL:
            maxL = S_new

    return x, v, Table, maxL, q1, q2


def reference(metod, x, b, maxL, q1, q2):  # Справка
    if metod == 1:
        T = [0, 1]
        T[0] = "n=", len(x) - 1
        T[1] = " b-xn=", b - x[len(x) - 1]
        return T
    else:
        T = [0, 1, 2 , 3, 4]
        T[0]="n=", len(x) - 1
        T[1]=" b-xn=", b - x[len(x) - 1]
        T[2]="max OLP=", maxL
        T[3]="max h=", q1[0], " when x=", q1[1]
        T[4]="min h=", q2[0], " when x=", q2[1]
        return T

def cnv(tup):
    str = ''
    if type(tup) == tuple:
        for item in tup:
            str = str + "% s" % item
        return str
    else:
        return tup

def halfh(xi, vi, h):
    xi = xi + h
    k1 = f(xi, vi)
    k2 = f(xi + h / 2, vi + (h / 2) * k1)
    k3 = f(xi + h / 2, vi + (h / 2) * k2)
    k4 = f(xi + h, vi + h * k3)
    vi = vi + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return xi, vi


def halfh_v2(xi, vi, h):  # Половинный шаг
    x = [xi]
    v = [vi]

    for i in [0, 1]:
        x.append(x[i] + h)
        k1 = f(x[i], v[i])
        k2 = f(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = f(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = f(x[i] + h, v[i] + h * k3)
        v.append(v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))

    return x, v


def halfh_v2Test(xi, vi, h):  # Половинный шаг для тестовой функции
    x = [xi]
    v = [vi]

    for i in [0, 1]:
        x.append(x[i] + h)
        k1 = Test(x[i], v[i])
        k2 = Test(x[i] + h / 2, v[i] + (h / 2) * k1)
        k3 = Test(x[i] + h / 2, v[i] + (h / 2) * k2)
        k4 = Test(x[i] + h, v[i] + h * k3)
        v.append(v[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))

    return x, v

_VARS = {'window': False}
headers = {'i':[], 'x':[], 'v':[], 'v2':[], 'v1-v2':[], 'S':[], 'h':[], 'C1':[], 'C2':[], 'U':[], 'u-v':[]}
headers1 = {'i':[], 'x':[], 'v':[], 'v2':[], 'v1-v2':[], 'S':[], 'h':[], 'C1':[], 'C2':[]}
headings = list(headers)
headings1 = list(headers1)
table = pandas.DataFrame(columns=headers)
table1 = pandas.DataFrame(columns=headers1)
values = table.values.tolist()
values1 = table1.values.tolist()
layout = [
          [gui.Text('x0:'),gui.HSeparator(pad=(50,0)), gui.Text(key='Help'), gui.HSeparator(pad=(50,0)),gui.Table(values = values, expand_x=True, headings = headings, key='Table', expand_y=True, auto_size_columns=True, col_widths=list(map(lambda x:len(x)+1, headings)))],
          [gui.Input(key='x0'), gui.HSeparator(pad=(150,0)), gui.Table(values = values1, expand_x=True, headings = headings1, key='Table1', expand_y=True, auto_size_columns=True, col_widths=list(map(lambda x:len(x)+1, headings1)))],
          [gui.Text('u0:')],
          [gui.Input(key='u0')],
          [gui.Text('h:')],
          [gui.Input(key='h')],
          [gui.Text('n:')],
          [gui.Input(key='n')],
          [gui.Text('eps:')],
          [gui.Input(key='eps')],
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
        u0 = float(values['u0'])
        x0 = float(values['x0'])
        h = float(values['h'])
        n = int(values['n'])
        eps = float(values['eps'])
        if metodTest == 1:  # вызов метода для тестовой фунуции с постоянным шагом

            x, v, u, Table1, maxL = RungeKutt4Test(x0, u0, h, n, eps, b)
            fig1 = plt.figure()
            plt.subplot()
            plt.plot(x, v, "g-")
            # plt.show()
            plt.plot(x, u, "y-")
            plt.title("Численное решение тестовой задачи")
            draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig1)
            i = 0
            while len(Table1) > i:
                print(Table1[i])
                i += 1

            Help = reference(metodTest, x, b, maxL, 0, 0)
            for i in range(2):
                text = text + cnv(Help[i]).strip() + "\n"
            gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
            del Table1[0]
            gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table'), Table1)
            gui.Window.refresh(_VARS['window'])
        elif metodTest == 2:  # вызов метода для тестовой фунуции с переменным шагом

            x, v, u, Table1, maxL, q1, q2 = RungeKutt4hTest(x0, u0, h, n, eps, b)
            fig2 = plt.figure()
            plt.subplot()
            plt.plot(x, v, "g-")
            # plt.show()
            plt.plot(x, u, "y-")
            plt.title("Численное решение тестовой задачи")
            draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig2)
            i = 0
            while len(Table1) > i:
                print(Table1[i])
                i += 1
            Help = reference(metodTest, x, b, maxL, q1, q2)
            for i in range(5):
                text = text + cnv(Help[i]).strip() + "\n"
            gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
            del Table1[0]
            gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table'), Table1)
            gui.Window.refresh(_VARS['window'])
        if metod == 1:  # вызов метода с постоянным шагом
            plt.subplot()
            fig3 = plt.figure()
            x, v, Table, maxL = RungeKutt4(x0, u0, h, n, eps, b)
            plt.plot(x, v, "y-")
            plt.title("Численное решение основной задачи")
            draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig3)
            i = 0
            while len(Table) > i:
                print(Table[i])
                i += 1

            Help = reference(metod, x, b, maxL, 0, 0)
            for i in range(2):
                text = text + cnv(Help[i]).strip() + "\n"
            gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
            del Table[0]
            gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table1'), Table)
            gui.Window.refresh(_VARS['window'])
        elif metod == 2:  # вызов метода с переменным шагом
            plt.subplot()
            fig4 = plt.figure()
            x, v, Table, maxL, q1, q2 = RungeKutt4h(x0, u0, h, n, eps, b)
            plt.plot(x, v, "g-")
            plt.title("Численное решение основной задачи")
            draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig4)
            i = 0
            while len(Table) > i:
                print(Table[i])
                i += 1
            Help = reference(metod, x, b, maxL, q1, q2)
            for i in range(5):
                text = text + cnv(Help[i]).strip() + "\n"
            gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
            del Table[0]
            gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table1'), Table)
            gui.Window.refresh(_VARS['window'])
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
_VARS['window'].close()