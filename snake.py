import tkinter as tk
import random

class snake:
    def __init__(self,root):
        self.root = root
        self.pos_1 = [67+15*i for i in range(5)]
        self.root.bind('<Key>',lambda e:self.move(e.char))
        self.bg_make()

    def bg_make(self):
        x = y = 0 # 40x45 (y,x) x is 15 times y is 12 times and diff btwn 2 x is 15
        for i in range(180): #makes all the buttons
            btn = tk.Button(text=i,width=5,height=2,bg='black',fg='black') ; btn.pack()
            btn.place(x=x,y=y)
            if x <= 15*45:
                x += 45
                if x == 15*45:
                    x = 0
                    y += 40

        self.bg_color()
    
    def bg_color(self):
        for widget in self.root.winfo_children():
            if widget.cget('text') in self.pos_1:
                widget.config(bg='green',fg='green') #make things in list green

                if widget.cget('text') == self.pos_1[0]:#change color of head
                    widget.config(bg='blue',fg='white') #fg = white shows current position in button

                elif widget.cget('text') == self.pos_1[-1]:#change color of tail
                    widget.config(bg='red',fg='white')

            else:
                widget.config(bg='black',fg='black') #make everything black
    
    def move(self,event):
        if event == 'a': #left
            self.pos_1.insert(0,self.pos_1[0]-1) #ok puts new pos of head into first index
            self.pos_1.pop() #removes last index
        
        elif event == 'd': #right
            self.pos_1.insert(0,self.pos_1[0]+1)
            self.pos_1.pop()

        elif event == 'w': #front
            self.pos_1.insert(0,self.pos_1[0]-15)
            self.pos_1.pop()
        
        elif event == 's': #back
            self.pos_1.insert(0,self.pos_1[0]+15)
            self.pos_1.pop()

        self.bg_color()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('675x480')
    root.title('Snake')
    root.resizable(False, False)
    snake(root)
    root.mainloop()