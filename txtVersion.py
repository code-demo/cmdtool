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
		c = 1
		self.frame = Frame(master)
		self.frame.pack()

		
		self.label_snapshots = Label(self.frame,text="--------------------------Snapshots--------------------------",font=("Helvetica", 16))
		self.label_snapshots.grid(row=r, column=c)
		r = r + 1

		self.Listbox_number = Listbox(self.frame, width ="2")
		self.Listbox_number.grid(row=r, column=c - 1 )
		self.Listbox_snapshots = Listbox(self.frame, selectmode = BROWSE,width ="120")
		self.Listbox_snapshots.bind('<<ListboxSelect>>',self.insertSelectionToText)
		self.Listbox_snapshots.grid(row=r, column=c)
		r = r + 1

		self.label_combination = Label(self.frame,text="----------------Your snapshots combination----------------",font=("Helvetica", 16))
		self.label_combination.grid(row=r, column=c)
		r = r + 1


		self.Text_combination_scrollbar = Scrollbar(self.frame, orient=VERTICAL)
		
		self.Text_combination = Text(self.frame, height = "5", width = "90",yscrollcommand = self.Text_combination_scrollbar.set)
		self.Text_combination.grid(row=r, column=c)
		self.Text_combination_scrollbar.config(command=self.Text_combination.yview)
		# b
		r = r + 1

		self.Button_executeCombination = Button(self.frame, text="Execute Combination", command=self.executeCmdsCombination)
		self.Button_executeCombination.grid(row=r, column=c)
		r = r + 1

		self.label_combination = Label(self.frame,text="---------------Add a Snapshot----------------",font=("Helvetica", 16))
		self.label_combination.grid(row=r, column=c)
		r = r + 1

		self.Entry_Snapshot = Entry(self.frame,width="120")
		self.Entry_Snapshot.grid(row=r, column=c)
		r = r + 1

		self.Button_addSnapshot = Button(self.frame, text="Add Snapshot", command=self.insertSnapshotToFileAndListbox)
		self.Button_addSnapshot.grid(row=r, column=c)
		r = r + 1

		self.Button_delSnapshot = Button(self.frame, text="Delete Snapshot", command=self.deleteSnapshotFromFileAndListbox)
		self.Button_delSnapshot.grid(row=r, column=c)
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



dirname, filename = os.path.split(os.path.abspath(__file__))
snapshotsFilePath = dirname + "/snapshots.txt"
testSnapshotParser = SnapshotParser(snapshotsFilePath)

# testSnapshotParser.RootListWithNewSnapshot(location,cmd)[0]
# testSnapshotParser.writeDomToOneLineXml()


root = Tk()
windows = cmdSnapshot(root,testSnapshotParser)
windows.insertAllSnapshots()
# for default ,you might want to give the recent cmd.
# insertContent = windows.Listbox_snapshots.get(0)
# windows.Text_combination.insert(END,insertContent)

root.mainloop()