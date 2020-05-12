from tkinter import *
from tkinter.scrolledtext import *

class InvalidMarkException(Exception):
    '''Invalid Mark Exception'''
    
class Student:
    def __init__(self, id, name, mark=0):
        self._id = id
        self._name = name
        self.mark = mark    #no underscore - allow user to make use of exception in setter
        
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def mark(self):
        return self._mark
    @mark.setter
    def mark(self, mark):
        if mark < 0 or mark > 100:
            raise InvalidMarkException('Mark must be between 0 and 100')
        self._mark = mark
   
    def __str__(self):
        return 'Id: {} Name: {:10} Mark: {}'.format(self._id, self._name, self._mark)
    
class TutorialGroup:
        
    def __init__(self, name):
        self._name = name
        self._students = {}
     
    @property
    def name(self):
        return self._name
        
    def search(self,id):
        if id in self._students.keys():
            return id
        return None
    
    def addStudent(self, id, name):      
        find = self.search(id)
        if find is not None:
            raise InvalidMarkException('id already exists')                
        else:
            self._students[id] = Student(id, name)  
                    
    def addMark(self,id, mark):
        find = self.search(id)
        if find is None:
            raise InvalidMarkException('id not found!')        
        elif self._students[id].mark != 0:
            raise InvalidMarkException('Mark has already been assigned')
        else:
            self._students[id].mark = mark
                
    def resetMark(self,id):
        find = self.search(id)
        if find is None:
            raise InvalidMarkException('id not found!')        
        else:
            if self._students[find].mark != 0:
                previous_mark = self._students[find].mark
                self._students[id].mark = 0
                return previous_mark
            else:
                raise InvalidMarkException('Mark is already 0!')
    
    def getStudentMarks(self, option):
        fail ={}
        all = {}
        if option == 'Fail':
            for k in self._students.keys():
                if self._students[k].mark < 50:
                    fail[k] = self._students[k].name,self._students[k].mark
            return fail
        elif option == 'All':
            for k in self._students.keys():
                all[k] = self._students[k].name, self._students[k].mark
            return all
        else:
            raise InvalidMarkException('Invalid Option!')         
################################################################################################
class AssignmentGUI:
    def __init__(self,tg):
        self._tg = tg
        
        self.win = Tk()
        self.win.resizable(False, False)
        self.win.title(self._tg.name)
        self.initWidgets()
        self.win.mainloop()
    
    def initWidgets(self):
        dataFrame = Frame(self.win)
        dataFrame.grid(column=0, row=0)
        
        lblcode = Label(dataFrame, text='Id:')
        lblcode.grid(column=0, row=0,sticky=E) 
        lblqty = Label(dataFrame, text='Exam mark:')
        lblqty.grid(column=0, row=1,sticky=E)
        
        self._id = StringVar()
        self._entryid = Entry(dataFrame, textvariable=self._id)
        self._entryid.grid(row=0,column=1,sticky=E)
        self._mark = StringVar()
        self._entrymark = Entry(dataFrame,textvariable=self._mark)
        self._entrymark.grid(row=1,column=1,sticky=E)
 
        
        btnAddReset = Frame(dataFrame)
        self._btnAddClick = Button(btnAddReset,text='Add',command=self.btnAddClick)
        self._btnAddClick.grid(row=0,column=0)
        self._btnResetClick = Button(btnAddReset,text='Reset',command=self.btnResetClick)
        self._btnResetClick.grid(row=0, column=1)
        btnAddReset.grid(row=2, column=1)
        
        radioFrame = Frame(dataFrame)
        self._radValue = IntVar()
        self._radValue.set(0)
        self._rbtnAll = Radiobutton(radioFrame, text='All',variable=self._radValue,value=0)
        self._rbtnFail = Radiobutton(radioFrame, text='Fail',variable=self._radValue,value=1)
        self._btnDisplayClick = Button(radioFrame,text='Display',command=self.btnDisplayClick)
        self._rbtnAll.grid(column=0, row=0)
        self._rbtnFail.grid(column=1, row=0)
        self._btnDisplayClick.grid(column=2, row=0)
        radioFrame.grid(row=3,column=1)

        outputFrame = Frame(self.win)
        outputFrame.grid(row=2, column=0, columnspan=2)
        self._output = ScrolledText(outputFrame,width=40,height=15, wrap=WORD)
        self._output.grid(row=4, column=0, sticky='WE',pady=5)
        self._output.config(state=DISABLED)
    
    def printLine(self, msg):
        self._output.config(state=NORMAL)
        self._output.insert('end', msg+'\n')
        self._output.config(state=DISABLED)
    
    def btnAddClick(self):
        try:
            id = self._entryid.get()
            mark = int(self._entrymark.get())
            self._tg.addMark(id,mark)
            self.printLine('Marks entered')
        except ValueError:
            self.printLine('Invalid Input!')  
        except InvalidMarkException as e:
            self.printLine(str(e))   
    
    def btnResetClick(self):  
        try:
            id = self._entryid.get()
            oldscore = self._tg.resetMark(id)
            self.printLine('Mark reset for {} from {} to 0 successful!'.format(id,oldscore))
        except InvalidMarkException as e:
            self.printLine(str(e))

    def btnDisplayClick(self):
        if self._radValue.get() == 1:
            fail = self._tg.getStudentMarks('Fail')
            self.printLine('id '+'Name    '+'Mark')
            for k in fail.keys():
                self.printLine('{} {:7} {}'.format(k,fail[k][0],fail[k][1]))
            self.printLine('')  
        else:
            all = self._tg.getStudentMarks('All')  
            self.printLine('id '+'Name    '+'Mark')
            for k in all.keys():
                self.printLine('{} {:7} {}'.format(k,all[k][0],all[k][1]))   
            self.printLine('') 

def main():
    tg = TutorialGroup('SUSS')
    tg.addStudent('s1', 'John')
    tg.addStudent('s2', 'Peter')
    tg.addStudent('s3', 'Joe')
    AssignmentGUI(tg)

main()