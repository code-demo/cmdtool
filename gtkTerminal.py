from Tkinter import*
import xml
from xml import *
from xml.dom import minidom
from pprint import pprint
from datetime import datetime
import os
from subprocess import call

# helper functions

def mp(goal,content):
	print "-----BEGIN-----"
	print "[debug]"
	print goal
	print content
	print "[debug]"
	print "-----END-----"

def printdg(content):
	print "-----BEGIN-----"
	print "[debug]" + content
	print "-----END-----"


class Notebook(Frame):
    """Notebook Widget"""
    def __init__(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)        
    
        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
                                                                                           #Make various argument available to the rest of the class
        self.activefg = activefg                                                           
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                  #This dictionary holds the label and frame instances of each tab
        self.tabs = 0                                                                      #Keep track of the number of tabs                                                                             
        self.noteBookFrame = Frame(parent)                                                 #Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)                                            #Create a frame to put the "tabs button" in
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 2, **kw)           #Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)                                                    #self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def change_tab(self, IDNum):
        """Internal Function"""
        
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  #Make sure tab hasen't been deleted
                if i <> IDNum:                                                             #Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()                                       #Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     #Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0]['fg'] = self.inactivefg                             #Set the fg of the tab, showing it is selected, default is black
                else:                                                                      #When on the tab that is currently selected...
                    self.tabVars[i][1].grid()                                              #Re-grid the frame that corresponds to the tab                      
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   #Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0]['fg'] = self.activefg                               #Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width = 2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """
        
        temp = self.tabs                                                                   #Temp is used so that the value of self.tabs will not throw off the argument sent by the label's event binding
        self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               #Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  #Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) #Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                #Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               #Grid the frame ontop of any other already existing frames
        self.change_tab(0)                                                                 #Set focus to the first tab
        self.tabs += 1                                                                     #Update the tab count
        return self.tabVars[temp][1]                                                       #Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                b[0].destroy()                                                             #Destroy the tab's frame, along with all child widgets
                self.tabs -= 1                                                             #Subtract one from the tab count
                self.deletedTabs.append(self.iteratedTabs)                                 #Apend the NumID of the given tab to the list of deleted tabs
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1                                                         #Add one to the loop count
    
    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                self.change_tab(self.iteratedTabs)                                         #send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1     

class SnapshotParser:
	def __init__(self,snapshotsFilePath):
		self.snapshotsFilePath = snapshotsFilePath
		self.snapshotsTxtOpen = open(snapshotsFilePath,"r+")
		self.snapshotsTxt=self.snapshotsTxtOpen.read()
		self.snapshotsTxtOpen.close()
		self.snapshotsTxt.rstrip()
		self.snapshotsList = self.snapshotsTxt.rstrip().split("\n")


	def addToListHeadThenToFile(self,cmd):
		self.snapshotsList.insert(0,cmd)
		self.snapshotsTxtOpen = open(self.snapshotsFilePath,"r+")
		print self.snapshotsTxtOpen
		for cmd in self.snapshotsList:
			self.snapshotsTxtOpen.write(cmd + "\n")
		self.snapshotsTxtOpen.close()



	def updateListAccordingToFile(self,snapshotsFilePath):
		print "updating"


	def deleteFromListThenFromFile(self,snapshot):
		if snapshot in self.snapshotsList:
			self.snapshotsList.remove(snapshot)
			self.updateFileByList()
		else:
			print "the input snapshot can't be find in the list and file"

	def updateFileByList(self):
		self.snapshotsTxtOpen = open(self.snapshotsFilePath,"r+")
		self.snapshotsTxtOpen.truncate()
		for snapshot in self.snapshotsList:
			self.snapshotsTxtOpen.write(snapshot + "\n")
		self.snapshotsTxtOpen.close()

class cmdSnapshot:
	def __init__(self,master,snapshotParser):
		self.snapshotParser = snapshotParser
		r = 0
		c = 1 + 1
		# self.frame = Frame(master)# to adapt to tab formate
		self.frame = master
		self.frame.pack()
		self.Frame_block0_0 = Frame(self.frame, height=500, width=400)
		self.Frame_block0_1 = Frame(self.frame, height=500, width=400)
		self.Frame_block1_0 = Frame(self.frame, height=500, width=400)
		self.Frame_block1_1 = Frame(self.frame, height=500, width=400)
		self.Frame_block0_0.grid(row = r,column = c - 1 ,columnspan = 2)
		self.Frame_block0_1.grid(row = r,column = c + 1)
		self.Frame_block1_0.grid(row = r,column = c + 2)
		self.Frame_block1_1.grid(row = r,column = c + 3)
		r = r + 1
		wid_Frame_block0_0 = self.Frame_block0_0.winfo_id()
		wid_Frame_block0_1 = self.Frame_block0_1.winfo_id()
		wid_Frame_block1_0 = self.Frame_block1_0.winfo_id()
		wid_Frame_block1_1 = self.Frame_block1_1.winfo_id()
		
		# b = Button(self.frame,text="Send", command=lambda:send_cmd(wid_Frame_block0_0))
		# b.pack(side=RIGHT)
		initCmds = "cd ~/Webdev/ROR/vocvov/upgrade4vocvov/vocvov;" 
		print os.system('xterm -into %d -geometry 63x40 -sb -e " %s /bin/bash" &' % (wid_Frame_block0_0,initCmds) )
		print os.system('xterm -into %d -geometry 63x40 -sb -e " %s /bin/bash" &' % (wid_Frame_block0_1,initCmds) )
		print os.system('xterm -into %d -geometry 63x40 -sb -e " %s /bin/bash" &' % (wid_Frame_block1_0,initCmds) )
		print os.system('xterm -into %d -geometry 63x40 -sb -e " %s /bin/bash" &' % (wid_Frame_block1_1,initCmds) )

		
		self.label_snapshots = Label(self.frame,text="----------------Snapshots------------",font=("Helvetica", 16))
		self.label_snapshots.grid(row=r, column=c)
		r = r + 1

		self.Listbox_number = Listbox(self.frame, width ="2")
		self.Listbox_number.grid(row=r, column=c - 1 )
		self.Listbox_snapshots = Listbox(self.frame, selectmode = BROWSE,width ="40")
		self.Listbox_snapshots.bind('<<ListboxSelect>>',self.insertSelectionToText)
		self.Listbox_snapshots.grid(row=r, column=c )
		r = r + 1

		r = r - 2
		self.label_combination = Label(self.frame,text="---------Edit area--------",font=("Helvetica", 16))
		self.label_combination.grid(row=r, column=c + 1)
		r = r + 1


		self.Text_combination_scrollbar = Scrollbar(self.frame, orient=VERTICAL)
		
		self.Text_combination = Text(self.frame, height = "5", width = "40",yscrollcommand = self.Text_combination_scrollbar.set)
		self.Text_combination.grid(row=r, column=c + 1)
		self.Text_combination_scrollbar.config(command=self.Text_combination.yview)
		r = r + 1

		# self.Button_executeCombination = Button(self.frame, text="Execute Combination", command=self.executeCmdsCombination)
		# self.Button_executeCombination.grid(row=r, column=c + 1)
		# r = r + 1

		r = r - 2
		self.label_combination = Label(self.frame,text="---------Add a Snapshot---------",font=("Helvetica", 16))
		self.label_combination.grid(row=r, column=c + 2)
		r = r + 1

		self.Entry_Snapshot = Entry(self.frame,width="40")
		self.Entry_Snapshot.grid(row=r, column=c + 2)
		r = r + 1

		self.Button_addSnapshot = Button(self.frame, text="Add Snapshot", command=self.insertSnapshotToFileAndListbox)
		self.Button_addSnapshot.grid(row=r, column=c + 2)
		r = r + 1

		self.Button_delSnapshot = Button(self.frame, text="Delete Snapshot", command=self.deleteSnapshotFromFileAndListbox)
		self.Button_delSnapshot.grid(row=r, column=c + 2)
		r = r + 1

		self.Button_closeUI = Button(self.frame, text="Close All Window", command=self.closeUI)
		self.Button_closeUI.grid(row=r, column=c + 2)
		r = r + 1

		

	def executeCmdsCombination(self):
		mp("should get all in text field",self.Text_combination.get(1.0,END))
		List_Lines_Text_combination = self.Text_combination.get(1.0,END).rstrip().split('\n')
		print len(List_Lines_Text_combination)
		for line in List_Lines_Text_combination:
			if line!="":
				location = line.split('>>>>')[0]
				cmd = line.split('>>>>')[1]			
				execute_cmd_inDir(location,cmd)
	def insertSnapshotToFile(self):
		TextContent = self.Entry_Snapshot.get().rstrip()
		self.snapshotParser.addToListHeadThenToFile(TextContent)

	def insertSnapshotToFileAndListbox(self):
		self.Listbox_snapshots.delete(0,END)
		self.insertSnapshotToFile()
		self.insertAllSnapshots()

	def deleteSnapshotFromFileAndListbox(self):
		self.Listbox_snapshots.delete(0,END)
		TextContent = self.Entry_Snapshot.get().rstrip()
		self.snapshotParser.deleteFromListThenFromFile(TextContent)
		self.insertAllSnapshots()

	def closeUI(self):
		os.system('killall xterm')
		root.destroy()

	# def isDoubleClick():

	# def curentTime():
	# 	mp("curent time ",datetime.now())
	# 	return datetime.now()


	def insertSelectionToText(self,EventInstance):
		# ww:tuple is just array. use [0] to reference the first element
		mp("type of selection is typle",type(self.Listbox_snapshots.curselection()[0]))
		selectedIndex = self.Listbox_snapshots.curselection()[0]

		selectedContent = self.Listbox_snapshots.get(selectedIndex)

		self.Text_combination.insert(END,selectedContent)
		self.Text_combination.insert(END,"\n")
		# mp("selection is ",selectedContent)



	def insertAllSnapshots(self):	
		number = 0
		for Snapshot in self.snapshotParser.snapshotsList:
			self.insertSnapshot(number,Snapshot)
			number = number + 1

	def insertSnapshot(self,row_number, snapshot_oneline):
		self.Listbox_number.insert(int(row_number), row_number)
		self.Listbox_snapshots.insert(row_number, snapshot_oneline)


def execute_cmd_inDir(dir,cmd):
	recordedOriginalLcation = os.getcwd()
	printdg("record the current dir:" + recordedOriginalLcation) 

	os.chdir(dir)
	printdg( "change dir to target dir :" + os.getcwd())

	printdg("will execute cmd")
	array_cmd = cmd.split("\n")

	for i in range (0,len(array_cmd)):
		printdg("will execute : " + array_cmd[i] )
		return_code = call(array_cmd[i],shell=True)
		printdg( "finish executing \"%(cmd)s\"with return code: %(returnCode)s " % {"cmd":array_cmd[i], "returnCode" :str(return_code)})
		failMessage=""
		if return_code ==52:
			printdg("Please login to accurev first using $ accurev login")
			failMessage="Please login accurev first using $ accurev login"
		if return_code != 0	:
			printdg("check back to [debug] info")
			win32api.MessageBox(0," ".join(( "Failed:", cmd.replace("call",""), "." , "Reason: " ,failMessage)),'Fail',0x00001000L);
			return False					
	os.chdir(recordedOriginalLcation)
	printdg( "will change back to original dir :" + recordedOriginalLcation)
	printdg("current dir: " + os.getcwd()) 
	print "Finished!"
	# TODO: give user a better feedback when done.
	win32api.MessageBox(0,"Finished " + cmd.replace("call",""),'Succeed',0x00001000L);
	return True


root = Tk()
note = Notebook(root, width= 1800, height =700, activefg = 'red', inactivefg = 'blue')  #Create a Note book Instance
# note.grid()
#TODO: make it a list
tab1 = note.add_tab(text = "snapshots")                                                  #Create a tab with the text "Tab One"
# tab2 = note.add_tab(text = "window1")                                                  #Create a tab with the text "Tab Two"
# tab3 = note.add_tab(text = "window2")                                                #Create a tab with the text "Tab Three"


dirname, filename = os.path.split(os.path.abspath(__file__))
dirname = dirname + "/cmdList"
snapshotsFilePath = dirname + "/snapshots.txt"
#complete version, every step is clear for reader. Below, will use short version
newSnapshotParser = SnapshotParser(snapshotsFilePath)
windows = cmdSnapshot(tab1,newSnapshotParser)
windows.insertAllSnapshots()
# short version:()combine everything in one line
# cmdSnapshot(tab2,SnapshotParser(dirname + "/window1.txt")).insertAllSnapshots()
# cmdSnapshot(tab2,SnapshotParser(dirname + "/window2.txt")).insertAllSnapshots()


# for default ,you might want to give the recent cmd.
# insertContent = windows.Listbox_snapshots.get(0)
# windows.Text_combination.insert(END,insertContent)


# quick-dirty fix, don't fully understand why. It uses self.tabVars[i][1].grid()
# TODO:BUG:it's about the grid() method. 
# Ideal fix: won't need any of these focus to show up a normal GUI
# the followings works differnetly
# 1.
"""
note = Notebook(root, width= 1800, height =700, activefg = 'red', inactivefg = 'blue')
...
...
note.focus_on(tab1)
note.focus_on(tab2)
note.focus_on(tab3)
note.focus_on(tab4)
note.focus_on(tab5)
"""
# 2. the current one. the height and width doesn't matter, the content will fit the container frame
# focus_on all five tabs will disable the GUI from auto fit the content, it will go to the notebook size as specified before.
# note.focus_on(tab3)
# note.focus_on(tab2)



root.mainloop()
