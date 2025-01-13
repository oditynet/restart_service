import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label
import os
import paramiko
parami=1

#version=0.1.1

port = 22
username = 'root'
password = 'root'

#ansiblestring=" ansible_connection=ssh ansible_ssh_user=root ansible_ssh_pass=root\n"

listcheck=[]
nodeservice=[]
masterservice=[]
masterbutton=[]
nodebutton=[]

class SystemdRestart:
    def __init__(self, root):
        global masterbutton
        global nodebutton
        # masterbutton = ['Master1', 'Master2','Master3']
        # nodebutton = ['Node1', 'Node2','Node3', 'Node4']
        m=0
        with open('hosts') as f:
            for text in f:
                text = text.rstrip('\n').split()
                if text[0] == "[masters]":
                    m=1
                    n=1
                    continue
                if text[0] == "[nodes]":
                    m=2
                    n=1
                    continue
                if m == 1:
                    masterbutton.append(("Master"+str(n),text[0]))
                    n+=1
                if m == 2:
                    nodebutton.append(("Node" + str(n),text[0]))
                    n+=1

        print(masterbutton)
        print(nodebutton)
        global listcheck
        self.root = root
        self.root.title("GUI nodes for restart services")
        self.root.geometry("400x900")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)

        # Configure styles
        style = ttk.Style()
        style.configure("Display.TEntry",
                       padding=10,
                       font=('Arial', 20))
        
        style.configure("Calc.TButton",
                       padding=10,
                       font=('Arial', 14, 'bold'),
                       width=8)

        # Main display frame
        display_frame = ttk.Frame(root, padding="20 20 20 10")
        display_frame.pack(fill='x')

        # Button frame
        check_frame = ttk.Frame(root, padding="20 10 20 20")
        check_frame.pack(fill='both', expand=True)

        masterservice.append('zookeeper')
        masterservice.append('hive-metastore')
        masterservice.append('hive-server2')
        masterservice.append('hadoop-hdfs-namenode')
        masterservice.append('hadoop-hdfs-journalnode')
        masterservice.append('hadoop-hdfs-zkfc')
        masterservice.append('hbase-master')

        nodeservice.append('hadoop-yarn-nodemanager')
        nodeservice.append('hadoop-hdfs-datanode')
        nodeservice.append('hbase-regionserver')
        nodeservice.append('solr-server')

        current = 0
        self.checkbox = {}
        for btn_text,ipddr in masterbutton:
            current+=1
            listcheck.append([btn_text,-1])
            checkbox = ttk.Checkbutton(check_frame,text=btn_text,command=lambda x=btn_text: self.button_click(x))
            checkbox.grid(row=current, column=0, sticky='new')
            self.checkbox[btn_text] = checkbox
        currentsrv=0
        for btn_text in masterservice:
            currentsrv+=1
            listcheck.append([btn_text,-1])
            checkbox = ttk.Checkbutton(check_frame,text=btn_text,command=lambda x=btn_text: self.button_click(x))
            checkbox.grid(row=currentsrv, column=2, sticky='new')
            self.checkbox[btn_text] = checkbox
        current=currentsrv
        bar = Label(check_frame, text=" ")
        current += 1
        currentsrv += 1
        bar.grid(row=current, column=0)
        for btn_text,ipddr in nodebutton:
            current+=1
            listcheck.append([btn_text,-1])
            checkbox = ttk.Checkbutton(check_frame,text=btn_text,command=lambda x=btn_text: self.button_click(x))
            checkbox.grid(row=current, column=0, sticky='new')
            self.checkbox[btn_text] = checkbox

        for btn_text in nodeservice:
            currentsrv+=1
            listcheck.append([btn_text,-1])
            checkbox = ttk.Checkbutton(check_frame,text=btn_text,command=lambda x=btn_text: self.button_click(x))
            checkbox.grid(row=currentsrv, column=2, sticky='new')
            self.checkbox[btn_text] = checkbox
        if current < currentsrv:
            current=currentsrv
        current += 1

        bar = Label(check_frame, text=" ")
        bar.grid(row=current, column=0)
        current += 1

        button = ttk.Button(check_frame,text="Restart",style="Calc.TButton", command=self.systemdrestart)
        button.grid(row=current, column=0, sticky='nsew')

        #print(listcheck)

    def button_click(self, value):
        global listcheck
        for i in listcheck:
            if i[0] == value:
                i[1]*=(-1)
        #print(listcheck)

    def systemdrestart(self):
        global listcheck
        global masterservice
        global nodeservice
        global masterbutton
        global nodebutton
        global parami

        #ansfile = open('inventory', 'w')
        #ansfile.write("[all]\n")
        for i in listcheck:
            if i[0][:6] == "Master" and i[1] == 1:
                print("On ",i[0])
                for host,ipaddr in masterbutton:
                    if host == i[0]:
                        #print("ip ",ipaddr)
                        break
                for srv in listcheck:
                    if srv[0] in masterservice:
                        if srv[1] == 1:
         #                   ansfile.write(ipaddr+ansiblestring)
                            #print("systemctl restart ",srv[0])
                            if parami == 1:
                                paramiko.util.log_to_file('paramiko.log')
                                s = paramiko.SSHClient()
                                s.load_system_host_keys()
                                s.connect(ipaddr, port, username, password, timeout=7)
                                stdin, stdout, stderr = s.exec_command(' systemctl restart {srv[0]}')
                                print(stdout.read())
                                s.close()
                            else:
                                print(subprocess.Popen(f"ssh , timeout=7 root@{ipaddr} systemctl restart {srv[0]}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate())
                            #cmd="ssh root@"+ipaddr+" systemctl restart "+srv[0]
                            #print(cmd)
                            #os.system(cmd)

            elif i[0][:4] == "Node" and i[1] == 1:
                print("On ",i[0])
                for host,ipaddr in nodebutton:
                    if host == i[0]:
                        #print("ip ",ipaddr)
                        break
                for srv in listcheck:
                    if srv[0] in nodeservice:
                        if srv[1] == 1:
          #                  ansfile.write(ipaddr + ansiblestring)
                            if parami == 1:
                                paramiko.util.log_to_file('paramiko.log')
                                s = paramiko.SSHClient()
                                s.load_system_host_keys()
                                s.connect(ipaddr, port, username, password, timeout=7)
                                stdin, stdout, stderr = s.exec_command(' systemctl restart {srv[0]}')
                                print(stdout.read())
                                s.close()
                            else:
                                print(subprocess.Popen(f"ssh , timeout=7 root@{ipaddr} systemctl restart {srv[0]}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate())
                            #cmd = "ssh root@"+ipaddr+" systemctl restart "+srv[0]
                            #print(cmd)
                            #os.system(cmd)
                            #print("systemctl restart ",srv[0])

if __name__ == "__main__":
    root = tk.Tk()
    services = SystemdRestart(root)
    root.mainloop()
