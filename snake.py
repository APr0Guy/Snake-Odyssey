import tkinter as tk
import random

class snake:
    def __init__(self,root):
        self.root = root
        self.pos_1 = [67+15*i for i in range(5)]
        self.tick_speed = 400
        self.last_pressed = ''
        self.apple_eaten = 0

        self.label_main = tk.Label(self.root,text='PRESS SPACE TO START',font='Arial 20 bold') ; self.label_main.pack()
        self.root.bind('<Key>',self.change_key)

        self.make_apple() #bg gets made in making of apple

        self.root.bind('<FocusIn>',lambda e=None:print('yes')) #for testing
        self.root.bind('<FocusOut>',lambda e=None:print('no'))

    def change_key(self,event):
        if event.char in ['w','a','s','d']:
            self.last_pressed = event.char

        elif event.char == ' ': #to start game press space
            self.last_pressed = 'w'
            self.move(self.last_pressed) #actually starts game

    def make_apple(self):
        self.apple_pos = random.randint(0,180) #makes apple in random position
        while self.apple_pos in self.pos_1: #apple doesnt spawn in snakes body
            self.apple_pos = random.randint(0,180)
        
        self.bg_make() #makes bg after apple has been made

    def bg_make(self):
        x,y = 0,40 # 40x45 (y,x) x is 15 times y is 12 times and diff btwn 2 x is 15
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
            if isinstance(widget,tk.Button):
                if int(widget.cget('text')) in self.pos_1:
                    widget.config(bg='green',fg='green') #make things in list green

                    if int(widget.cget('text')) == self.pos_1[0]:#change color of head
                        widget.config(bg='blue',fg='white') #fg = white shows current position in button

                    elif int(widget.cget('text')) == self.pos_1[-1]:#change color of tail
                        widget.config(bg='orange',fg='white')
                    
                elif int(widget.cget('text')) == self.apple_pos:
                    widget.config(bg='red',fg='white')

                else:
                    widget.config(bg='black',fg='black') #make everything black

    def move(self,event):
        self.label_main.config(font='Arial 15 bold',text=f'Length of Snake: {len(self.pos_1)}  Score: {self.apple_eaten}')

        if event == 'a': #left
            self.pos_1.insert(0,self.pos_1[0]-1) #assigns new position for head
        
        elif event == 'd': #right
            self.pos_1.insert(0,self.pos_1[0]+1)

        elif event == 'w': #front
            self.pos_1.insert(0,self.pos_1[0]-15)
        
        elif event == 's': #back
            self.pos_1.insert(0,self.pos_1[0]+15)

        if self.apple_pos == self.pos_1[0]:
            ... #doesnt remove tail if apple is eaten
        else:
            self.pos_1.pop() #removes tail

        self.bg_color() #makes things green again according to self.pos_1
        self.root.after(self.tick_speed,lambda:self.move(self.last_pressed)) #auto move
    
        self.apple_check()
    
    def apple_check(self): #this is for scores and making the body bigger
        if self.apple_pos == self.pos_1[0]:
            self.apple_eaten+=1 #increases apple
            self.make_apple() #remakes everything gives it a cool white flash vfx

            if self.apple_eaten%5 == 0:
                if self.tick_speed > 0:
                    self.tick_speed-=50

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('675x520') #(y,x)
    root.title('Snake')
    root.resizable(False, False)
    snake(root)
    root.mainloop()