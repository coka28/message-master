import sys,win32api,win32gui,win32con
from PIL import ImageGrab,Image
from time import sleep,time
import numpy as np
def getWordHandle():
    winlist,toplist = [],[]
    def enum_cb(hwnd,results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb,toplist)
    for w in winlist:
        if 'Word' in w[1]:
            return w[0]
    return None
def listHandles():
    winlist,toplist = [],[]
    def enum_cb(hwnd,results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb,toplist)
    return winlist

def getHandle(name):
    procs = {}
    for i,k in listHandles():
        if name.lower() in k.lower():
            procs[k] = i
    return procs

import matplotlib.pyplot as plt
import multiprocessing as mp
grid = 50
scrollspeed = 1100

def overlap(im1,im2,nr,L,Q,dat):
    arr1 = np.asarray(im1)
    arr1 = np.transpose(arr1,(1,0,2))
    arr1 = arr1[::grid]
    arr1 = np.transpose(arr1,(1,0,2))
    arr2 = np.asarray(im2)
    arr2 = np.transpose(arr2,(1,0,2))
    arr2 = arr2[::grid]
    arr2 = np.transpose(arr2,(1,0,2))
    minlist = []
    mindex = None

    prog = 0
    µ = min(len(arr1),len(arr2))
    for i in range(µ):
        arr1_ = np.concatenate((arr1,np.zeros((len(arr2)-(i+1),)+arr2.shape[1:],dtype='uint8')+255),axis=0)
        arr2_ = np.concatenate((np.zeros((len(arr1)-(i+1),)+arr1.shape[1:],dtype='uint8')+255,arr2),axis=0)
        diff = abs(arr1_-arr2_).sum()#*(len(arr1)+len(arr2))/(len(arr1)+len(arr2)-(i+1))
        minlist.append((str(nr),i,diff))
        if nr==0:
            dat.append(minlist[-1][2])
        if nr == -1 and i==300:
            print(arr1_,abs(arr1_-arr2_))
            im = Image.fromarray(abs(arr1_-arr2_))
            im.show()
        if mindex==None:
            mindex = i
            mini = minlist[0]
        elif minlist[mindex][2]>diff:
            mindex = i
            mini = minlist[i]
        if i/µ>prog:
            prog += 0.1/grid
            print('.',end='')
            Q.put(True)
    L.append(mini)
    return

def getDocImage(handle):
    t0 = time()
    # only grabs first instance of word in handle list
    tmp = list(zip(listHandles()))
    if 'Microsoft Office-Aktivierungs-Assistent' in tmp[1]:
        win32gui.ShowWindow(tmp[0][tmp[1].index('Microsoft Office-Aktivierungs-Assistent')],0)
    hndl = handle
    win32gui.ShowWindow(hndl,6)
    win32gui.ShowWindow(hndl,9)
    sleep(0.5)
    rect = win32gui.GetWindowRect(hndl)
    ims = []
    targetPos = rect[0]+int((rect[2]-rect[0])/2),rect[1]+int((rect[3]-rect[1])/2)
    winButtPos = (10,win32api.GetSystemMetrics(1))
    win32api.SetCursorPos(winButtPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,*winButtPos,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,*winButtPos,0,0)
    sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,*winButtPos,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,*winButtPos,0,0)
    sleep(2)
    while True:
        ims.append(ImageGrab.grab(rect))
        win32api.SetCursorPos(targetPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,*targetPos,-int(scrollspeed*7/20),0)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,*targetPos,-int(scrollspeed/4),0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,*targetPos,-int(scrollspeed/5),0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,*targetPos,-int(scrollspeed/5),0)
        sleep(0.04)
        if len(ims)>=2:
            im1 = np.asarray(ims[-1])
            im2 = np.asarray(ims[-2])
            im_ = im1-im2
            if abs(im_.sum())==0:
                del(ims[-1])
                break
    LBorders = []
    RBorders = []
    
    for im in ims:
        arr = np.asarray(im)
        needle = [int(len(arr)/2),int(len(arr[0])/2)] # y,x
        tmp = 1
        while sum(arr[needle[0]][needle[1]])!=255*len(arr[needle[0]][needle[1]]):
            needle[0] -= tmp
            if needle[0] == 0: tmp = -1
            if needle[0] == len(arr):
                im.show()
                raise Exception('something wrong with some image')
        while sum(arr[needle[0]][needle[1]])==255*len(arr[needle[0]][needle[1]]):
            needle[0] -= 1
        needle[0] += 8
        while sum(arr[needle[0]][needle[1]])==255*len(arr[needle[0]][needle[1]]):
            needle[1] -= 1
        needle[1] += 1
        LBorders.append(needle[1])
        while sum(arr[needle[0]][needle[1]])==255*len(arr[needle[0]][needle[1]]):
            needle[1] += 1
        RBorders.append(needle[1])
        
    for i in range(len(ims)):
        ims[i] = ims[i].crop((min(LBorders),0,max(RBorders),ims[i].size[1]))
    x1,x2 = min(LBorders),max(RBorders)
    maxgap = int(18*((x2-x1)/792))
    for i in range(len(ims)):
        arr = np.asarray(ims[i])
        needle = [int(len(arr)/2),0] # y,x
            
        while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
            needle[0] -= 1
        needle[0] += 1
        y1 = needle[0]
        while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
            needle[0] += 1
        needle[0] -= 1
        y2 = needle[0]
        gap1 = [None,None]
        gap2 = [None,None]
        if sum(arr[y1-maxgap][0])==255*len(arr[0][0]):
            needle[0] = y1-maxgap
            while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
                needle[0] += 1
            gap1 = [needle[0],y1]
            needle[0] -= 1
            while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
                needle[0] -= 1
            needle[0] += 1
            y1 = needle[0]
        if sum(arr[y2+maxgap][0])==255*len(arr[0][0]):
            needle[0] = y2+maxgap
            while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
                needle[0] -= 1
            needle[0] += 1
            gap2 = [y2,needle[0]]
            while sum(arr[needle[0]][needle[1]])==255*len(arr[0][0]):
                needle[0] += 1
            needle[0] -= 1
            y2 = needle[0]
        if gap1[0]!=None:
            vert = [(y1,gap1[0]),(gap1[1],y2)]
            if gap2[0]!=None:
                vert[1] = (gap1[1],gap2[0])
                vert += [(gap2[1],y2)]
        elif gap2[0]!=None:
            vert = [(y1,gap2[0]),(gap2[1],y2)]
        else:
            vert = [(y1,y2)]
        arr_ = np.concatenate(tuple(arr[v[0]:v[1]] for v in vert),axis=0)
        ims[i] = Image.fromarray(arr_)
    if len(ims)==1: imarr = np.asarray(ims[0])

    thrM = mp.Manager()
    L = thrM.list()
    Q = mp.Queue()
    global data
    data = thrM.list()
    thrds = []
    thrdNr = int(mp.cpu_count()*0.75)
    prog,n = 0,0
    
    from tkinter import Tk,Canvas
    top = Tk(None,""," Word Window Scan Assembly Progress")
    top.geometry('500x150')
    top.resizable(width=False,height=False)
    canv = Canvas(top,width=500,height=150)
    canv.create_rectangle((15,15,485,135),outline='grey45',width=3)
    text = canv.create_text(250,75,text='0 %',font=('Times New Roman',18))
    pr = canv.create_rectangle((17,13,18,133),fill='#22dd66')
    canv.pack()
    top.update_idletasks()
    top.update()
    try:    
        for i in range(len(ims)-1):
            while len(thrds)>=thrdNr:
                for k in range(len(thrds)-1,-1,-1):
                    if thrds[k].exitcode!=None:
                        thrds[k].join()
                        thrds[k].kill()
                        del(thrds[k])
                sleep(.2)


            thr = mp.Process(target=overlap,args=(ims[i],ims[i+1],i,L,Q,data))
            thrds.append(thr)
            thr.start()
            try:
                test = False
                while Q.get_nowait():
                    test = True
                    n += 0.1/(len(ims)-1)/grid
            except:
                if test:
                    canv.delete(pr)
                    canv.delete(text)
                    pr = canv.create_rectangle((17,17,int(n*466)+18,133),fill='#22dd66',width=0)
                    text = canv.create_text(250,75,text='%s'%round(n*100,2)+' %',font=('Times New Roman',18))
                    top.update_idletasks()
                    top.update()

        while True:
            try:
                test = False
                while Q.get_nowait():
                    test = True
                    n += 0.1/(len(ims)-1)/grid
            except:
                if test:
                    canv.delete(pr)
                    canv.delete(text)
                    pr = canv.create_rectangle((17,17,int(n*466)+18,133),fill='#22dd66',width=0)
                    text = canv.create_text(250,75,text='%s'%round(n*100,2)+' %',font=('Times New Roman',18))
                    top.update_idletasks()
                    top.update()
                    sleep(.1)
            if round(n,3)>=1: break
        top.destroy()
        
        for i in range(len(thrds)):
            thrds[i].join()
            thrds[i].kill()
        for i in range(len(thrds)-1,-1,-1): del(thrds[i])
    except KeyboardInterrupt:
        top.destroy()
        for i in range(len(thrds)-1,-1,-1):
            thrds[i].kill()
            del(thrds[i])
        print('!aborted!')
        return
    res = {}
    while True:
        try:
            tmp = L.pop(0)
        except:
            print('blubb.. empty queue')
            break
        res[tmp[0]] = tmp[1]
        print('.',end='')

    vert = []
    tmp = 0
    arrs = [np.asarray(im) for im in ims]

    for i in range(len(ims)):
        if i == 0:
            pass
        else:
            vert.append((res[str(i-1)],ims[i].size[1]))

    imarr = np.asarray(ims[0])
    for v,ar in zip(vert,arrs[1:]):
        imarr = np.concatenate((imarr,ar[v[0]:v[1]]), axis=0)
        
    a = Image.fromarray(imarr)
    print('runtime : %s'%round(time()-t0,2)+'s')
    return a
