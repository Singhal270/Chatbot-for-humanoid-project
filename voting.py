import random
from tkinter import *
import sqlite3


def insertdata(question,option):
    conn = sqlite3.connect("C:/Users/MOHIT SINGHAL/Desktop/projects/votedata.db")
    cmd = "SELECT * FROM question WHERE no="+str(question)
    cursor = conn.execute(cmd)
    choice="option"+str(option)
    for row in cursor:
        current=row[option]
        cmd = "UPDATE question SET "+str(choice)+"="+str(current+1)+" WHERE no="+str(question)
    conn.execute(cmd)
    conn.commit()
    conn.close()

def vote():
        global vote1;
        global vote2;
        global vote3;
        global vote4;
        
        window = Tk()
        window.title("Quiz")
        window.geometry("600x450")

        def khatam():
                window.destroy()       

        questions = [["it is first question","1","2","3","4"]]
        questions.append(["it is third question","1","2","3","4"])
        questions.append(["it is forth question","1","2","3","4"])
        questions.append(["it is fifth question","1 ","2","3","4"])
        questions.append(["it is six question","1","2","3","4"])
        def clear():
                list = window.grid_slaves()
                for n in list:
                        n.destroy()

        class Quiz:
                def __init__(self,quest):
                        clear()
                        self.Fragen = []
                        for n in quest:
                                self.Fragen.append(n)
                        self.a1=""
                        self.a2=""
                        self.a3=""
                        self.a4=""
                        self.Ra=""
                        self.RaBtn = Button(window, text="",font=("Arial",14))
                        self.antw1 = Button(window, text="",font=("Arial",14))
                        self.antw2 = Button(window, text="",font=("Arial",14))
                        self.antw3 = Button(window, text="",font=("Arial",14))
                        self.antw4 = Button(window, text="",font=("Arial",14))
                        self.lock=False
                        self.right=0
                        self.count=0
                        self.naechste = Button(window,text="next",font=("Arial",14),command=self.Frage)
                        self.nummer=0
                        self.Max=5
                        self.Frage()
                def Frage(self):
                        self.naechste.grid(column=0,row=5,pady=5)
                        if len(self.Fragen) > 0 and self.nummer < self.Max:
                                self.nummer += 1
                                self.lock = False
                                fragenText = self.Fragen[0][0]
                                self.Ra = self.Fragen[0][-1]
                                answers = []
                                for i in range(1,5):
                                        answers.append(self.Fragen[0][i])
                                

                                self.a1 = answers[0]
                                self.a2 = answers[1]
                                self.a3 = answers[2]
                                self.a4 = answers[3]

                                frage = Text(window, font=("Arial", 14), width=40, height=2)
                                frage.insert(END,fragenText)
                                frage.grid(column=0,row=0,padx=80,pady=(75,0))

                                self.antw1 = Button(window, text=self.a1, font=("Arial",14),width=39, command = self.control1)
                                self.antw2 = Button(window, text=self.a2, font=("Arial",14),width=39, command = self.control2)
                                self.antw3 = Button(window, text=self.a3, font=("Arial",14),width=39, command = self.control3)
                                self.antw4 = Button(window, text=self.a4, font=("Arial",14),width=39, command = self.control4)

                                self.antw1.grid(column=0,row=1,pady=(8,5))
                                self.antw2.grid(column=0,row=2,pady=5)
                                self.antw3.grid(column=0,row=3,pady=5)
                                self.antw4.grid(column=0,row=4,pady=5)

                                if self.a1 == self.Ra:
                                        self.RaBtn = self.antw1
                                elif self.a2 == self.Ra:
                                        self.RaBtn = self.antw2
                                elif self.a3 == self.Ra:
                                        self.RaBtn = self.antw3
                                elif self.a4 == self.Ra:
                                        self.RaBtn = self.antw4
                                self.Fragen.pop(0)
                        else:
                                clear()
                                lb = Label(window, text="you vote for " + str(self.right) + " argument from " + str(self.Max) + ",thanks ",font=("Arial",14))
                                lb.grid(column=0,row=0,padx=120,pady=(170,15))
                                zumMenu = Button(window, text="Menu",font=("Arial",14),command=khallas)
                                zumMenu.grid(column=0,row=1)

                def control1(self):
                        if self.lock == False:                   
                                if self.Ra != self.a1:
                                        self.antw1.configure(bg="yellow")
                                        self.right += 1          
                                else:
                                        self.antw1.configure(bg="yellow")  
                                        self.right += 1   

                            
                                insertdata(self.nummer,1)
                                self.lock = True
                                                
                def control2(self):
                    
                        if self.lock == False:
                                if self.Ra != self.a2:
                                        self.antw2.configure(bg="yellow")
                                        self.right += 1
                                else:
                                        self.antw2.configure(bg="yellow")
                                        self.right += 1
                                
                                insertdata(self.nummer,2)
                    
                                self.lock = True

                def control3(self):
                        if self.lock == False:
                                if self.Ra != self.a3:
                                        self.antw3.configure(bg="yellow")
                                        self.right += 1
                                else:
                                        self.antw3.configure(bg="yellow")
                                        self.right += 1
                            
                                insertdata(self.nummer,3)
                  
                                self.lock = True

                def control4(self):
                        if self.lock == False:
                                if self.Ra != self.a4:
                                        self.antw4.configure(bg="yellow")
                                        self.right += 1
                                else:
                                        self.antw4.configure(bg="yellow")
                                        self.right += 1
                                
                                insertdata(self.nummer,4)
                          
                                self.lock = True



        class Menu:
                def __init__(self):
                        clear()
                        self.Quiz = Button(window, text="Vote", font=("Arial", 14), command=quizCreator, width=15, height=3)
                        self.Quiz.grid(column=0,row=0,padx=218,pady=170)


        def khallas():
            clear()
            window.destroy()


        def menuCreator():
                m = Menu()

        def quizCreator():
                q = Quiz(questions)

        menuCreator()
        window.mainloop()
        print("nikal gaye")


