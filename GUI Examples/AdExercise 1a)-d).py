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
        if mark < 0 or mark >100:
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
def addMark(tg):
    try:
        id = input('Enter ID: ')
        mark = int(input('Enter Mark: '))
        tg.addMark(id,mark)
        print('Marks entered')
    except ValueError:
        print('Invalid Input!')  
    except InvalidMarkException     as e:
        print(e)   
        
def resetMark(tg):
    try:
        reset = input('Enter id to reset score to zero: ')
        oldscore = tg.resetMark(reset)
        print('Mark reset for {} from {} to 0 successful!'.format(reset,oldscore))
    except InvalidMarkException as e:
        print(e)  
        
def displayOption(tg):
    try:
        option = input('Enter option to list (Fail/All): ')
        if option == 'Fail':
            fail = tg.getStudentMarks('Fail')
            print('id '+'Name    '+'Mark')
            for k in fail.keys():
                print('{} {:7} {}'.format(k,fail[k][0],fail[k][1]))  
        elif option == 'All':
            all = tg.getStudentMarks('All')  
            print('id '+'Name    '+'Mark')
            for k in all.keys():
                print('{} {:7} {}'.format(k,all[k][0],all[k][1]))    
        else:
            raise InvalidMarkException('Invalid Option')  
    except InvalidMarkException as e:
        print(e)
        
def main():
    tg = TutorialGroup('')
    tg.addStudent('s1', 'John')
    tg.addStudent('s2', 'Peter')
    tg.addStudent('s3', 'Joe')
    while True:
        print('1. Add mark\n2. Reset mark\n3. Display marks\n4. Quit.')
        option = int(input('Enter Option: '))
        if option == 1:
            addMark(tg)
        elif option == 2:
            resetMark(tg)
        elif option == 3:
            displayOption(tg)
        elif option == 4:
            break

main()
            
    
    
