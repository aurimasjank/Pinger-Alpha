import json
import os
import time
import subprocess
import datetime
import smtplib
from tkinter.ttk import Separator, Style
from operator import itemgetter
from email.mime.text import MIMEText
from tkinter import *
import tkinter.messagebox as tkMessageBox
from tkinter import ttk
import sys
def savefile(d):
    dic= {}
    with open('test.json', 'w') as fp:
        for elem in d:
            json.dump({elem["name"]:{elem["status"]:elem["ip"]}}, fp)
            fp.write('\n')
        fp.close
def savestatistics(name):
	with open(name+".txt", "a+") as out:
		try:
			out.write(str(subprocess.check_output("ping -n 1 " + name)))
			out.write("\n")
		except:
			pass
	out.close()
# def readprobar():
    # d=[]
    # with open('probar.json', 'r') as f:
        # for line in f:
            # d=json.loads(line)
        
        # f.close()

        # return d
def print(err):
	with open("print.txt", "a+") as rr:
		rr.write(err)
		rr.close()
def compresion(name,datachck):
	lcnt = 0
	lines = 0
	check = False
	with open(name + ".txt", "r") as cm:
		lines = cm.readlines()
		cm.close()
	if len(lines)>20 :
		with open(name+".txt", "w") as cc:
			
			if datachck == 10 :
				n=2
			else:
				n=1
			lines = lines[n:]
			for item in lines:
				cc.write(item)
			cc.close()

def print():
    try:
        with open("print.txt", "r") as rr:
            err = rr.read()
            return err
            rr.close()
    except: 
        with open("print.txt", "w+") as rr:
            rr.close()


def openfile():
    d={}
    lists=[]
    with open('test.json', 'r') as f:
        for line in f:
            line_ = json.loads(line)
            name = list(line_.keys())[0]
            status = list(line_[name].keys())[0]
            ip = line_[name][status]
            d[name] = {'name':name, "status":status, 'ip':ip}
        f.close()
        for ele in d:
            lists.append(d[ele])
        return lists
#GUI main class		
class GUI(Tk):
    def __init__(self):
        self.tk = Tk()
        self.Firstgo=True
        self.timespend = 0
        self.tk.wm_title("Web Service")
        self.tk.configure(background='black')
        #self.tk.wm_state('zoomed')
        self.tk.attributes("-fullscreen",True)
        #Frames
        self.tk.columnconfigure(0, weight=1)
        self.tk.rowconfigure(0, weight=1)
        self.left= Frame(self.tk, bg="black")
        self.left.grid(column=0, row = 0, pady=5 ,padx=10, sticky=N)
        
        #self.center = Frame (self.tk ,bg= "black")
        #self.center.grid(column=1, row = 0, padx=10, sticky=N+S+E+W )
        
        self.center = Separator(self.tk, orient="vertical")
        self.center.grid(column=1, row=0, sticky="ns")
        
        sty = Style(self.center)
        sty.configure("TSeparator", background="#00CC00")
        
        self.right= Frame(self.tk, bg="black")
        self.right.grid(column=2, row = 0, pady=5,padx=10, sticky=N)

        self.probar= Frame(self.tk, bg= "black")
        self.probar.grid(column=1, row = 1, sticky= S)
        
        self.botFrame = Frame(self.tk, bg="black")
        self.botFrame.grid(column=2, row = 1, pady=5, sticky= S)
        
        self.colnr = 0
        self.rownrleft = 0
        self.rownrright = 0

        self.titlelbl= Label(self.right, text="Service Status:",bg="black", fg="#00CC00",font=("Helvetica", 24))
        self.titlelbl2= Label(self.left, text="GW Status:",bg="black", fg="#00CC00",font=("Helvetica", 24))
        self.titlelbl.grid(column=0, row = 0,sticky=N)        
        self.titlelbl2.grid(column=0, row = 0,sticky=N)
        
        #self.probars=readprobar()
        self.statuslabel = Label(self.botFrame, text="Script status :  ", bg="black",fg="#00CC00", font=("Helvetica", 24))
        self.statuslabel.grid(column=0, row = 0)
        

        
        self.progress = ttk.Progressbar(self.probar,orient ="horizontal",length = 410, mode ="determinate")
        self.progress.grid(column=0, row = 0,pady= (20,0))
        
        self.string = StringVar()
        self.timecount = StringVar()
    
        
        self.titlelbl3= Label(self.probar, textvariable= self.string ,bg="black", fg="#00CC00",font=("Helvetica", 24))
        self.titlelbl3.grid(column=0, row = 1)
        
        self.statuscount1 = Label(self.botFrame, text="Pinger last run in :",fg="#00CC00", bg="black", font=("Helvetica", 24))
        self.statuscount1.grid(column=0, row = 0)
        
        self.statuscount = Label(self.botFrame, textvariable=self.timecount,fg="#00CC00", bg="black", font=("Helvetica", 24))
        self.statuscount.grid(column=0, row = 1)
        
        
        
        
        self.tk.after(1000, self.task)
        self.label = {}
        self.statuscount = 0
        self.freezecheck = 0


    def task(self):
    
        i = 0
        self.list=[]
        #self.probars=readprobar()
        self.probarcount=0
        self.string.set (str(self.probarcount) + " / " +str(len(self.list)*10))
        self.progress["value"] = self.probarcount
        
        self.progress["maximum"] = len(self.list)*10
        self.right
        #err=str( print() )

        
        self.list = openfile()
        name=""
        if self.label != {}:#deleting previous information that we could refresh
            for ele in self.label:

                self.label[ele].destroy()
        self.label= {}
        whatframe = self.right
        whatrow= self.rownrright
        self.list = sorted(self.list, key=itemgetter('status'))
        for elem in self.list:#creating visual status if server is online text is in color green and opsite red
            
            if "_VPN" in elem["name"]:
                whatframe = self.left
                whatrow= self.rownrleft
                name=elem["name"][:-4]
                self.rownrleft+=1
                
                
            else :
                whatframe = self.right
                whatrow= self.rownrright
                self.rownrright+=1
                name=elem["name"]
            if elem["status"]=="true":
                lb = Label(whatframe,text=name , fg="#00CC00",bg="black", font=("Helvetica", 28))
            if elem["status"]=="false":
                lb = Label(whatframe,text=name, fg="black",bg="#00CC00", font=("Helvetica", 28))
            lb.grid(column= 0, row = whatrow ,pady=10 , sticky= W+E)	
            
            self.label[elem["name"]] = lb
            
        #lastrun = pingervalidation()
        
        # if lastrun == 'True':
            # self.timespend = 0
            # self.freezecheck += 1
            # self.timecount.set (str(self.timespend))

        # else: 
            # self.timespend += 1
            # self.freezecheck1 = 0
            # self.timecount.set (str(self.timespend))


        self.wd=self.tk.winfo_reqwidth()
        self.wdd=self.tk.winfo_width()

        self.fwidth = self.wdd/5
        self.left.columnconfigure(0,minsize=self.fwidth*2)

        self.right.columnconfigure(0,minsize=self.fwidth*2)

        self.center.columnconfigure(0,minsize=self.fwidth)

        self.tk.after(1000, self.Pinger)#Program refresh main window works every 5s
		
    def Pinger(self):
        #self.self.list
        xcount=0
        DETACHED_PROCESS = 8
        for ele in self.list:
            cnt=0
            recieved = 0
            hostname = ele["ip"]
            datachck=0
            if ele["status"] == "true": # checks if website previuosly was online in last cycle
                while cnt < 10: # checks 10 times if website is reachable
                    datachck+=1
                    if datachck == 11:
                        datachck =0
                    response = subprocess.call("ping -n 1 " + hostname, creationflags=DETACHED_PROCESS)    
                    #response = os.system("ping -n 1 " + hostname)
                    savestatistics(hostname)
                    print(hostname)
                    print(response)
                    compresion(hostname,datachck)
                    cnt+=1
                    if cnt == 10: 
                        timestamp(hostname)
                    if response == 0:
                        recieved+=1
                        
                    else:
                        recieved-=1
                    xcount+=1
                    #probar(xcount,len(dict)*10)
                    
                if recieved < 8 : 
                    ele["status"] = "false"
                    gmail_user = 'email@gmail.com'
                    gmail_pwd = 'password'
                    FROM = "sender@gmail.com"
                    TO = "reciever@compensalife.lt"
                    SUBJECT = "subject"
                    TEXT = (ele["name"],hostname, 'is down!')
                    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
                    """ % (FROM , TO , SUBJECT, TEXT)
                    try:
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.ehlo()
                        server.starttls()
                        server.login(gmail_user, gmail_pwd)
                        server.sendmail(FROM, TO, message)
                        server.close()
                    except:
                        print("failed to send mail")
                else: 
                    continue
            else:
                
                try: #If server was offline it checks if server came back online
                    serverback=0
                    for i in range(10):
                        #responsecheck = subprocess.call("ping -n 1 " + hostname, creationflags=DETACHED_PROCESS)
                        responsecheck =  os.system("ping " + hostname)
                        
                        if responsecheck == 0:
                            serverback+=1
                        else:
                            print ("server is still down")
                        if serverback > 8 :
                            ele["status"] = "true"
                except:
                    pass
                    #print("Failed verify offline server")
                xcount+=10
                #probar(xcount,len(dict)*10)
        try:
            savefile(sorted(self.list, key=itemgetter('status'), reverse=True))
        except:
            print("Program Failed")

        self.tk.after(1000, self.task)
	
#forever loop
Gui= GUI()
Gui.mainloop()

