from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import math


def gridfunc(event): #regular gridlines function
    ax.grid() #This works because for some reason mpl auto-negates .grid() when grid is already true
    plt.draw()

def minkfuncoff(event): #minkovski gridlines function
    if minkfuncoff.counter % 2 == 1: #The counter allows one button for both on and off
        print(len(lines)) #not needed, just for debugging
        ax.lines = [] #empties the lines set. The lines aren't actuaally plotted at any point, just placed in plotted set lines.
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1 #increments counter.
        print(minkfuncoff.counter) #not needed, just for debugging
    elif minkfuncoff.counter % 2 == 0:
        linedraw(x, beta, scale) #redraws the lines
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1 #increments counter
    
def linedraw(x, beta, scale): #this draws the lines
    lines.append(ax.plot(x, beta*x, '-r', label='ct prime axis')) #This adds the ct prime axis to lines.
    lines.append(ax.plot(x, (1/beta)*x,'-.g', label='x prime axis')) #This adds x prime to lines
    for y in np.arange(-10 * scale, 10 * scale, scale): # Ten lines on either side should do it. Scale is float, not int, so numpy is needed
        lines.append(ax.plot(x, beta*x + y, '-r', label=y)) #Technically, both axes are doubly drawn. mpl doubles the light intensity shading for some reason. Cool intensity effect. Emphasizes the axes.
        lines.append(ax.plot(x, (1/beta)*x + y, '-.g', label=y))

minkfuncoff.counter = 0    
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(-5,5,100) #Tech nically this could be anything else.
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

beta = 0.5 #NEED TO MAKE THIS CUSTOMIZABLE VIA SOME SORT OF SLIDER
scale = math.sqrt((1 + beta ** 2) / (1 - beta ** 2)) # Normal scale function
lines = [] #set lines starts empty
linedraw(x, beta, scale) # defaults to having line drawn

plt.xlim(-5, 5) #arbitrary, but makes it centered and nice looking.
plt.ylim(-10, 10) #same

gridbutton = plt.axes([0.51, 0.01, 0.2, 0.075]) #Buttons may need to be smaller
bgridfunc = Button(gridbutton, 'Regular Gridlines!', color = 'grey', hovercolor = 'green')
bgridfunc.on_clicked(gridfunc)

minkgridbuttonoff = plt.axes([0.21, 0.01, 0.2, 0.075])
mgridfuncoff = Button(minkgridbuttonoff, 'Minkowski Gridlines!', color = 'grey', hovercolor = 'green')
mgridfuncoff.on_clicked(minkfuncoff)

plt.show()
