from tkinter import *
import tkinter as tk
from tkinter import ttk
from time import strftime, localtime
import os
from widgets import *
from time import ctime,sleep
from custom import *

top = Tk(None, "", " Health Message Maker")
top.geometry("608x812")
top.resizable(width=False,height=False)
style = ttk.Style()
style.theme_create('mainstyle', parent='alt', settings={
    'north.TNotebook': {'configure': {
        'background':'#555',
        'tabmargins': [5,5,5,5],
        'relief':'flat'}},
    'bgb.TNotebook.Tab': {'configure': {
        'background': '#aaa',
        'bd': 0,
        'padding':[0,0]},}})
style.theme_use('mainstyle')

style2 = ttk.Style()
style2.configure('mainTabs.TNotebook', tabmargins=[5,10,5,0], tabposition='nw',
                 background=colors[0], font=('Arial',14))
style2.configure('mainTabs.TNotebook.Tab', background=colors[1],foreground=colors[2],
                 font=('Arial','14','bold'))
tabbgstyle = ttk.Style()
tabbgstyle.configure('bgb.TFrame', background=colors[3], bd=0)
tabbgstyle.configure('bgb.TFrame.Tab', background=colors[4], bd=0)

tabTop = ttk.Notebook(top, style='mainTabs.TNotebook')

gdtTab = ttk.Frame(tabTop, width=608, height=760, style='bgb.TFrame')
HL7Tab = ttk.Frame(tabTop)
DICOMTab = ttk.Frame(tabTop)

tabTop.add(gdtTab, text='  GDT  ')
tabTop.add(HL7Tab, text='  HL7  ')
tabTop.add(DICOMTab, text='  DICOM  ')

gdtTabTop = CustomNotebook(gdtTab, width=608, height=696)
HL7TabTop = CustomNotebook(HL7Tab, width=608, height=696)
DICOMTabTop = CustomNotebook(DICOMTab, width=608, height=696)

def gdtprint():
    for n in gdtTabTop.children:
        if gdtTabTop.children[n].winfo_ismapped():
            for m in gdtTabTop.children[n].contentFrame.elements:
                if m not in  ['Satzidentifikation','Satzlänge']:
                    gdtTabTop.children[n].contentFrame.elements[m].update()
            gdtTabTop.children[n].print()
            break

def gdtsave():
    for n in gdtTabTop.children:
        if gdtTabTop.children[n].winfo_ismapped():
            for m in gdtTabTop.children[n].contentFrame.elements:
                if m not in  ['Satzidentifikation','Satzlänge']:
                    gdtTabTop.children[n].contentFrame.elements[m].update()
            path = gdtTabTop.children[n].paths[0]
            gdtTabTop.children[n].save(path)
            break

def setgdtpath(*opts):
    for n in gdtTabTop.children:
        if gdtTabTop.children[n].winfo_ismapped():
            gdtpathopts.set('')
            new_choices = tuple(gdtTabTop.children[n].paths)
            for choice in new_choices:
                gdtMsgPathMenu['menu'].add_command(label=choice, command=tk._setit(gdtpathopts, choice))
            gdtTabTop.children[n].paths.insert(0,gdtTabTop.children[n].paths.pop(
                gdtTabTop.children[n].paths.index(opts[0])))
            break

gdtprintBtn = Button(gdtTab,text='Nachricht anzeigen',command=gdtprint,bd=5)
gdtprintBtn.place(x=300,y=728)
gdtsaveBtn = Button(gdtTab,text='Speichern',command=gdtsave,bd=5)
gdtsaveBtn.place(x=140,y=728)
gdtpathopts = tk.StringVar()
gdtMsgPathMenu = OptionMenu(gdtTab,variable=gdtpathopts,value=os.environ['HOME']+'/Messages/gdt/test.gdt',command=setgdtpath)
gdtMsgPathMenu.place(x=216,y=728)

import pickle
try:
    with open('recent.p','rb') as recentFile:
        recent = pickle.load(recentFile)
except:
    with open('recent.p','wb') as recentFile:
        pickle.dump([],recentFile)
    recent = []

gdtTab1 = gdtFileTab(gdtTabTop)
gdtTab2 = gdtFileTab(gdtTabTop)
gdtTabTop.add(gdtTab1, text='  file 1  ')
gdtTabTop.add(gdtTab2, text='  file 2  ')

gdtTabTop.place(x=0,y=0)
HL7TabTop.place(x=0,y=0)
DICOMTabTop.place(x=0,y=0)

tabTop.pack(expand=1, fill='both')

