import tkinter as tk
import random

class snake:
    def __init__(self,root):
        self.root = root
        self.root.bind('<Key>',lambda e:print(e))
        self.bg_make()

    def bg_make(self):
        x = y = 0 # 40x45 (y,x) x is 15 times y is 12 times
        for i in range(180):
            btn = tk.Button(text=i,width=5,height=2).place(x=x,y=y)
            x+=45

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('720x560')
    root.title('Snake')
    root.resizable(False, False)
    snake(root)
    root.mainloop()