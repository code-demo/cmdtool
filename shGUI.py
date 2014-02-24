#the other guys GUI
from Tkinter import *
from os import system as cmd

root = Tk()
termf = Frame(root, height=700, width=1000)
termf.pack(fill=BOTH, expand=YES)
wid = termf.winfo_id()

f=Frame(root)
Label(f,text="/dev/pts/").pack(side=LEFT)
tty_index = Entry(f, width=3)
tty_index.insert(0, "1")
tty_index.pack(side=LEFT)
Label(f,text="Command:").pack(side=LEFT)
e = Entry(f)
e.insert(0, "ls -l")
e.pack(side=LEFT,fill=X,expand=1)

def send_entry_to_terminal(*args):
    """*args needed since callback may be called from no arg (button)
   or one arg (entry)
   """
    command=e.get()
    tty="/dev/pts/%s" % tty_index.get()
    cmd("%s <%s >%s 2> %s" % (command,tty,tty,tty))

e.bind("<Return>",send_entry_to_terminal)
b = Button(f,text="Send", command=send_entry_to_terminal)
b.pack(side=LEFT)
f.pack(fill=X, expand=1)

cmd('xterm -into %d -geometry 160x50 -sb -e "ls; sh" &' % wid)

root.mainloop()