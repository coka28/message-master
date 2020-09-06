
from tkinter import *
import os,stat
import tkinter as tk
from tkinter import ttk
from time import strftime, localtime
from custom import *

colors = ['#263','#485','#ddd','#263','#643','#efe']

class TypeSelector:

    def __init__(self,top):
        self.container = LabelFrame(top.content,text='  Nachrichtentyp  ',width=562,height=100)
        self.typeRB6301 = Radiobutton(self.container, text='6301 (Stammdaten importieren)',
                                      variable=top.msgType, value='6301', command=top.setType)
        self.typeRB6302 = Radiobutton(self.container, text='6302 (Untersuchung anfordern)',
                                      variable=top.msgType, value='6302', command=top.setType)
        self.typeRB6310 = Radiobutton(self.container, text='6310 (Untersuchung exprotieren)',
                                      variable=top.msgType, value='6310', command=top.setType)
        self.typeRB6311 = Radiobutton(self.container, text='6311 (blaaa)',
                                      variable=top.msgType, value='6311', command=top.setType)

        self.typeRB6301.place(x=20,y=7)
        self.typeRB6302.place(x=20,y=37)
        self.typeRB6310.place(x=270,y=7)
        self.typeRB6311.place(x=270,y=37)

    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()


class LabeledLineEdit:

    def update(self):
        if self.var.get()!='':
            self.top.message.setField(self.field,self.var.get())
        else:
            self.top.message.setField(self.field,None)
        self.top.message.setMsgLength()
        self.top.sentLength.set(self.top.message.fields['Satzlänge'][1])
        return True

    def __init__(self, top, label, field, var, font=('Arial','11')):
        self.top = top
        self.container = Frame(top.content,width=580,height=36)
        self.field = field
        self.var = var
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else '')
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.line = Entry(self.container, font=font, width=28)
        self.line.config(textvariable=self.var, validate=ALL, validatecommand=self.update)
        self.label.place(x=0,y=7)
        self.line.place(x=300,y=7)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()

class LabeledTextEdit:

    def update(self):
        self.top.message.setField(self.field,self.var.get())
        self.top.message.setMsgLength()
        self.top.sentLength.set(self.top.message.fields['Satzlänge'][1])
        return True

    def __init__(self, top, label, field, var, font=('Arial','11')):
        self.top = top
        self.container = Frame(top.content,width=580,height=180)
        self.field = field
        self.var = var
        self.textContainer = Frame(self.container,width=288,height=170)
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else '')
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.scrollbar = Scrollbar(self.textContainer, orient= VERTICAL)
        self.textfield = Text(self.textContainer, yscrollcommand= self.scrollbar.set,width=28,height=9)
        self.scrollbar.config(command=self.textfield.yview)
        self.textfield.insert(END,top.message.fields[field][1] if top.message.fields[field][1]!=None else '')
        self.textContainer.place(x=300,y=7)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.textfield.pack()
        self.line = self.textfield
        #self.line.config(Variable=self.var, validate='key', validatecommand=self.update)
        self.label.place(x=0,y=7)
        self.textfield.bind('<Enter>', top.container._unbound_to_mousewheel)
        self.textfield.bind('<Leave>', top.container._bound_to_mousewheel)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()

class LabeledText:

    def __init__(self, top, label, field, var, font=('Arial','11')):
        self.top = top
        self.container = Frame(top.content,width=580,height=36)
        self.field = field
        self.var = var
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else '')
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.label2 = Label(self.container, textvariable=self.var, font=font)
        self.label.place(x=0,y=7)
        self.label2.place(x=300,y=7)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()

class LabeledDroplist:

    def update(self,*args):
        if self.var.get()!='':
            self.top.message.setField(self.field,self.mapping(self.var.get()))
        else:
            self.top.message.setField(self.field,None)
        self.top.message.setMsgLength()
        self.top.sentLength.set(self.top.message.fields['Satzlänge'][1])

    def __init__(self, top, label, field, var, *opts, mapping=(lambda x:x), font=('Arial','11')):
        self.top = top
        self.mapping = mapping
        self.container = Frame(top.content,width=580,height=36)
        self.field = field
        self.var = var
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else '')
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.drop = OptionMenu(self.container, self.var, *opts, command=self.update)
        self.label.place(x=0,y=7)
        self.drop.place(x=300,y=7)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()

class LabeledDateEdit:

    def update(self):
        self.var.set(self.days.get()+self.months.get()+self.years.get())
        if self.var.get()!='':
            self.top.message.setField(self.field,self.var.get())
        else:
            self.top.message.setField(self.field,None)
        self.top.message.setMsgLength()
        self.top.sentLength.set(self.top.message.fields['Satzlänge'][1])
        return True

    def __init__(self, top, label, field, var, font=('Arial','11')):
        self.days = StringVar()
        self.months = StringVar()
        self.years = StringVar()
        self.top = top
        self.container = Frame(top.content,width=580,height=36)
        self.field = field
        self.var = var
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else
                     ('01012000' if field in top.message.mandatory[top.msgType.get()] else ''))
        self.days.set(self.var.get()[:2])
        self.months.set(self.var.get()[2:4])
        self.years.set(self.var.get()[4:])
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.daysline = Entry(self.container, font=font, width=2)
        self.daysline.config(textvariable=self.days, validate=ALL, validatecommand=self.update)
        self.monthsline = Entry(self.container, font=font, width=2)
        self.monthsline.config(textvariable=self.months, validate=ALL, validatecommand=self.update)
        self.yearsline = Entry(self.container, font=font, width=4)
        self.yearsline.config(textvariable=self.years, validate=ALL, validatecommand=self.update)
        self.label2 = Label(self.container, text='TT/MM/JJJJ', font=font+('italic',), width=10,anchor='e')
        self.label.place(x=0,y=7)
        self.daysline.place(x=300,y=7)
        self.monthsline.place(x=326,y=7)
        self.yearsline.place(x=352,y=7)
        self.label2.place(x=410,y=7)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()

class LabeledTimeEdit:

    def update(self):
        self.var.set(self.hours.get()+self.minutes.get()+self.seconds.get())
        print(self.var.get())
        if self.var.get()!='':
            self.top.message.setField(self.field,self.var.get())
        else:
            self.top.message.setField(self.field,None)
        self.top.message.setMsgLength()
        self.top.sentLength.set(self.top.message.fields['Satzlänge'][1])
        return True
    
    def __init__(self, top, label, field, var, font=('Arial','11')):
        self.hours = StringVar()
        self.minutes = StringVar()
        self.seconds = StringVar()
        self.top = top
        self.container = Frame(top.content,width=580,height=36)
        self.field = field
        self.var = var
        self.var.set(tmp if (tmp:=top.message.fields[field][1])!=None else '')
        self.hours.set(self.var.get()[:2])
        self.minutes.set(self.var.get()[2:4])
        self.seconds.set(self.var.get()[4:])
        self.label = Label(self.container, text=label, font=font, width=30,anchor='e')
        self.hoursline = Entry(self.container, font=font, width=2)
        self.hoursline.config(textvariable=self.hours, validate=ALL, validatecommand=self.update)
        self.minutesline = Entry(self.container, font=font, width=2)
        self.minutesline.config(textvariable=self.minutes, validate=ALL, validatecommand=self.update)
        self.secondsline = Entry(self.container, font=font, width=2)
        self.secondsline.config(textvariable=self.seconds, validate=ALL, validatecommand=self.update)
        self.label2 = Label(self.container, text='HH:MM:SS', font=font+('italic',), width=10,anchor='e')
        self.label.place(x=0,y=7)
        self.hoursline.place(x=300,y=7)
        self.minutesline.place(x=326,y=7)
        self.secondsline.place(x=352,y=7)
        self.label2.place(x=410,y=7)
        
    def place(self):
        self.container.pack()

    def remove(self):
        self.container.pack_forget()


class Console:
    '''
    '''

    def __init__(self, top, label=None, bg='gray95', bd='2', font=('Arial',12), width=None, height=None):
        if isinstance(label,str):
            self.container = LabelFrame(top,text=label,bg=bg,bd=bd,font=font,width=width,height=height)
        else:
            self.container = Frame(top,bg=bg, bd=bd, width=608, height=height)

        self.scrollbar = Scrollbar(self.container, orient= VERTICAL)
        self.textfield = Text(self.container, yscrollcommand= self.scrollbar.set,bg=bg,width=width,height=height)
        self.scrollbar.config(command=self.textfield.yview)
        self.textfield.insert(END,'Hallo!')
        self.textfield.configure(state=DISABLED)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.textfield.pack()


    def addLine(self, line, timestamp=False):
        self.textfield.configure(state = NORMAL)
        if timestamp: line = '\n' + strftime('%H:%M:%S : ') + line
        self.textfield.insert(END, line)
        self.textfield.configure(state = DISABLED)
        self.textfield.see(END)

    def place(self,**kwargs):
        self.container.place(**kwargs)


class Content:
    '''
    '''

    def setType(self):
        self.message.setType(self.msgType.get())
        self.top.consoleFrame.addLine('Changed Message Type to '+self.msgType.get(),True)

    def __init__(self, top, gdtMsg):
        self.top = top
        self.container = ScrollFrame(self.top, bd=4, width=608,height=536)
        self.content = self.container.interior
        
        self.typeState = None
        self.message = gdtMsg
        self.active = []
        
        # vars for message
        self.msgType = StringVar()
        tmpType = gdtMsg.fields['Satzidentifikation'][1]
        if tmpType not in ['6301','6302','6310','6311']:
            self.message.setType('6301')
        self.msgType.set(gdtMsg.fields['Satzidentifikation'][1])
        
        self.gdtReceiver = StringVar()
        self.gdtReceiver.set(self.message.fields['GDT-ID-Empfänger'][1])
        
        self.gdtSender = StringVar()
        self.gdtSender.set(self.message.fields['GDT-ID-Sender'][1])
        
        self.encoding = StringVar()
        self.encoding.set(self.message.fields['Zeichensatz'][1])
        
        self.gdtVersion = StringVar()
        self.gdtVersion.set(self.message.fields['GDT-ID-Sender'][1])
        
        self.patID = StringVar()
        self.patID.set(self.message.fields['Patienten-ID'][1])
        
        self.nameAppendix = StringVar()
        self.nameAppendix.set(self.message.fields['Namenszusatz'][1])
        
        self.lastName = StringVar()
        self.lastName.set(self.message.fields['Nachname'][1])
        
        self.firstName = StringVar()
        self.firstName.set(self.message.fields['Vorname'][1])
        
        self.dateOfBirth = StringVar()
        self.dateOfBirth.set(self.message.fields['Geburtsdatum'][1])
        
        self.patTitle = StringVar()
        self.patTitle.set(self.message.fields['Titel'][1])
        
        self.insuranceNr = StringVar()
        self.insuranceNr.set(self.message.fields['Versicherungsnummer'][1])
        
        self.residence = StringVar()
        self.residence.set(self.message.fields['Wohnort'][1])
        
        self.address = StringVar()
        self.address.set(self.message.fields['Adresse'][1])
        
        self.insuranceType = StringVar()
        self.insuranceType.set(self.message.fields['Versichertenart'][1])
        
        self.sex = StringVar()
        self.sex.set(self.message.fields['Geschlecht'][1])
        
        self.height = StringVar()
        self.height.set(self.message.fields['Körpergröße'][1])
        
        self.weight = StringVar()
        self.weight.set(self.message.fields['Gewicht'][1])
        
        self.language = StringVar()
        self.language.set(self.message.fields['Muttersprache'][1])
        
        self.procedure = StringVar()
        self.procedure.set(self.message.fields['Verfahren'][1])
        
        self.testIdent = StringVar()
        self.testIdent.set(self.message.fields['Test-Ident'][1])
        
        self.examDate = StringVar()
        self.examDate.set(self.message.fields['Erhebungsdatum'][1])
        
        self.examTime = StringVar()
        self.examTime.set(self.message.fields['Erhebungsuhrzeit'][1])
        
        self.diagnose = StringVar()
        self.diagnose.set(self.message.fields['Diagnose'][1])
        
        self.finding = StringVar()
        self.finding.set(self.message.fields['Befund'][1])
        
        self.finding2 = StringVar()
        self.finding2.set(self.message.fields['Fremdbefund'][1])
        
        self.comment = StringVar()
        self.comment.set(self.message.fields['Kommentar'][1])
        
        self.filePath = StringVar()
        self.filePath.set(self.message.fields['Dateipfad'][1])

        self.sentLength = StringVar()
        self.message.setMsgLength()
        self.sentLength.set(gdtMsg.fields['Satzlänge'][1])

        def insuranceTypeMapping(insType):
            if insType.isnumeric():
                if insType == '1':
                    return 'Mitglied'
                if insType == '3':
                    return 'Familienversicherter'
                if insType == '5':
                    return 'Rentner'
            else:
                if insType == 'Mitglied':
                    return '1'
                if insType == 'Familienversicherter':
                    return '3'
                if insType == 'Rentner':
                    return '5'

        def sexMapping(sex):
            if sex.isnumeric():
                if sex == '1':
                    return 'Männlich'
                if sex == '2':
                    return 'Weiblich'
            else:
                if sex == 'Männlich':
                    return '1'
                if sex == 'Weiblich':
                    return '2'

        def codeMapping(encoding):
            if encoding.isnumeric():
                if encoding == '1':
                    return 'ascii'
                if encoding == '2':
                    return 'utf8'
                if encoding == '3':
                    return 'cp1252'
            else:
                if encoding == 'ascii':
                    return '1'
                if encoding == 'utf8':
                    return '2'
                if encoding == 'cp1252':
                    return '3'
            
        self.elements = {
            'Satzidentifikation': TypeSelector(self),
            'Satzlänge': LabeledText(self,'Satzlänge','Satzlänge',self.sentLength),
            'GDT-ID-Empfänger': LabeledLineEdit(self,'GDT-ID-Empfänger','GDT-ID-Empfänger',self.gdtReceiver),
            'GDT-ID-Sender': LabeledLineEdit(self,'GDT-ID-Sender','GDT-ID-Sender',self.gdtSender),
            'Zeichensatz': LabeledDroplist(self,'Zeichensatz','Zeichensatz',self.encoding,'ascii','utf8','cp1252',mapping=codeMapping),
            'GDT-Version': LabeledDroplist(self,'GDT-Version','GDT-Version',self.gdtVersion,'02.10'),
            'Patienten-ID': LabeledLineEdit(self,'Patienten-ID','Patienten-ID',self.patID),
            'Namenszusatz': LabeledLineEdit(self,'Namenszusatz','Namenszusatz',self.nameAppendix),
            'Nachname': LabeledLineEdit(self,'Nachname','Nachname',self.lastName),
            'Vorname': LabeledLineEdit(self,'Vorname','Vorname',self.firstName),
            'Geburtsdatum': LabeledDateEdit(self,'Geburtsdatum','Geburtsdatum',self.dateOfBirth),
            'Titel': LabeledLineEdit(self,'Titel','Titel',self.patTitle),
            'Versicherungsnummer': LabeledLineEdit(self,'Versicherungsnummer','Versicherungsnummer',self.insuranceNr),
            'Wohnort': LabeledLineEdit(self,'Wohnort','Wohnort',self.residence),
            'Adresse': LabeledLineEdit(self,'Adresse','Adresse',self.address),
            'Versichertenart': LabeledDroplist(self,'Versichertenart','Versichertenart',self.insuranceType,'Mitglied','Familienversicherter','Rentner',mapping=insuranceTypeMapping),
            'Geschlecht': LabeledDroplist(self,'Geschlecht','Geschlecht',self.sex,'Männlich','Weiblich',mapping=sexMapping),
            'Körpergröße': LabeledLineEdit(self,'Körpergröße (cm)','Körpergröße',self.height),
            'Gewicht': LabeledLineEdit(self,'Gewicht (kg)','Gewicht',self.weight),
            'Muttersprache': LabeledLineEdit(self,'Muttersprache','Muttersprache',self.language),
            'Verfahren': LabeledLineEdit(self,'Verfahren','Verfahren',self.procedure),
            'Test-Ident': LabeledLineEdit(self,'Test-Ident','Test-Ident',self.testIdent),
            'Erhebungsdatum': LabeledDateEdit(self,'Erhebungsdatum','Erhebungsdatum',self.examDate),
            'Erhebungsuhrzeit': LabeledTimeEdit(self,'Erhebungsuhrzeit','Erhebungsuhrzeit',self.examTime),
            'Diagnose': LabeledLineEdit(self,'Diagnose','Diagnose',self.diagnose),
            'Befund': LabeledLineEdit(self,'Befund','Befund',self.finding),
            'Fremdbefund': LabeledLineEdit(self,'Fremdbefund','Fremdbefund',self.finding2),
            'Kommentar': LabeledTextEdit(self,'Kommentar','Kommentar',self.comment),
            #'Dateipfad': LabeledPathBrowser(self,'Dateipfad','Dateipfad',self.filePath),
        }

        self.update()
        

    def update(self):
        try: pickle
        except: import pickle
        try:
            config = {}
            with open('config','rb') as confFile:
                config = pickle.load(confFile)
        except:
            if list(config.keys()) != ['gdt','hl7','dicom']:
                config = {'gdt': [], 'hl7': [], 'dicom': []}
            
            config = {
                'gdt': self.message.mandatory,
                'hl7': ({} if config['hl7'] == {} else config['hl7']),
                'dicom': ({} if config['dicom'] == {} else config['dicom'])
                }
            with open('config','wb') as confFile:
                pickle.dump(config,confFile)

        print(self.active)
        print(config)

        for n in self.active:
            self.elements[n].remove()

        for n in config['gdt'][self.msgType.get()]:
            if n not in self.active:
                self.active.append(n)

        for n in self.active[::-1]:
            if n not in config['gdt'][self.msgType.get()]:
                self.active.remove(n)

        self.active = list(self.elements.keys())

        for n in self.active:
            self.elements[n].place()

        

    def place(self,**kwargs):
        self.container.grid(row=0,column=0)


class gdtFileTab(ttk.Frame):

    def __init__(self, parent, title=None, message=None, width=None, height=None, recentpaths=[]):
        ttk.Frame.__init__(self,parent,width=width,height=height)
        n = 0
        for i in os.listdir():
            if 'test' in i: n += 1
        self.title = (title if isinstance(title,str) and len(title)>0 else 'test%s'%n)
        if message == None: self.message = gdt2_1msg()
        else: self.message = message
        self.contentFrame = Content(self, self.message)
        self.consoleFrame = Console(self, width=64, height=8)
        self.consoleFrame.place(x=2, y=544)
        self.contentFrame.place(x=0, y=0)
        if not os.path.exists(os.environ['HOME']+'/Messages/gdt'):
            os.mkdir(os.environ['HOME']+'/Messages')
            os.mkdir(os.environ['HOME']+'/Messages/gdt')
        self.paths = [os.environ['HOME']+'/Messages/gdt/'+self.title+'.gdt'] + recentpaths

    def print(self):
        lines = self.message.validate()
        if lines[0]:
            self.consoleFrame.addLine('Warnungen:',True)
            for n,ln in enumerate(lines[1]):
                self.consoleFrame.addLine('\n%s : %s'% (n+1,ln),False)
            self.consoleFrame.addLine('\n',False)
            self.consoleFrame.addLine('\nNachricht:\n')
            for ln in lines[2]:
                self.consoleFrame.addLine('\n'+ln,False)
        else:
            self.consoleFrame.addLine('Fehler:',True)
            for n,ln in enumerate(lines[1]):
                self.consoleFrame.addLine('\n%s : %s'% (n,ln),False)
        self.consoleFrame.addLine('\n',False)

    def save(self,path):
        lines = self.message.validate()
        if lines[0]:
            if len(lines[1])>0:
                self.consoleFrame.addLine('Warnungen:',True)
                for n,ln in enumerate(lines[1]):
                    self.consoleFrame.addLine('\n%s : %s'% (n+1,ln),False)
            with open(path,'w+b') as file:
                encoding = ('cp1252' if (tmp:=self.message.fields['Zeichensatz'][1])==None
                            else ('ascii' if tmp=='1' else ('utf8' if tmp=='2' else 'cp1252')))
                for ln in lines[2]:
                    file.write(bytes(ln+'\r\n',encoding))

            self.consoleFrame.addLine('Printed to file: '+path,True)
        else:
            self.consoleFrame.addLine('File has errors! Not printed to file',True)

    def open(self,path):
        lines = self.message.validate(path=path)
        if lines[0]:
            for ln in lines[2]:
                ID = ln[3:7]
                content = ln[7:]
                for key in self.message.fields:
                    if ID == self.message.fields[key][0]:
                        self.message.fields[key][1] = content
            self.consoleFrame.addLine('Loaded from file: '+path,True)
        else:
            self.consoleFrame.addLine('File '+path+' faulty, not loaded',True)
                
    
    def pack(self, **kwargs):
        self.container.pack(**kwargs,expand=True)

class gdt2_1msg:
    
    fields = {}

    mandatory = {
        '6301': ['Satzidentifikation', 'Satzlänge', 'GDT-Version', 'Patienten-ID', 'Nachname',
                 'Vorname','Geburtsdatum'],
        '6302': ['Satzidentifikation', 'Satzlänge', 'GDT-Version', 'Patienten-ID', 'Nachname',
                 'Vorname','Geburtsdatum'],
        '6310': ['Satzidentifikation', 'Satzlänge', 'GDT-Version', 'Patienten-ID', 'Nachname',
                 'Vorname','Geburtsdatum'],
        '6311': ['Satzidentifikation', 'Satzlänge', 'GDT-Version', 'Patienten-ID']
    }

    optional = {
        '6301': ['GDT-ID-Empfänger','GDT-ID-Sender','Zeichensatz','Namenszusatz','Titel',
                 'Versicherungsnummer','Wohnort','Adresse','Versichertenart','Geschlecht',
                 'Körpergröße','Gewicht','Muttersprache'],
        '6302': ['GDT-ID-Empfänger','GDT-ID-Sender','Zeichensatz','Namenszusatz','Titel',
                 'Versicherungsnummer','Wohnort','Adresse','Versichertenart','Geschlecht',
                 'Körpergröße','Gewicht','Muttersprache','Verfahren','Test-Ident'],
        '6310': ['GDT-ID-Empfänger','GDT-ID-Sender','Zeichensatz','Namenszusatz','Titel',
                 'Versicherungsnummer','Wohnort','Adresse','Versichertenart','Geschlecht',
                 'Körpergröße','Gewicht','Muttersprache','Verfahren','Erhebungsdatum',
                 'Erhebungsuhrzeit','Diagnose','Befund','Kommentar','Fremdbefund','Kommentar',
                 'Dateipfad'],
        '6311': ['GDT-ID-Empfänger','GDT-ID-Sender','Zeichensatz','Namenszusatz','Nachname',
                 'Vorname','Geburtsdatum','Titel','Verfahren','Erhebungsdatum','Erhebungsuhrzeit']
    }

    activeFields = []

    def len3(string):
        res = '000'
        res = res[:3-len(str(len(string)+9))] + str(len(string)+9)
        return res

    def setMsgLength(self):     # call before printing to file
        self.fields['Satzlänge'][1] = 'LNGTH'

        lngth = 0
        for name in self.fields:
            if self.fields[name][1]:
                lngth += len(self.fields[name][1])+2
            
        lngth = str(lngth)
        while len(lngth)<5:
            lngth = '0' + lngth

        self.fields['Satzlänge'][1] = self.fields['Satzlänge'][1].replace('LNGTH',lngth)
        
    def __init__(self):
        self.fields = {
            'Satzidentifikation': ['8000',None],
            'Satzlänge': ['8100',None],
            'GDT-ID-Empfänger': ['8315',None],
            'GDT-ID-Sender': ['8316',None],
            'Zeichensatz': ['9206',None],
            'GDT-Version': ['9218','02.10'],
            'Patienten-ID': ['3000',None],
            'Namenszusatz': ['3100',None],
            'Nachname': ['3101',None],
            'Vorname': ['3102',None],
            'Geburtsdatum': ['3103',None],
            'Titel': ['3104',None],
            'Versicherungsnummer': ['3105',None],
            'Wohnort': ['3106',None],
            'Adresse': ['3107',None],
            'Versichertenart': ['3108',None],
            'Geschlecht': ['3110',None],
            'Körpergröße': ['3622',None],
            'Gewicht': ['3623',None],
            'Muttersprache': ['3628',None],
            'Verfahren': ['8402',None],
            'Test-Ident': ['8410',None],
            'Erhebungsdatum': ['6200',None],
            'Erhebungsuhrzeit': ['6201',None],
            'Diagnose': ['6205',None],
            'Befund': ['6220',None],
            'Fremdbefund': ['6221',None],
            'Kommentar': ['6227',None],
            'Dateipfad': ['6305',None]
        }
    
    def toFile(self,path):
        try:
            with open(path,'w+b') as file:
                for name in self.fields:
                    if self.fields[name][1]:
                        field = self.fields[name]
                        file.write(bytes(gdt2_1msg.len3(field[1])+field[0]+field[1],'cp1252'))
                        file.write(b'\r\n')
            return True
        except Exception as e:
            print(e)
            return False

    def setType(self,newType):
        if newType not in ['6301','6302','6310','6311']:
            return False

        self.fields['Satzidentifikation'][1] = newType
        self.activeFields = []
        for key in self.fields:
            if self.fields[key][1] and key in self.mandatory[newType]+self.optional[newType]:
                self.activeFields.append(key)
        self.setMsgLength()
        return True

    def setField(self,key,value):
        try:
            self.fields[key][1] = value
            if key not in self.activeFields:
                self.activeFields.append(key)
            if value == None:
                self.activeFields.remove(key)
            self.setMsgLength()
            return True
        except:
            return False

    def validate(self,path=None,lines=None):
        errors = []
        valid = True
        encoding = None
        if path:
            with open(path,'rb') as msgFile:
                content = msgFile.read()
                msg = str(content,'cp1252')

                if msg.find('92061\r\n') > -1:
                    encoding = 'ascii'
                elif msg.find('92062\r\n') > -1:
                    encoding = 'utf8'
                elif msg.find('92063\r\n') > -1:
                    encoding = 'cp1252'

                if encoding:
                    msg = str(content,encoding)
        elif lines:
            msg = "".join(lines)
        else:
            msg = ''
            fields = self.fields
            for n in fields:
                if fields[n][1]:
                    msg += gdt2_1msg.len3(fields[n][1]) + fields[n][0] + fields[n][1]
                    msg += '\r\n'

        if msg == '':
            errors.append('FATAL: empty file')
            return False,errors

        if msg.find('\r\n') == -1:
            errors.append('WARNING: wrong format for newlines in file... trying to correct that')
            msg = msg.replace('\n','\r\n')
            if msg.find('\r\n') == -1:
                errors.append('FATAL: only one line was found')
                valid = False

        lines = msg.split('\r\n')

        if '' in lines:
            lines.remove('')
        
        for i in range(len(lines)):
            if len(lines[i]) != int(lines[i][:3])-2:
                errors.append('WARNING: wrong line length info in line '+str(i+1)+'... correcting that')
                tmp = str(len(lines[i])+2)
                while len(tmp)<3:
                    tmp = '0'+tmp
                lines[i] = tmp + lines[i][3:]

        msgType = msg.find('8000')
        msgTypeLine = None
        if msgType == -1:
            errors.append('FATAL: message type not specified')
            return False,errors
        if msgType != 3 or msg[msgType-4] != '\n':
            errors.append('FATAL: message type not specified')
            return False,errors
        if msg[msgType+4:msgType+8] not in ['6301','6302','6310','6311']:
            errors.append('FATAL: unknown or unsupported message type')
            return False,errors
        else:
            msgTypeLine = lines.index(msg[msgType-3:msgType+8])
            msgType = msg[msgType+4:msgType+8]

        validFieldIDs = [self.fields[tmp][0] for tmp in self.mandatory[msgType]+self.optional[msgType]]
        validFieldIDs.remove('8000')
        foundInLines = [False for tmp in validFieldIDs]

        correct9206 = True
        correct9218 = True
        correct3110 = True

        for i in range(len(lines)-1,-1,-1):
            if i==msgTypeLine:
                pass
            else:
                validLine = False
                abortTests = False
                ID = None
                for k in range(len(validFieldIDs)):
                    if validFieldIDs[k] == lines[i][3:7]:
                        if foundInLines[k] != False:
                            errors.append('WARNING: duplicate field in lines '+str(foundInLines[k]+1)+
                                          ' and '+str(i+1)+'... removing second occurance')
                            del(lines[i])
                            abortTests = True
                            break
                        else:
                            ID = lines[i][3:7]
                            foundInLines[k] = i
                            validLine = True
                            break
                if abortTests: pass
                elif not validLine:
                    errors.append('WARNING: unknown or unsupported field ID ('+lines[i][3:7]+') in line '+str(i+1)+
                                  '... removing line')
                    del(lines[i])
                else: # rules for specific contents
                    if ID == '8100': # sentence length
                        if not len(lines[i]) == 12:
                            errors.append('WARNING: sentence length (8010) has to be a 5-digit number')
                        if not lines[i][7:].isnumeric():
                            errors.append('WARNING: sentence length (8010) has to be a numeric value but resolved to "'+
                                          lines[i][7:]+'"... correcting that')
                            correct8010 = False
                    if ID == '9206': # message encoding (must be 1,2 or 3)
                        if not lines[i][7:] in ['1','2','3']:
                            errors.append('WARNING: message encoding (9206) has to be a value of 1, 2 or 3... defaulting to 3 (ANSI cp1252)')
                            correct9206 = False
                    if ID == '9218': # gdt version (has to be '02.10')
                        if lines[i][7:] != '02.10':
                            errors.append('WARNING: message specifies unsupported GDT version ('+
                                          lines[i][7:]+' at field 9218)... changing to 02.10')
                            correct9218 = False
                    if ID in ['3103','6200']: # dates (format must be ddMMyyyy)
                        if len(lines[i]) != 15 or not lines[i][7:].isnumeric() or not 1 <= int(lines[i][9:11]) <= 12:
                            errors.append('FATAL : %s ('%('Geburtsdatum' if ID=='3103' else 'Erhebungsdatum')+
                                          ID+') : format has to be ddMMyyyy!')
                            return False,errors
                        elif int(lines[i][9:11]) in [1,3,5,7,8,10,12]:
                            if not 1 <= int(lines[i][7:9]) <= 31:
                                errors.append('FATAL : %s ('%('Geburtsdatum' if ID=='3103' else 'Erhebungsdatum')+
                                              ' ('+ID+')... format has to be ddMMyyyy!')
                                return False,errors
                        elif int(lines[i][9:11]) in [4,6,9,11]:
                            if not 1 <= int(lines[i][7:9]) <= 30:
                                errors.append('FATAL : %s ('%('Geburtsdatum' if ID=='3103' else 'Erhebungsdatum')+
                                              ' ('+ID+')... format has to be ddMMyyyy!')
                                return False,errors
                        else:
                            if not 1 <= int(lines[i][7:9]) <= 29:
                                errors.append('FATAL : %s ('%('Geburtsdatum' if ID=='3103' else 'Erhebungsdatum')+
                                              ' ('+ID+')... format has to be ddMMyyyy!')
                                return False,errors
                    if ID == '6201': # time of day (format must be hhmmss)
                        if len(lines[i]) != 13 or not lines[i][7:].isnumeric() or not 0 <= int(lines[i][7:9]) <= 23:
                            errors.append('FATAL : Erhebungsuhrzeit ('+ID+')... format has to be hhmmss!')
                            return False,errors
                        if not 0 <= int(lines[i][9:11]) <= 59:
                            errors.append('FATAL : Erhebungsuhrzeit ('+ID+')... format has to be hhmmss!')
                            return False,errors
                        if not 0 <= int(lines[i][11:13]) <= 59:
                            errors.append('FATAL : Erhebungsuhrzeit ('+ID+')... format has to be hhmmss!')
                            return False,errors
                    if ID == '3110':
                        if lines[i][7:] not in ['1','2']:
                            errors.append('WARNING: unsupported gender specified in line '+str(i+1)+'... defaulting to male (1)')
                            correct3110 = False
                    if ID == '6305':
                        try:
                            open(lines[i][7:],'rb')
                        except:
                            errors.append('WARNING: file not found (line '+str(i+1)+')')

        if not correct9206:
            for i in range(len(lines)):
                if '9206' == lines[i][3:7]:
                    lines[i] = lines[i][:7] + '3'
                    break

        if not correct9218:
            for i in range(len(lines)):
                if '9218' == lines[i][3:7]:
                    lines[i] = lines[i][:7] + '02.10'
                    break
        
        if not correct3110:
            for i in range(len(lines)):
                if '3110' == lines[i][3:7]:
                    lines[i] = lines[i][:7] + '1'
                    break

        for i in range(len(lines)):
            if '8100' == lines[i][3:7]:
                lines[i] = '0148100LNGTH'
                lngth = 0
                for ln in lines:
                    lngth += len(ln)+2

                lngth = str(lngth)
                while len(lngth)<5:
                    lngth = '0' + lngth

                lines[i] = lines[i].replace('LNGTH',lngth)

        minFields = [self.fields[tmp][0] for tmp in self.mandatory[msgType]]

        for ln in lines:
            if ln[3:7] in minFields:
                minFields.remove(ln[3:7])

        for n in range(len(minFields)):
            for k in self.fields:
                if self.fields[k][0]==minFields[n]:
                    minFields[n] = k
                    break

        if minFields != []:
            errors.append('FATAL: missing mandatory fields for message type "'+msgType+'": '+", ".join(minFields))
            return False,errors

        print()
        for n,l in enumerate(lines):
            print(n+1,'\t',l)
        print()

        return True,errors,lines
