from Tkinter import *
import socket
import sys
import tkMessageBox
import ttk
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global_username = ""

def onClose(master):
        
    message = "logout"
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.strip().split()
    master.destroy()
    print >>sys.stderr, 'onCLose'
    return 1
    
def controlClose(master):
    result = tkMessageBox.askquestion("Close", "Are You Sure?", icon='warning')
    if result == 'yes':
        onClose(master)
    else:
        return 0    

def initListUser(listboxUser):
    listboxUser.delete(0, END)
    message = "DAFTARGR"
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.split()
    print data
    
    for i in range(len(data)):
        if data[i] in ['0005']:
            continue
        else:
            listboxUser.insert(i-1, data[i])
    
    print listboxUser.get(0, END)
    return 1
    
def initListGroup(listboxGroup):
    listboxGroup.delete(0, END)
    message = "DAFTARUS"
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.split()
    print data
    
    for i in range(len(data)):
        print "on for"
        if data[i] in ['0004']:
            continue
        else:
            listboxGroup.insert(i-1, data[i])
    
    return 1

def recvMessage(textMessage, username):
    while True:
        print "on while recv message"
        data = client_socket.recv(1024)
        data = data.split(":")
        print data
        if data[0] == username:
            textMessage.insert(END, username+" say : "+data[1])
            textMessage.see("end")
            print "1"
        elif data[0] == "0001\n":
            flag == 0
            print "2"
            break
        elif data[0] == "3331\n":
            continue
    print "thread destroyed : "+username
    return 1

def sendMessage(master, recipient):   
    #main frame    
    mainframe = master.winfo_children()
    frames = mainframe[0].winfo_children()
    
    #get scrollbar widget    
    widget = frames[0].winfo_children()
    scrollbar=widget[0]   
    
    #get text widget
    widget=widget[1]        
    
    #get entry widget    
    entry = frames[1].winfo_children()
    entry = entry[0]
    
    #get message    
    msg = entry.get()
    entry.delete(0, 'end')    
    
    #send message
    
    message = "SEND "+recipient+" "+msg
    client_socket.sendall(message)

    widget.insert(END, "You say : "+msg+"\n")  
    widget.see("end")       
    
    return 1
    
def closeRoom(master, thread):
    print "1"
    master.destroy()
    client_socket.sendall("DUMP") 
    print "2"
    return 1

def sendGroup(master, groupname):
    #main frame    
    mainframe = master.winfo_children()
    frames = mainframe[0].winfo_children()
    
    #get scrollbar widget    
    widget = frames[0].winfo_children()
    scrollbar=widget[0]   
    
    #get text widget
    widget=widget[1]        
    
    #get entry widget    
    entry = frames[1].winfo_children()
    entry = entry[0]
    
    #get message    
    msg = entry.get()
    entry.delete(0, 'end')    
    
    #send message
    
    message = "SENDG "+groupname+" "+msg
    client_socket.sendall(message)

    widget.insert(END, "You say : "+msg+"\n")  
    widget.see("end")       
    
    return 1
    
def recvGroup(textMessage, groupname, client_username):
    while True:
        print "on while recv message"
        data = client_socket.recv(1024)
        data = data.split("(")
        print data
        if data[0] == groupname:
            message = data[1].split(")")
            username = message[0]
            print username
            print client_username
            if username == client_username:
                continue
            else:
                message = message[1].split(":")
                message = message[1].split("\n")
                msg = message[0]
                
                textMessage.insert(END, username+" say : "+msg+"\n")
                textMessage.see("end")
                print "1"
        elif data[0] == "0001\n":
            print "2"
            break
        elif data[0] == "3331\n":
            continue
        else:
            continue
    print "thread destroyed : "+groupname
    return 1

def showGroup(event, username):
    widget = event.widget    
    
    print "username : "+username    
    
    selection = widget.curselection()
    groupname = widget.get(selection[0])
    print groupname
    
    #join grup sebelum melakukan chat dengan group
    respon = tkMessageBox.askquestion("Join Group", "You will automatically join the group. Are you sure?")
    if respon == 'no':
        return 0
    
    message = "JOING "+groupname
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    
    top = Tk()
    top.title(groupname)
    
    mainframe = Frame(top, bd=10)
    mainframe.pack()
    
    frameMessage = Frame(mainframe, bd = 5)
    frameMessage.pack()
    frameInput = Frame(mainframe, bd = 5)
    frameInput.pack()    
    
    scrollbar = Scrollbar(frameMessage)
    scrollbar.pack(side=RIGHT, fill=Y)
    textMessage = Text(frameMessage, yscrollcommand=scrollbar.set, width=40, height=20)
    textMessage.pack()  
    scrollbar.config(command=textMessage.yview)
    
    s = threading.Thread(target=recvGroup, args=(textMessage, groupname, username))
    s.start()    
    
    entry = Entry(frameInput, width=30)
    entry.pack(side=LEFT)
    buttonSend = Button(frameInput, text="Send", command= lambda:sendGroup(top, groupname))
    buttonSend.pack(side=LEFT)
    
    top.protocol("WM_DELETE_WINDOW", lambda: closeRoom(top, s))
    
    top.mainloop()    
    
    return 1
  
def showRoom(event):
    widget = event.widget    
    
    selection = widget.curselection()
    username = widget.get(selection[0])
    print username
    
    top = Tk()
    top.title(username)
    
    mainframe = Frame(top, bd=10)
    mainframe.pack()
    
    frameMessage = Frame(mainframe, bd = 5)
    frameMessage.pack()
    frameInput = Frame(mainframe, bd = 5)
    frameInput.pack()    
    
    scrollbar = Scrollbar(frameMessage)
    scrollbar.pack(side=RIGHT, fill=Y)
    textMessage = Text(frameMessage, yscrollcommand=scrollbar.set, width=40, height=20)
    textMessage.pack()  
    scrollbar.config(command=textMessage.yview)
    
    s = threading.Thread(target=recvMessage, args=(textMessage, username))
    s.start()    
    
    entry = Entry(frameInput, width=30)
    entry.pack(side=LEFT)
    buttonSend = Button(frameInput, text="Send", command= lambda:sendMessage(top, username))
    buttonSend.pack(side=LEFT)
    
    top.protocol("WM_DELETE_WINDOW", lambda: closeRoom(top, s))
    
    top.mainloop()    
    
    return 1

def onCreateGroup(master, groupname):
    message = "BUATG "+groupname
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.split()
    if data[0] in ['4441']:
        respon = tkMessageBox.showinfo("Berhasil", "Group berhasil dibuat, Ok utk melanjutkan")
        if respon == 'ok':
            master.destroy()
    elif data[0] in ['4442']:
        respon = tkMessageBox.showinfo("Gagal", "Nama group telah terpakai")
    
    return 1

def controlCreateGroup(master):
    
    top = Tk()
    top.title("Create Group")
    
    mainframe = Frame(top, bd=10)
    mainframe.pack()
    
    entryName = Entry(mainframe, width=20)
    entryName.pack()
    
    buttonCreate = Button(mainframe, text="Create", command=lambda:onCreateGroup(top, entryName.get()))
    buttonCreate.pack()
    
    return 1

def showDashboard(username):
    top = Tk()
    top.title("Dashboard Chat-EK2")
    top.protocol("WM_DELETE_WINDOW", lambda:controlClose(top))
    
    
    
    #border luar
    topframe = Frame(top, bd=10)    
    topframe.pack()    
    
    #notebook
    notebook = ttk.Notebook(topframe)    
    
    #notebook page 1
    mainframe = Frame(notebook, bd = 10)
    mainframe.pack()    
    
    labelFrame = LabelFrame(mainframe, text="Basic Info", font=("Calibri", 9), width=20)
    labelFrame.pack()
    
    frameUser = Frame(labelFrame, bd=5)
    frameUser.pack()

    labelUser = Label(frameUser, text="Login as")
    labelUser.pack(side=LEFT)
    infoUser = Label(frameUser, text=": "+username) 
    infoUser.pack(side=LEFT)
    
    frameLabelList = Frame(mainframe, bd = 5)    
    frameLabelList.pack()    
    
    frameListUser = Frame(mainframe, bd=5)
    frameListUser.pack()    
    
    labelListUser = Label(frameLabelList, text="Online User :")
    labelListUser.pack(side = LEFT)
            
    scrollbar = Scrollbar(frameListUser)
    scrollbar.pack( side = RIGHT, fill=Y)    
    
    listboxUser = Listbox(frameListUser, yscrollcommand = scrollbar.set, height=5, width=20)    
    listboxUser.bind('<<ListboxSelect>>', showRoom)    
    buttonRefresh = Button(frameLabelList, text="Refresh", command=lambda:initListUser(listboxUser) )
    buttonRefresh.pack(side = LEFT)    
    
    initListUser(listboxUser)
    listboxUser.pack()
     
    
     
    scrollbar.config(command = listboxUser.yview)    
    
    notebook.add(mainframe, text="Private")
    
    #notebook page 2
    mainframe = Frame(notebook, bd = 10)
    mainframe.pack()    
    
    labelFrame = LabelFrame(mainframe, text="Basic Info", font=("Calibri", 9), width=20)
    labelFrame.pack()
    frameUser = Frame(labelFrame, bd=5)
    frameUser.pack()

    labelUser = Label(frameUser, text="Login as")
    labelUser.pack(side=LEFT)
    infoUser = Label(frameUser, text=": "+username) 
    infoUser.pack(side=LEFT)
    
    frameLabelList = Frame(mainframe, bd = 5)    
    frameLabelList.pack()    
    
    frameListUser = Frame(mainframe, bd=5)
    frameListUser.pack()
    labelListUser = Label(frameLabelList, text="Group List :")
    labelListUser.pack(side=LEFT)
    
    
    scrollbar = Scrollbar(frameListUser)
    scrollbar.pack( side = RIGHT, fill=Y)    
    
    listboxGroup = Listbox(frameListUser, yscrollcommand = scrollbar.set, height=5, width=20)
    listboxGroup.bind('<<ListboxSelect>>', lambda event: showGroup(event, username))
    
    buttonRefresh = Button(frameLabelList, text="Refresh", command=lambda:initListGroup(listboxGroup) )
    buttonRefresh.pack(side = LEFT)    
        
    initListGroup(listboxGroup)
    listboxGroup.pack()
    
    scrollbar.config(command = listboxGroup.yview)     
    
    buttonCreate = Button(mainframe, text="Create Group", command=lambda:controlCreateGroup(top))
    buttonCreate.pack()    
    
    notebook.add(mainframe, text="Group")
    notebook.pack()
    top.mainloop()

def controlLogin(master):
    mainframe = master.winfo_children()
    frames = mainframe[0].winfo_children()
    widgets = frames[0].winfo_children()    
    username = widgets[1].get()
    widgets = frames[1].winfo_children()
    password = widgets[1].get()
    print >>sys.stderr, 'message: '+username
    print >>sys.stderr, 'password: '+password
    
    message = 'MASUK '+username+' '+password
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.strip().split()
    if data[0] in ['2221']:
        master.destroy()
        global_username = username
        showDashboard(username)
    elif data[0] in ['2222']:
        tkMessageBox.showinfo("Error", "Username atau password salah")
    elif data[0] in ['0003']:
        tkMessageBox.showinfo("Error", "Akun \""+username+"\" sedang login")
        
    return 1

def controlRegister(master):
    mainframe = master.winfo_children()
    frames = mainframe[0].winfo_children()
    widgets = frames[0].winfo_children()    
    username = widgets[1].get()
    widgets = frames[1].winfo_children()
    password = widgets[1].get()
    widgets = frames[2].winfo_children()
    repassword = widgets[1].get()
    print >>sys.stderr, 'message: '+username
    print >>sys.stderr, 'password: '+password
    print >>sys.stderr, 'repass: '+password
    
    if password == repassword:
        message = "SIGNUP "+username+" "+password
        client_socket.sendall(message)
        data = client_socket.recv(1024)
        data = data.strip().split()
        if data[0] in ['1111']:
            respon = tkMessageBox.showinfo("Berhasil", "Registrasi akun berhasil")
            if respon == 'ok':
               showHome(master)
            else:
                print "not oke"
        elif data[0] in ['1112']:
            tkMessageBox.showinfo("Error", "Username sudah ada")
        else:
            tkMessageBox.showinfo("Error", "Unknown error")
    else:
        tkMessageBox.showinfo("Registrasi", "Password tidak cocok")
    return 1
    
def showRegister(master):
    master.destroy()    
    top = Tk()
    top.title("Registration")  
    top.protocol("WM_DELETE_WINDOW", lambda: controlClose(top))    

    mainframe = Frame(top, bd = 10)
    mainframe.pack()
    frame = Frame(mainframe, bd = 5)
    frame.pack()
    frameBottom = Frame(mainframe, bd = 5)
    frameBottom.pack(side = TOP)
    frameBottom2 = Frame(mainframe, bd = 5)
    frameBottom2.pack(side = TOP)
    frameButton = Frame(mainframe, bd = 5)
    frameButton.pack(side = TOP)
    
    L1 = Label(frame, text="User Name", width=10)
    L1.pack( side = LEFT)
    E1 = Entry(frame, bd =2)
    E1.pack(side = LEFT)
    
    L2 = Label(frameBottom, text="Password", width=10)
    L2.pack( side = LEFT)
    E2 = Entry(frameBottom, bd =2)
    E2.pack(side = LEFT)
    
    L3 = Label(frameBottom2, text="Retype Pass", width = 10)
    L3.pack(side=LEFT)
    E3 = Entry(frameBottom2, bd =2)
    E3.pack(side = LEFT)
    
    buttonRegister = Button(frameButton, text=("Register"), font=("Calibri", 9), command=lambda: controlRegister(top)) 
    buttonRegister.pack(side=LEFT)
    buttonCancel = Button(frameButton, text=("Cancel"), font=("Calibri", 9), command=lambda: showHome(top))
    buttonCancel.pack(side=LEFT)    
    top.mainloop()

def showLogin(master):
    master.destroy()    
    top = Tk()
    top.title("Login")  
    top.protocol("WM_DELETE_WINDOW", lambda: controlClose(top))    
    
    mainframe = Frame(top, bd = 10)
    mainframe.pack()
    frame = Frame(mainframe, bd = 5)
    frame.pack()
    frameBottom = Frame(mainframe, bd = 5)
    frameBottom.pack(side = TOP)
    frameButton = Frame(mainframe, bd = 5)
    frameButton.pack(side = TOP)
    
    L1 = Label(frame, text="User Name", width=10)
    L1.pack( side = LEFT)
    E1 = Entry(frame, bd =2)
    E1.pack(side = LEFT)
    
    L2 = Label(frameBottom, text="Password", width=10)
    L2.pack( side = LEFT)
    E2 = Entry(frameBottom, bd =2)
    E2.pack(side = LEFT)
    
    buttonLogin = Button(frameButton, text=("Login"), font=("Calibri", 9), command=lambda: controlLogin(top)) 
    buttonLogin.pack(side=LEFT)
    buttonCancel = Button(frameButton, text=("Cancel"), font=("Calibri", 9), command=lambda: showHome(top))
    buttonCancel.pack(side=LEFT)    
    top.mainloop()
    
def showHome(master):
    master.destroy()
    top = Tk()
    top.title("Chat EK-2")
    top.minsize(200, 150)
    top.maxsize(200, 150)        
    #top.protocol("WM_DELETE_WINDOW", onClose)    
        
    frameFill = Frame(top, height=30)
    frameFill.pack()
        
    frameLogin = Frame(top)
    frameLogin.pack()
    frameRegister = Frame(top)
    frameRegister.pack(side = TOP)    
    
    loginButton = Button(frameLogin, text="Login", width=10, height=2, font=("Calibri", 9), command=lambda: showLogin(top))
    loginButton.pack(side = TOP)
    registerButton = Button(frameRegister, text="Register", width=10, height=2,font=("Calibri", 9), command=lambda: showRegister(top))
    registerButton.pack(side = TOP)    
    
    top.mainloop()

def controlConnect(master):
    mainframes = master.winfo_children()
    frames = mainframes[0].winfo_children()

    widgets = frames[0].winfo_children()    
    address = widgets[1].get()
    
    widgets = frames[1].winfo_children()
    port = widgets[1].get()
    
    print "parameter : "+address+" "+port    
    
    try: 
        server_address = (address, int(port))
        client_socket.connect(server_address)
        print "koneksi sukses"
        
        showHome(master)
    except:
        print "koneksi gagal"
        tkMessageBox.showinfo("Info", "Connection error!")

def initialize():
    top = Tk()
    top.title("Chat EK-2")
    
    frame = Frame(top, bd=5)
    frame.pack()
    frameServerAddress = Frame(frame, bd=5)
    frameServerAddress.pack()
    frameServerPort = Frame(frame, bd=5)
    frameServerPort.pack(side = TOP)
    frameButton = Frame(frame, bd=5)
    frameButton.pack(side=TOP)    
    
    labelAddress = Label(frameServerAddress, text=("Server Address"), width = 15, justify=LEFT)
    labelAddress.pack(side=LEFT)
    labelPort = Label(frameServerPort, text=("Server Port"), width = 15, justify=LEFT)
    labelPort.pack(side=LEFT)
    
    entryAddress = Entry(frameServerAddress, bd=2)
    entryAddress.pack(side=LEFT)
    entryPort = Entry(frameServerPort, bd=2)
    entryPort.pack(side=LEFT)
    
    buttonConnect = Button(frameButton, text=("Connect"), command=lambda: controlConnect(top))
    buttonConnect.pack(side=TOP)    
    
    top.mainloop()    
    
initialize()

'''
Note:
1. fungsi tidak di return sebelum fungsi lain di return

'''