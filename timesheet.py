#modules 
from tkinter import * 
from csv import *
from datetime import * 



class TimeSheet:

    #### GUI ######

    def __init__(self, rW):
        self.rW = rW
        self.GUIsetup()

    def GUIsetup(self):
        #summary verify variable - this var assigned 1 when correct files loaded --> ensure Run Summary Button not clicked unless files loaded
        self.time_summaryVerify = 0
        self.employ_summaryVerify = 0
        
        #title
        self.rW.title("GUI") #<--- need title from biz team

        #entries
        self.sv1 = StringVar()
        self.sv2 = StringVar()
        self.timeEntry = Entry(self.rW, textvariable = self.sv1, state='readonly', width = 60).grid(row=0, column=1, columnspan=5, pady=3, padx=3)
        self.employEntry = Entry(self.rW, textvariable = self.sv2, state='readonly', width = 60).grid(row=1, column=1, columnspan=5, pady=3, padx=3)

        #buttons
        self.timeButton = Button(self.rW, width = 20, text='Select Time Sheet File', command = self.Time_fileSelect).grid(row=0, column=0, sticky=W, pady=5, padx=5)
        self.employButton = Button(self.rW, width = 20, text='Select Employee List File', command = self.Employ_fileSelect).grid(row=1, column=0, sticky=W, pady=5, padx=5)
        self.summaryButton = Button(self.rW, width = 20, text='Run Summary', command = self.timeSummary).grid(row=0, column=6, rowspan=2, sticky=NSEW, pady=2, padx=5)

    #### File load ####
    def Time_fileSelect(self):
        self.time_fileName = filedialog.askopenfilename(title = "Please choose the Employee Time Sheet File")
        if self.time_fileName == "":
            messagebox.showwarning('Error', 'Error: You failed to select a file. Please choose the Employee Time Sheet File')
        else:
            self.timeEntry = Entry(state='normal')
            self.load_TimeCSV(self.time_fileName)
            self.sv1.set(self.time_fileName)
            self.timeEntry = Entry(state='readonly')
        
        if type(self.time_csvList) != list:
            messagebox.showwarning('Error - Incorrect file type!', 'Error: the file you selected is not the correct format. Ensure that you have loaded a .csv excel sheet.')

    def Employ_fileSelect(self):
        self.employ_fileName = filedialog.askopenfilename(title = "Please choose the Employee Member File")
        if self.employ_fileName == "":
            messagebox.showwarning('Error', 'Error: You failed to select a file. Please choose the Employee Member File')
        else:
            self.employEntry = Entry(state='normal')
            self.load_EmployCSV(self.employ_fileName)
            self.sv2.set(self.employ_fileName)
            self.employEntry = Entry(state='readonly')

        if type(self.employ_csvList) != list:
            messagebox.showwarning('Error - Incorrect file type!', 'Error: the file you selected is not the correct format. Ensure that you have loaded a .csv excel sheet.')
        else:
            self.dataManipulator()
    

    def load_TimeCSV(self, fileName):
        try:
            self.timeInfo = open(self.time_fileName)
            self.time_csvList = self.timeInfo.readlines()
            self.time_csvList = self.time_csvList[1::3]
            #print(self.time_csvList)
            self.time_csvList = self.clean_timeCSV()
            self.timeInfo.close()
            self.time_summaryVerify = 1 #file loaded --> verify
            
        except:
            self.time_csvList = "Error File"
            return self.time_csvList

    def load_EmployCSV(self, fileName):
        try:
            self.employInfo = open(self.employ_fileName)
            self.employ_csvList = self.employInfo.readlines()
            self.employ_csvList = self.employ_csvList[1::3]
            self.employ_csvlist = self.clean_employCSV()
            self.employInfo.close()
            self.employ_summaryVerify = 1 #file loaded --> verify
            
        except:
            print('naw we in except for some reason')
            self.employ_csvList = 'Error File'
            return self.employ_csvList

    ### Clean up file ### 
    
    def clean_timeCSV(self):
        clean_timeList = []
        for line in self.time_csvList:
            line = line.rstrip()
            if len(line) != 0:
                clean_timeList.append(line)

        preSplit_timeList = []
        for line in clean_timeList:
            indivLines = line.split(',')
            preSplit_timeList.append(indivLines)
        self.mother_timeList = []
        
        for items in preSplit_timeList:
            #date = items[1]
            date = datetime.strptime(items[1], '%m/%d/%Y').strftime('%Y-%m-%d')
            items[1] = date
            itemsout = []
            #print(items)
            for item in items:
                try:
                    itemsout.append(float(item))
                    
                except ValueError:
                    itemsout.append(item)

            self.mother_timeList.append(itemsout)
        #print(self.mother_timeList)
        self.new_mother_timeList = []
        for item in self.mother_timeList:
            miniList = item[0:2:] + item[4:5:] + item[6:9:]
            self.new_mother_timeList.append(miniList)
            #print(miniList)
        #print(self.new_mother_timeList)
            
        return self.new_mother_timeList

    
    def clean_employCSV(self):
        
        clean_employList = []
        for line in self.employ_csvList:
            line = line.rstrip()
            if len(line) != 0:
                clean_employList.append(line)
        
        preSplit_employList = []
        for line in clean_employList:
            indivLines = line.split(',')
            preSplit_employList.append(indivLines)

        self.date_mother_employList = []
        for items in preSplit_employList:
            itemsout = []
            for item in items:
                try:
                    itemsout.append(float(item))
                except ValueError:
                    itemsout.append(item)
            self.date_mother_employList.append(itemsout)
        #print(self.date_mother_employList)

        self.noDate_mother_employList = self.date_mother_employList[1::]
        for listical in self.noDate_mother_employList:
            name = listical[2][1::] + listical[3].strip('"')
            listical.pop(2) and listical.pop(2)
            listical.append(name)

        ## if want improved name list with date
        self.newName_mother_employList = self.date_mother_employList[0::1] + self.noDate_mother_employList
        return self.newName_mother_employList

    ## checks employee list to raw time sheet data and returns dict summarizing hours worked on projects within certain weeks
    def dataManipulator(self):
        
        for item in self.new_mother_timeList:
            week = date(int(item[1][0:4:]), int(item[1][5:7:]), int(item[1][8:10:])).isocalendar()[1]
            item[1] = week
            
        self.personDict = {}
        for x in self.noDate_mother_employList:
            innerList = []
            for y in self.new_mother_timeList:
                if x[0] == y[0]:
                    innerList.append(y)
                    self.personDict[x[0]] = innerList
        print('this be dat personDict', self.personDict)

        ## employeeDict = {'employee1': {proj:[9,2,4,5,6,], proj:[0,3,4,6,]}}
##        self.employeeDict = {}
##        for i in self.personDict:
##            print('')
        
##    
    def timeSummary(self):
        if self.time_summaryVerify == 1 and self.employ_summaryVerify == 1:
            print('both entries are gucci')
            self.finalEmployeeDict = {}
            for key, value in self.personDict.items():
                self.finalEmployeeDict[key] = {}
                for item in value:
                    self.finalEmployeeDict[key][item[4]] = [0]*52

            #employeeDict = {'employee1': {proj:[0, 0, 0, 0, 0], proj2:[0, 0, 0,0]}}
                    
            for key1, value1 in self.personDict.items():
                #print(key)
                #print(value)
                for item1 in value1:
                    #print(item) # lists of data 
                    for key2, value2 in self.finalEmployeeDict.items():
                        print(key2)
                        #print(value2)
                        for item2 in value2:
                            #print(value[item])
                            #print('item2', item2)
                            if item1[0] in self.finalEmployeeDict:
                                if item1[4] in item2:
                                    print('hello')
                                    #self.finalEmployeeDict[key1][item[4]] = item2[0:item1[2]:]+item2[item1[2]::]
            print(self.finalEmployeeDict)
                                
                        
                        




                
##                for item in value:
##                    weeks = [0]*52
##                    finalEmployeeDict[key][item[4]] = weeks
##                    if item[4] in finalEmployee[key][item[4]]:
##                        finalEmployee[key][item[4]] = weeks[0:int(item[1]):] + list[item[2]] + weeks[
##                        
##                    finalEmployeeDict[key][item[] = weeks
##            print(finalEmployeeDict)

                    #finalEmployeeDict[key][item[4]] = weeksList
                    #print(finalEmployeeDict)
##                    if item[4] in finalEmployeeDict[key]:
##                        finalEmployeeDict[key][item[4]] = weeksList[int(item[1])] + item[2]
##                        print('hello')
##                        print(finalEmployeeDict)
##                    else:
##                        finalEmployeeDict[key][item[4]] = weeksList
##                        print(finalEmployeeDict)
##                        print('no')
                    
        else:
            print('something went wrong')

    ### Logical Sequence ###
    ### 1) use <week = date(int(newDate[0:4:]), int(newDate[5:7:]), int(newDate[8:10:])).isocalendar()[1]> to get week
    ### 2) consolidate all hours within week --> if same person, if in same project, if same week, add hours
    ### 3) display hours for weeks in existence
    ### 4) for output csv - first list will have headers with all weeks. If hours for a week are all zero
    ### idea: have drop down menu for week ranges --> show dates but datapoint is the week for the date ranges -->
            ### a) build out complete list with all weeks and data points --> mother_timeSummary_list
            ### b) get week ranges --> index/copy mother_timeSummary_list with selected ranges and display those 

    
    
    
    
    
    
    
#GUI initiation 
rW = Tk()
app = TimeSheet(rW)
rW.mainloop()




