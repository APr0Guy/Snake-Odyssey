import tkinter as tk
import random

def convert(char):
    char_dict = {'w':'Up','W':'Up','s':'Down','S':'Down','d':'Right','D':'Right','a':'Left','A':'Left'}
    return char_dict.get(char,char)

class snake_canv:
    def __init__(self,root,game_values):
        self.root = root
        self.root.config(bg='black')
        self.game_values = game_values
        self.game_state_perm = {'start':False,'die':False} #state of game

        self.game_state = self.game_state_perm.copy()

        self.perm_tick_speed = 100 #for speed of snake
        self.tick_speed = self.perm_tick_speed
        self.apple_eaten = 0

        self.frame = tk.Frame(self.root,width = game_values['column']*game_values['cell_size'],
                              height = game_values['row']*game_values['cell_size'],bg='black') ; self.frame.pack(expand='True') #changes geomerty based on game_values['column'] and game_values['row']
        self.canvas = tk.Canvas(self.frame,width=self.frame.cget('width'),height=self.frame.cget('height')) ; self.canvas.pack() #same size as frame so its in seperate place than root
        
        self.grid_loc = {} #stores every grids position (x,y) along with their id
        self.grid_loc_reverse = {} #stores every grids id along with their position (x,y)

        print(f"""Cell Size: {self.game_values['cell_size']}\ncolumn,row : {self.game_values['column'],self.game_values['row']}
Size of Frame/Canvas: {self.game_values['column']*self.game_values['cell_size'],self.game_values['row']*self.game_values['cell_size']}
Size of window: {(self.game_values['column']+2)*self.game_values['cell_size'],(self.game_values['row']+2)*self.game_values['cell_size']}""")

        self.last_pressed = 'Up' #starting key when game starts unless changed
        
        self.make() #makes grid for game
        self.make_apple() #makes apple

        self.root.bind('<Key>',self.change_key) #allows changing of direction

    def change_key(self,event):
        self.opp = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
        current_pressed = self.last_pressed #for checking if new event is not opposite to old so you die immediately

        if self.game_state['start'] == True: #so 
            if event.char in ['w','a','s','d','W','A','S','D']:
                if current_pressed == self.opp[convert(event.char)]: #so you cant press w then s to immediately die
                    ...
                else: #if not opposites then take the input
                    self.last_pressed = convert(event.char)

            elif event.keysym in ['Up','Down','Left','Right']:
                if current_pressed == self.opp[event.keysym]: #so you cant press Up then Down to immediately die
                    ...
                else: #if not opposites then take the input
                    self.last_pressed = event.keysym

        elif self.game_state['start'] == False: #to start game press space

            if event.char in ['w','a','s','d','W','A','S','D']:
                self.last_pressed = convert(event.char)

                if self.last_pressed == 'Down': #when restarting if you went down direction last you would instantly die
                    self.last_pressed = 'Up'

            elif event.char == ' ':
                self.game_state['start'] = True
                self.move(self.last_pressed) #actually starts game
        
        print('Current direction : {}'.format(self.last_pressed))

        self.canvas.delete('snake_eye') #deletes all eyes on input
        self.make_eye() #makes eye on input

    def make(self):
        x,y=0,0
        for i in range(self.game_values['column']*self.game_values['row']): #total boxes
            if i%2 == 0:
                grids = self.canvas.create_rectangle(x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size'],
                                                     fill='#1C1F2A',tag = 'snake_bg') #grey color with snake_bg tag
            else:
                grids = self.canvas.create_rectangle(x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size'],
                                                     fill='#0F0F14',tag = 'snake_bg') #black color with snake_bg tag

            self.grid_loc[grids] = (x,y)#stores location of each box with number
            self.grid_loc_reverse[(x,y)] = grids

            self.canvas.tag_bind(grids,'<Button-1>',lambda e,g=grids:print(f'Number: {g}, Coord: {self.grid_loc.get(g)}'))

            if x<self.game_values['cell_size']*self.game_values['column']: #makes game_values['column']
                x+=self.game_values['cell_size']
                if x == self.game_values['cell_size']*self.game_values['column']: #makes game_values['row']
                    x = 0
                    y += self.game_values['cell_size']

        self.body_pos = [] #stores body pos

        #for getting heads location
        head_x , head_y = self.game_values['column']//2*self.game_values['cell_size'] , self.game_values['row']//2*self.game_values['cell_size'] #get coord of head position in center of board
        head_grid_no = self.grid_loc_reverse[(head_x,head_y)]
        # ^^ gets index of head then converts it into a number;first changes into string then into int

        for i in range(self.game_values['snake_size']): #runs till body size
            self.body_pos.append(self.grid_loc[head_grid_no]) #stores body id
            head_grid_no += self.game_values['column'] #cause diff btwn game_values['column'] is same so add to get other position

        #makes and colors body
        for index,item in enumerate(self.body_pos): #remakes evrything with new body position
            if index == 0: #colors head
                self.head = self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#189f11',tag = 'snake_body') #bbox gets coords of object

            elif index == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#175e13',tag = 'snake_body')
            else: #colors body
                self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#168211',tag = 'snake_body')
        
        self.make_eye()
    
    def make_apple(self):
        self.canvas.delete('apple')
        x = random.randrange(0 , (self.game_values['column']  *self.game_values['cell_size']) , self.game_values['cell_size'])
        y = random.randrange(0 , (self.game_values['row'] * self.game_values['cell_size']) , self.game_values['cell_size'])

        while (x,y) in self.body_pos: #repeats this function as long as apples position exists inside snakes body
            x = random.randrange(0 , (self.game_values['column']  *self.game_values['cell_size']) , self.game_values['cell_size'])
            y = random.randrange(0 , (self.game_values['row'] * self.game_values['cell_size']) , self.game_values['cell_size'])

        self.apple_pos_main = (x,y,x+self.game_values['cell_size'],y+self.game_values['cell_size']) #this is for making apple shape
        self.apple_pos = (x,y) #apple position to compare

        self.canvas.create_oval(self.apple_pos_main,tag='apple',fill="#C11B1B")

    def move(self,event):
        if self.game_state['die'] == False:
            x,y = self.body_pos[0]

            if event == 'Up':
                self.body_pos.insert(0,(x,y-self.game_values['cell_size'])) #adds new item in front (head) also changes coordinates of head based on cell size picked
            elif event == 'Down':
                self.body_pos.insert(0,(x,y+self.game_values['cell_size']))
            elif event == 'Left':
                self.body_pos.insert(0,(x-self.game_values['cell_size'],y))
            elif event == 'Right':
                self.body_pos.insert(0,(x+self.game_values['cell_size'],y))

            if self.body_pos[0] != self.apple_pos:
                self.body_pos.pop() #removes last item (tail) if apple is not eaten

            elif self.body_pos[0] == self.apple_pos:
                self.apple_eaten += 1 #increases apples eaten if in position

                if self.apple_eaten % 2 == 0: #increases speed if apple is eaten
                    self.tick_speed -= 1
                
                if self.game_values['type'] in ['reverse','r']: #for reverse gamemode type
                    self.die_check() #checks if head overlaps with body before reversing fo no error occours
                    self.body_pos = self.body_pos[::-1] #changes body
                    self.last_pressed = self.opp[self.last_pressed] #changes key to opposite of current
                
                print('Apples eaten : {} , Speed : {}'.format(self.apple_eaten,self.tick_speed))
                self.make_apple() #if apple is eaten remake the apple in different position

            #this is for checking if dead and remaking body
            self.die_check()
            self.remake_body()
            self.make_eye()

            self.move_loop_id = self.root.after(self.tick_speed,lambda :self.move(self.last_pressed)) #for preventing speed increase

    def remake_body(self):
        #die check
        top = (0 , -self.game_values['cell_size']) #this is if head is over top border condition (y axis)
        bottom = (0 , self.game_values['row']*self.game_values['cell_size']) #this is if head is below bottom border condition (y axis)
        left = (-self.game_values['cell_size'] , 0) #this is if head is over left border condition (x axis)
        right = (self.game_values['column']*self.game_values['cell_size'] , 0) #this is if head is over right border condition (x axis)

        if (self.body_pos[0][1]) != (top[1]) and (self.body_pos[0][1]) != (bottom[1]) and (self.body_pos[0][0]) != (left[0]) and (self.body_pos[0][0]) != (right[0]): #remaking of snake only when it is inside border
            
            self.canvas.delete('snake_body') #deletes everything with the tag 'snake_body'
            self.canvas.delete('snake_eye') #deletes all eyes

            try: #cause i delete body_pos so i get error if i create a body so if i get error it checks if player is dead then it checks die
                #makes and colors body
                for index,item in enumerate(self.body_pos): #remakes evrything with new body position
                    if index == 0: #colors head
                        self.head = self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#189f11',tag = 'snake_body') #bbox gets coords of object

                    elif index == len(self.body_pos) - 1: #colors tail also -1 cause index stop at len -1
                        self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#175e13',tag = 'snake_body')
                    else: #colors body
                        self.canvas.create_oval(self.canvas.bbox(self.grid_loc_reverse[item]),fill='#168211',tag = 'snake_body')

            except KeyError: #only if the error is keyerror
                self.die_check() #error check and game_over doesnt run more than once
        
        else:
            if self.game_values['mode'] in ['normal','n']: #for normal gamemode
                self.game_over()

            elif self.game_values['mode'] in ['infinite','i']: #for infinite gamemode

                if self.body_pos[0][1] == top[1]: #this is if it goes over top border
                    y = self.body_pos[0][1] + self.game_values['row']*self.game_values['cell_size'] #makes new coords for head
                    x = self.body_pos[0][0]

                    self.body_pos[0] = (x,y) #replaces old coords

                elif self.body_pos[0][1] == bottom[1]: #this is if it goes below bottom border
                    y = self.body_pos[0][1] - self.game_values['row']*self.game_values['cell_size'] #makes new coords for head
                    x = self.body_pos[0][0]

                    self.body_pos[0] = (x,y) #replaces old coords
                
                elif self.body_pos[0][0] == left[0]: #this is if it goes over left border
                    y = self.body_pos[0][1]
                    x = self.body_pos[0][0] + self.game_values['column']*self.game_values['cell_size'] #makes new coords for head

                    self.body_pos[0] = (x,y) #replaces old coords

                elif self.body_pos[0][0] == right[0]: #this is if it goes over right border
                    y = self.body_pos[0][1]
                    x = self.body_pos[0][0] - self.game_values['column']*self.game_values['cell_size'] #makes new coords for head

                    self.body_pos[0] = (x,y) #replaces old coords

                self.remake_body()
                self.make_eye()
    
    def make_eye(self): #the eyes are just round(self.ga...cell_size../1.6) here and there just switched between x1,y1,x2,y2
        #left right is just up down eyes but in that side
        try: #cause there is a unpacking error when making eyes cause head is nothing after dying
            if self.game_state['start'] == True: #cause snake looks broken like twisted if i make left right in start
                if self.last_pressed == 'Up':
                    padding = self.game_values['cell_size']//(10**int((len(str(self.game_values['cell_size']))-1))) #for getting optimal distance for pupil
                    #gets cell size gets first digit of cell_size using len of the cell_size

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1,y1,x2-(round(self.game_values['cell_size']/1.6)),y2-(round(self.game_values['cell_size']/1.6)))) #idk how 1.6 works but it works perfectly fine for eyes
                    left_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(left_eye)
                    x1,y1,x2,y2 = map(round,(x1+padding ,y1,
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    left_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')


                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1+(round(self.game_values['cell_size']/1.6)),y1,
                                            x2,y2-(round(self.game_values['cell_size']/1.6))))
                    right_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(right_eye)
                    x1,y1,x2,y2 = map(round,(x1+padding ,y1,
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    right_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')

                elif self.last_pressed == 'Down':
                    padding = self.game_values['cell_size']//(10**int((len(str(self.game_values['cell_size']))-1))) #for getting optimal distance for pupil
                    #gets cell size gets first digit of cell_size using len of the cell_size

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1,y1+(round(self.game_values['cell_size']/1.6)),
                                            x2-(round(self.game_values['cell_size']/1.6)),y2))
                    down_left_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')


                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1+(round(self.game_values['cell_size']/1.6)),y1+(round(self.game_values['cell_size']/1.6)),x2,y2)) #idk how 1.6 works but it works perfectly fine for eyes
                    down_right_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')
                
                elif self.last_pressed == 'Right':
                    padding = self.game_values['cell_size']//(10**int((len(str(self.game_values['cell_size']))-1))) #for getting optimal distance for pupil
                    #gets cell size gets first digit of cell_size using len of the cell_size

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1+(round(self.game_values['cell_size']/1.6)),y1,
                                            x2,y2-(round(self.game_values['cell_size']/1.6))))
                    right_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1+(round(self.game_values['cell_size']/1.6)),y1+(round(self.game_values['cell_size']/1.6)),x2,y2)) #idk how 1.6 works but it works perfectly fine for eyes
                    down_right_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')
                
                elif self.last_pressed == 'Left':
                    padding = self.game_values['cell_size']//(10**int((len(str(self.game_values['cell_size']))-1))) #for getting optimal distance for pupil
                    #gets cell size gets first digit of cell_size using len of the cell_size

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1,y1,x2-(round(self.game_values['cell_size']/1.6)),y2-(round(self.game_values['cell_size']/1.6)))) #idk how 1.6 works but it works perfectly fine for eyes
                    left_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(self.head)
                    x1,y1,x2,y2 = map(round,(x1,y1+(round(self.game_values['cell_size']/1.6)),
                                            x2-(round(self.game_values['cell_size']/1.6)),y2))
                    down_left_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')
            
            else: #just updates direction of pupils when choosing direction
                padding = self.game_values['cell_size']//(10**int((len(str(self.game_values['cell_size']))-1)))

                x1,y1,x2,y2 = self.canvas.bbox(self.head)
                x1,y1,x2,y2 = map(round,(x1,y1,x2-(round(self.game_values['cell_size']/1.6)),y2-(round(self.game_values['cell_size']/1.6)))) #idk how 1.6 works but it works perfectly fine for eyes
                left_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                x1,y1,x2,y2 = self.canvas.bbox(self.head)
                x1,y1,x2,y2 = map(round,(x1+(round(self.game_values['cell_size']/1.6)),y1,
                                        x2,y2-(round(self.game_values['cell_size']/1.6))))
                right_eye = self.canvas.create_oval((x1,y1,x2,y2), fill = "#ffffff",tag = 'snake_eye')

                if self.last_pressed == 'Up':
                    x1,y1,x2,y2 = self.canvas.bbox(left_eye)
                    x1,y1,x2,y2 = map(round,(x1+padding ,y1,
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    left_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(right_eye)
                    x1,y1,x2,y2 = map(round,(x1+padding ,y1,
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    right_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')
                
                elif self.last_pressed == 'Down': ... #snake cannot face down when starting

                elif self.last_pressed == 'Left':
                    x1,y1,x2,y2 = self.canvas.bbox(left_eye)
                    x1,y1,x2,y2 = map(round,(x1 ,y1+(round(self.game_values['cell_size']/(1.6*2))),
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    left_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')

                    x1,y1,x2,y2 = self.canvas.bbox(right_eye)
                    x1,y1,x2,y2 = map(round,(x1 ,y1+(round(self.game_values['cell_size']/(1.6*2))),
                    x2+padding-(round(self.game_values['cell_size']/(1.6*2))),y2-(round(self.game_values['cell_size']/(1.6*2))))) #cause eye is half of cell size then pupil is half of half of cell size

                    right_pupil = self.canvas.create_oval((x1,y1,x2,y2), fill = "#000000",tag = 'snake_eye')
                
                elif self.last_pressed == 'Right':
                    ...
    
        except TypeError: #unpacking error
            self.die_check()

    def die_check(self):
        if self.body_pos[0] in self.body_pos[1:]: #checks if head collides with body
            self.game_state['die'] = True #sets snake to dead
            self.game_over()

        elif self.game_state['die'] == True:
            self.game_over()

    def game_over(self,event=None):
        if event == None: #when game is first over
            print('You died press space to restart')
            for i in range(len(self.body_pos)-1): #makes it so error doesnt occur and game stops in normal mode cause removes all elements also doesnt affect display cause its in different
                    self.body_pos.pop()

            self.root.unbind('<Key>') #to remove changing keys from keybind
            self.root.bind('<Key>',lambda event:self.game_over(event))

        else: #when user presses key
            if event.char == ' ': #if user presses spacebar activates restart function
                self.root.unbind('<Key>')
                self.restart()

    def restart(self):
        self.root.after_cancel(self.move_loop_id) #after you die if you spam space the moving after stacks up so to remove the stacking it cancels the latest loop

        #remakes the entire body before restarting to show snake is there
        self.body_pos = []

        head_x , head_y = self.game_values['column']//2*self.game_values['cell_size'] , self.game_values['row']//2*self.game_values['cell_size'] #get coord of head position in center of board
        head_grid_no = self.grid_loc_reverse[(head_x,head_y)]
        # ^^ gets index of head then converts it into a number;first changes into string then into int

        for i in range(self.game_values['snake_size']): #runs till body size
            self.body_pos.append(self.grid_loc[head_grid_no]) #stores body id
            head_grid_no += self.game_values['column'] #cause diff btwn game_values['column'] is same so add to get other position
        
        self.last_pressed = 'Up' #cause head is in old position after dying

        self.make_apple()
        self.remake_body()
        self.make_eye()

        print('Press space to start')
        self.root.unbind('<Key>') #it was binded to self.reset

        #sets every function to default
        self.game_state = self.game_state_perm.copy()
        self.tick_speed = self.perm_tick_speed
        self.apple_eaten = 0

        self.root.bind('<Key>',self.change_key) #for starting game

if __name__ == '__main__': #this only makes snake run on this file so this wont affect menu
    game_values = {'cell_size': int(input('Cell Size: ')) ,'row': int(input('Row: ')),  'column': int(input('Column: ')), 'snake_size': int(input('Size of snake (when starting): ')), 'mode': input('Gamemode (normal[n]/infinite[i]): ').lower(), 'type': input('Gamemode Type (normal[n]/reverse[r]): ').lower()}

    #game_values = {'cell_size': 40 , 'column': 15, 'row': 12, 'snake_size': 4, 'mode': 'n', 'type': 'r'}

    if game_values['column']%2 == 0: #if game_values['column'] is even no the checkerboard wont appear
        game_values['column']+=1

    root = tk.Tk()
    root.focus_force() #puts focus in the game window once done typing inputs
    root.geometry(f"{(game_values['column']+2)*game_values['cell_size']}x{(game_values['row']+3)*game_values['cell_size']}") #changes geomerty based on input
    root.title('SNAKE_W_CANV')
    snake_canv(root,game_values)
    root.resizable(False,False) #stops fullscreen
    root.mainloop()
