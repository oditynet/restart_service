import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

listcheck=[]
nodeservice=[]
masterservice=[]

class SystemdRestart:
    def __init__(self, root):
        global listcheck
        self.root = root
        self.root.title("GUI nodes for restart services")
        self.root.geometry("400x600")
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
        current=0
        # Configure button layout
        masterbutton = ['Master1', 'Master2','Master3']
        nodebutton = ['Node1', 'Node2','Node3', 'Node4']

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

        self.checkbox = {}
        for btn_text in masterbutton:
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
        bar.grid(row=current+1, column=0)
        current+=1
        currentsrv+=1
        for btn_text in nodebutton:
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
        current=currentsrv

        bar = Label(check_frame, text=" ")
        bar.grid(row=current + 1, column=0)

        button = ttk.Button(check_frame,text="Restart",style="Calc.TButton", command=self.systemdrestart)
        button.grid(row=current+2, column=0, sticky='nsew')

        print(listcheck)

    def button_click(self, value):
        global listcheck
        for i in listcheck:
            if i[0] == value:
                i[1]*=(-1)
        print(listcheck)

    def systemdrestart(self):
        global listcheck
        global masterservice
        global nodeservice
        for i in listcheck:
            if i[0][:6] == "Master" and i[1] == 1:
                print(i[0])
                for srv in listcheck:
                    if srv[0] in masterservice:
                        if srv[1] == 1:
                            print("systemctl restart ",srv[0])

            elif i[0][:4] == "Node" and i[1] == 1:
                print(i[0])
                for srv in listcheck:
                    if srv[0] in nodeservice:
                        if srv[1] == 1:
                            print("systemctl restart ",srv[0])

if __name__ == "__main__":
    root = tk.Tk()
    services = SystemdRestart(root)
    root.mainloop()