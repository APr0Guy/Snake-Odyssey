import tkinter as tk
import random

class snake:
    def __init__(self,root):
        self.root = root
        self.root.bind('<Key>',lambda e:print(e))
        self.bg_make()

    def bg_make(self):
        x = y = 0 # 40x45 (y,x) x is 15 times y is 12 times and diff btwn 2 x is 15
        for i in range(180):
            btn = tk.Button(text=i,width=5,height=2,bg='black',fg='black') ; btn.pack()
            btn.place(x=x,y=y)
            if x <= 15*45:
                x += 45
                if x == 15*45:
                    x = 0
                    y += 40

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('675x480')
    root.title('Snake')
    root.resizable(False, False)
    snake(root)
    root.mainloop()
