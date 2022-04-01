##imports##
import names
from time import sleep
import random
from tkinter import *

couples = 5


#tkinter window
window = Tk()
c = Canvas(window, width = 500, height = 400, bg = 'lightblue')
c.pack()
window.title('Stable marriage problem')
textbox = c.create_text(250, 25, fill = 'black', font = 'Times 20', text = 'Stable Marriage Problem')
def change_text(size, newtext):
    c.itemconfig(textbox, text = newtext, font = 'Times ' + str(size))
    window.update()

#classes
class male:
    matched = False
    matched_to = ''
    starty = 200
    def __init__(self,preferences = [], name = '', startx = 0):
        self.prefs = preferences
        self.name = name
        self.startx = startx
        self.circle = c.create_oval(startx-25,self.starty-25,startx+25,self.starty+25,fill='blue',outline = 'black')
        self.name_text = c.create_text(startx, self.starty+37, fill='black', font = 'Times 15', text = self.name)

class female:
    matched = False
    matched_to = ''
    pindex = 0
    starty = 105
    def __init__(self,preferences = [], name = '', startx = 0):
        self.prefs = preferences
        self.name = name
        self.startx = startx
        self.circle = c.create_oval(startx-25,self.starty-25,startx+25,self.starty+25,fill = 'red',outline='black')
        self.name_text = c.create_text(startx,self.starty+37,fill='black',font = 'Times 15', text = self.name)
        self.currentx = startx
        self.currenty = self.starty

    #functions to move the graphics
    def move_by(self,x,y,steps = 100,secs = 3):
        movex = x / steps
        movey = y / steps
        delay = secs / steps
        for i in range(steps):
            c.move(self.circle,movex,movey)
            c.move(self.name_text,movex,movey)
            self.currentx += movex
            self.currenty += movey
            window.update()
            sleep(delay)

    def move_to(self,x,y,steps = 100, secs = 3):
        movex = x - self.currentx
        movey = y - self.currenty
        self.move_by(movex,movey,steps,secs)

    def reset_graphic(self):
        self.move_to(self.startx,self.starty,100,1.5)

    #ask to marry someone
    def ask(self, name):
        change_text(20,self.name + ' asks ' + name + '.')
        self.move_to(males[name].startx, 350,100,1.5)
        #if they are already matched
        if males[name].matched:
            #get indexes in priority of each option
            spouseindex = males[name].prefs.index(males[name].matched_to)
            newaskindex = males[name].prefs.index(self.name)
            change_text(20,name + ' is already matched.')
            sleep(2)
            #if this female is higher in preference list
            if spouseindex > newaskindex:
                #erase old connection
                change_text(15,name + ' prefers ' + self.name + ' over ' + males[name].matched_to + ', so they are matched.')
                females[males[name].matched_to].reset_graphic()
                females[males[name].matched_to].matched = False
                females[males[name].matched_to].matched_to = ''
                males[name].matched = False
                males[name].matched_to = ''
                #create a match
                self.matched = True
                males[name].matched = True
                matched_to = name
                males[name].matched_to = self.name
                self.move_by(0,-75,100,1.5)
                return 0

            else:
                change_text(15,name + ' prefers ' + males[name].matched_to + ', so no new match occurs.')
                self.reset_graphic()
        else:
            change_text(15,name + ' is not matched, so they are provisionally matched.')
            #create a match
            self.matched = True
            males[name].matched = True
            matched_to = name
            males[name].matched_to = self.name
            self.move_by(0,-75,secs=1.5)
            
            #return value to increment matches
            return 1
        return 0
        


###Thanks to Tyler for the base code that became test data generation - the code has changed a LOT since but the base principle is still the same
#generate names
temp_couples = couples
male_names = []
female_names = []
while temp_couples > 0:
    man = names.get_first_name(gender='male')
    woman = names.get_first_name(gender='female')
    if man not in male_names and woman not in female_names:
        male_names.append(man)
        female_names.append(woman)
        temp_couples -= 1


#generate preferences
males = {}
females = {}
for name in male_names:
    slist = list(female_names)
    random.shuffle(slist)
    males[name] = male(preferences = slist, name = name, startx = (male_names.index(name)*100)+50)

for name in female_names:
    slist = list(male_names)
    random.shuffle(slist)
    females[name] = female(preferences = slist, name = name, startx = (female_names.index(name)*100)+50)

##cycle through days##
day = 1
matches = 0
while couples != matches:
    change_text(30,'Day '+str(day))
    window.title('Stable Marriage Problem - Day ' + str(day))
    sleep(1.5)

    #iterate through each woman
    for name in females.keys():
        #if the woman isnt already matched
        if females[name].matched == False:
            #ask the next man on their list
            matches += females[name].ask(name = females[name].prefs[females[name].pindex])
            females[name].pindex += 1
    day += 1
change_text(40, 'Finished.')
window.mainloop()
