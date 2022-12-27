#coding=windows-1251
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import math
import PySimpleGUI as gui
import pandas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#print("Input step count:")
#n=int(input())
Text = ""
#print("Input step")
#h=float(input())
#print("Input b")
#b=float(input())
#print("Input e")
#e=float(input())
u=1
Table=[]
x1 = np.arange(0, 2, 0.01)
#plt.plot(x,math.log(x))
def O(w):
   t=float('{:.5f}'.format(w))
   return t
def f(x,u):
    return u
def CorrectStep(a,h):
    h=h/2
    a[0]=a[0]+h
    k1=f(a[0],a[1])
    k2=f(a[0]+h/2,a[1]+(h/2)*k1)
    k3=f(a[0]+h/2,a[1]+(h/2)*k2)
    k4=f(a[0]+h,a[1]+h*k3)
    a[1]=a[1]+(h/6)*(k1+2*k2+2*k3+k4)
    return a
def RungeKutt4B(n,h):
      i=0   
      x=[0]
      v=[1]
      while i<=n:
          if (x[i]>b):
             del x[len(x)-1]
             del v[len(v)-1]
             return x, v
          x.append(x[i]+h)
          k1=f(x[i],v[i])
          k2=f(x[i]+h/2,v[i]+(h/2)*k1)
          k3=f(x[i]+h/2,v[i]+(h/2)*k2)
          k4=f(x[i]+h,v[i]+h*k3)
          u=np.exp(x[i])
          v.append(v[i]+(h/6)*(k1+2*k2+2*k3+k4))
          i+=1  
      return x,v
def RungeKutt4(n,h):
      i=0  
      c=0
      C1=0
      C2=0
      x=[0]
      v=[1]
      maxh=h
      minh=h
      q1=0
      q2=0
      maxL=0
      while i<=n:
          if (x[i]>b):
             c=1
             del x[len(x)-1]
             del v[len(v)-1]
             return x, v, Table,i,O(maxh),O(minh),O(q1),O(q2),O(maxL),c
          x.append(x[i]+h)
          k1=f(x[i],v[i])
          k2=f(x[i]+h/2,v[i]+(h/2)*k1)
          k3=f(x[i]+h/2,v[i]+(h/2)*k2)
          k4=f(x[i]+h,v[i]+h*k3)
          u=np.exp(x[i])
          L=[x[i],v[i]]
          v1=v[i]+(h/6)*(k1+2*k2+2*k3+k4)
          v2=(CorrectStep([CorrectStep(L,h)[0], CorrectStep(L,h)[1]],h)[1])
          S=(v1-v2)/(2**4-1)
          E=abs(S*(2**4))
          #Table.append([i,float('{:.6f}'.format(x[i])),float('{:.13f}'.format(v[i])),float('{:.6f}'.format(v2)),float('{:.6f}'.format(abs(v1-v2))),E,h,float('{:.6f}'.format(C1)),float('{:.6f}'.format(C2)),float('{:.13f}'.format(u)),float('{:.20f}'.format(abs(u-v[i])))])
          if(abs(S)<e/(2**5)):
             v.append(v[i]+(h/6)*(k1+2*k2+2*k3+k4))
             h=2*h
             C2+=1
          elif(abs(S)>e):
              #i-=1
              del x[len(x)-1]

              h=h/2
              C1+=1
              continue
          else:
              v.append(v[i]+(h/6)*(k1+2*k2+2*k3+k4))
          if h>maxh:
              maxh=h
              q1=x[i]
          if h<minh:
              minh=h
              q2=x[i]
          if E>maxL:
              maxL=E 
          Table.append([i,float('{:.6f}'.format(x[i])),float('{:.13f}'.format(v[i])),float('{:.6f}'.format(v2)),float('{:.6f}'.format(abs(v1-v2))),E,h,float('{:.6f}'.format(C1)),float('{:.6f}'.format(C2)),float('{:.13f}'.format(u)),float('{:.20f}'.format(abs(u-v[i])))])
          i+=1
      return x,v,Table,i-1,O(maxh),O(minh),O(q1),O(q2),maxL,c
_VARS = {'window': False}
headers = {'i':[], 'x':[], 'v':[], 'v2':[], 'v1-v2':[], 'OLP':[], 'h':[], 'C1':[], 'C2':[], 'u':[], '|u-v|':[]}
headings = list(headers)
table = pandas.DataFrame(columns=headers)
values = table.values.tolist()
layout = [
          [gui.Text('n:'),gui.HSeparator(pad=(50,0)), gui.Text(key='Help'), gui.HSeparator(pad=(50,0)),gui.Table(values = values, expand_x=True, headings = headings, key='Table', expand_y=True, auto_size_columns=True, col_widths=list(map(lambda x:len(x)+1, headings)))],
          [gui.Input(key='n')],
          [gui.Text('ε:')],
          [gui.Input(key='e')],
          [gui.Text('h:')],
          [gui.Input(key='h')],
          [gui.Text('b:')],
          [gui.Input(key='b')],
          [gui.Exit('Exit')],
          [gui.Submit('Enter')],
          [gui.Canvas(key='figCanvas', expand_x=True, expand_y=True)],
]

#print(tabulate(T[3],["i","hi","xi","ui","vi","u2i","v2i","S*","C1","C2"],tablefmt="fancy_grid"))
_VARS['window'] = gui.Window('First', layout, resizable=True, finalize=True)
def cnv(tup):
    str = ''
    if type(tup) == tuple:
        for item in tup:
            str = str + "% s" % item
        return str
    else:
        return tup
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(fill = 'x', side='left', expand=True)
    return figure_canvas_agg
#print(tabulate(RungeKutt4(n,h)[2],["i","x","v","v2","v1-v2","OLP","h","C1","C2","u","|u-v|"], tablefmt="fancy_grid"))
while True:
    event, values = _VARS['window'].read()
    if event == 'Enter':
        n = int(values['n'])
        h = float(values['h'])
        b = float(values['b'])
        e = float(values['e'])
        if n > 100:
            n = 100
        text = [0, 1, 2, 3]
        fig = plt.figure()
        plt.subplot()
        plt.plot(x1,np.exp(x1), "b")
        plt.subplot()
        plt.plot(RungeKutt4(n,h)[0],RungeKutt4(n,h)[1],"g")
        plt.subplot()
        plt.plot(RungeKutt4B(n,h)[0],RungeKutt4B(n,h)[1],"y")
        bh=float(RungeKutt4(n,h)[0].pop())
        h1=b-bh
        if RungeKutt4(n,h)[9]==0:
            text[0] = "n=",len(RungeKutt4(n,h)[0])-2," b-xn=",O(h1)
        else:
            text[0] = "n=",len(RungeKutt4(n,h)[0])-1," b-xn=",O(h1)
        text[1] = "max OLP=",RungeKutt4(n,h)[8]
        text[2] = "max h=",RungeKutt4(n,h)[4]," when x=",RungeKutt4(n,h)[6]
        text[3] = "min h=",RungeKutt4(n,h)[5]," when x=",RungeKutt4(n,h)[7]
        for i in range(4):
            Text = Text + cnv(text[i]).strip() + "\n"
        draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig)
        gui.Text.update(gui.Window.find_element(_VARS['window'], 'Help'), text)
        gui.Table.update(gui.Window.find_element(_VARS['window'], 'Table'), RungeKutt4(n,h)[2])
        gui.Window.refresh(_VARS['window'])
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
_VARS['window'].close()


