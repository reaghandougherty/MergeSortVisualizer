from tkinter import *
from tkinter import ttk
import random
import numpy as np
import time
import math

_WIDTH_ = 800
_HEIGHT_ = 600



def syncArrayWithScreen(top_k):
    global N
    global array
    global width_bar
    global gap
    
    #print(f'N is now: {N}')
  
    
    temp = array.copy()
    
    for i,val in enumerate(array):
        x1 = 10+i*(width_bar+gap)
        x2 = 10+(i+1)*width_bar+i*gap
        
        if (top_k > 0 and i >= (N-top_k)):
            canvas.itemconfigure(rectangles[i], fill='green')
        elif (top_k == -1):
            canvas.itemconfigure(rectangles[i], fill='grey')
        else:
            canvas.itemconfigure(rectangles[i],fill='blue')
        
        canvas.coords(rectangles[i], x1, 600, x2, 600-val)
        
        canvas.itemconfigure(text_above[i],text=str(val))
        canvas.coords(text_above[i], ((x1+x2)//2,600-val-25))
        
    #
    fps = fps_slider.get()
    #print(f'fps is now: {fps}')
    #

    canvas.update()
    time.sleep(1/fps)
    
###
# regenerate screen for new N value
def regenArray(new_N):
    global N
    N=new_N

    global width_bar
    global gap
    width_bar = 1536 / (3*N-1)
    gap = width_bar // 2

    #reset canvas rectangles/text
    for r in rectangles:
        canvas.delete(r)
    for ta in text_above:
        canvas.delete(ta)
    
    rectangles.clear()
    text_above.clear()
    
    global array
    global isUserData
    
    if not isUserData:
        print("not user data")
        array=generateRandomArray(N)

    for i, num in enumerate(array):
        
        x1 = 10+i*(width_bar+gap)
        x2 = 10+(i+1)*width_bar+i*gap
        
        rect = canvas.create_rectangle(x1,600,x2,600-num,fill='grey')  #from the bottom
        # create a label for the bar
        txt = canvas.create_text(((x1+x2)//2,600-num-25),text=str(num))
        
        rectangles.append(rect)
        text_above.append(txt)
    
    print(rectangles)
    #print(text_above)    
    
    #print(canvas)
    #   
    
    canvas.update()
    time.sleep(1/fps)
    
    syncArrayWithScreen(0)
###

# generate a randomized array of given length
def generateRandomArray(length):
    arr = []
    L = range(200) #number will be between 0 and 200
    for i in range(0,length):
        arr.append(random.choice(L))

    return arr
    

####   algorithms
def merge_sort(numbers, left, right):
    if (left < right):
        middle = (left + right) // 2

        merge_sort(numbers, left, middle)
        merge_sort(numbers, middle + 1, right)
        merge(numbers, left, middle, right)

def merge(numbers, left, middle, right):
    # define index iterators: 
    # left arr: [i,...,middle], right arr: [j,...,right]
    # working arr: [0,...,k,...,N-1]
    i = left
    j = middle + 1
    k = left

    # copy of the working array
    temp = numbers.copy()
    print(temp)
    
    # iterate until one of the sides runs out of items
    while (i <= middle and j <= right):
        
        syncArrayWithScreen(0)

        if (temp[i] <= temp[j]):
            numbers[k] = temp[i]
            
            syncArrayWithScreen(0)
            i += 1
        else:
            numbers[k] = temp[j]
            
            syncArrayWithScreen(0)
            j += 1

        k += 1
    
    #append remaining from left side
    while (i <= middle):

        numbers[k] = temp[i]
        syncArrayWithScreen(0)
        k += 1
        i += 1

    #append remaining from right side
    while (j <= right):

        numbers[k] = temp[j]
        
        syncArrayWithScreen(0)
        time.sleep(1/60)
        
        k += 1
        j += 1

####

def start():
    global N
    global array
    global k

    N=int(N_slider.get())
    k=int(k_slider.get())
    
    if (N <= k):
        #cannot happen
        return
    
    #syncArrayWithScreen(0)
    global N_onReset
    
    if (N != N_onReset):
        regenArray(N)
    
    
    print(f'Call to start() gave {array} and N: {N}')
    merge_sort(array, 0, N-1)
    
    syncArrayWithScreen(k)
    
    canvas.update()
    time.sleep(1/fps)
    
    print("DONE")
    #reset boolean
    global isUserData
    isUserData = False
    N_onReset = -1
            

def reset():
    #global reset on the array contents
    global array
    global N
    N=int(N_slider.get())
    k=int(k_slider.get())
    if (N <= k):
        #cannot happen
        return
    
    #syncArrayWithScreen(0)
    regenArray(N)
    global N_onReset
    N_onReset = N
    #array = generateRandomArray(N)
    
    print(f'Call to reset() gave {array}')
    syncArrayWithScreen(-1)

# ---
# read in custom data to sort through
def custom():
    
    
    new_win = Toplevel(win)
    new_win.title("Custom Data Input")
    new_win.geometry("300x300")
    
    # entry for user input
    #entry_text = StringVar()
    #entry = ttk.Entry(new_win, textvariable=entry_text, width=25)
    #entry.geometry("200x100")
    #entry.pack()
    
    #entry_text
    text=Text(new_win, height=5, width=25)
    text.pack()
    #text.insert(END,entry_text.get())
    
    # submit button
    submit_b = ttk.Button(new_win, text="Submit", command=lambda: process_data(text.get("1.0",END)))
    submit_b.pack(side='bottom')
    
    new_win.mainloop()
    
# process input data
def process_data(data):
    
    data = data.replace(" ", "").replace("\n","").replace("[","").replace("]","")
    
    print(data)
    user_list = []
    
    for val in data.split(","):
        if not val.isnumeric():
            # it is not a number
            print(f'{val} is not a valid number')
            return
        # it is a number
        user_list.append(int(val))
    
    #user_list should contain all the array values
    for usr_num in user_list:
        print(usr_num)
        
    global N
    global N_onReset
    global array
    global isUserData
    
    isUserData = True
    array = user_list
    N = len(user_list)
    N_onReset = len(user_list)
    N_slider.set(N)
    regenArray(N)
    

# ---

win = Tk()

#values
N = 40
N_onReset = -1
isUserData = False

k = 8

#initial fps
fps = 60


ttk.Label(win, text='Merge Sort Visualization').pack()
canvas = Canvas(win, width=800, height=600, bg='white')
canvas.pack()

ttk.Button(win,text='Sort',command=start).pack(side='left',padx=5,pady=5)
ttk.Button(win,text='Reset',command=reset).pack(side='left',padx=5)
#
ttk.Button(win,text='Custom', command=custom).pack(side='left',padx=5)
#

#----

# Labels and slider to control the speed of sorting (via fps variable)
fps_label = ttk.Label(win, text="FPS: 60")
fps_label.pack(side='left', padx=25)

fps_slider = ttk.Scale(win, from_=5, to=300, orient=HORIZONTAL,
                        length=150, command=lambda x_val: fps_label.config(text=f'FPS: {math.floor(float(x_val))}'))

#label.config(text=str(math.floor(x_val)))

fps_slider.set(60)
fps_slider.pack(side='left', padx=5)



#----


#init values for N and k here?
N_label = ttk.Label(win, text="N: 5")
N_label.pack(side='left', padx=15)

N_slider = ttk.Scale(win, from_=5, to=100, orient=HORIZONTAL,
                        length=100, command=lambda n_val: N_label.config(text=f'N: {math.floor(float(n_val))}'))

#label.config(text=str(math.floor(x_val)))

N_slider.set(5)
N_slider.pack(side='left', padx=5)

N=math.floor(N_slider.get())

global array
array = generateRandomArray(N)

print(f'initial was {array}')

#k
k_label = ttk.Label(win, text="k: 3")
k_label.pack(side='left', padx=15)

k_slider = ttk.Scale(win, from_=1, to=50, orient=HORIZONTAL,
                        length=100, command=lambda k_val: k_label.config(text=f'k: {math.floor(float(k_val))}'))

#label.config(text=str(math.floor(x_val)))

k_slider.set(3)
k_slider.pack(side='left', padx=5)

k=math.floor(k_slider.get())


#----

width_bar = 1536 / (3*N-1)
gap = width_bar // 2

rectangles = []
text_above = []

for i, num in enumerate(array):
    
    x1 = 10+i*(width_bar+gap)
    x2 = 10+(i+1)*width_bar+i*gap
    
    rect = canvas.create_rectangle(x1,600,x2,600-num,fill='grey')  #from the bottom
    # create a label for the bar
    txt = canvas.create_text(((x1+x2)//2,600-num-25),text=str(num))
    
    rectangles.append(rect)
    text_above.append(txt)
    
canvas.update()
time.sleep(1/fps)
    


win.mainloop()





