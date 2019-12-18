#2019, Shmuel Padwa

from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
import numpy as np
import math


def gridfunc(event):
    ax.grid()
    plt.draw()

def minkfuncoff(event):
    if minkfuncoff.counter % 2 == 0:
        ax.lines = []
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1
    elif minkfuncoff.counter % 2 == 1:
        beta = betaslider.val
        linedraw(x, beta, scale)
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1
    
def linedraw(x, beta, scale):
    lines.append(ax.plot(x, beta*x, '-r', label='ct prime axis'))
    lines.append(ax.plot(x, (1/beta)*x,'-..g', label='x prime axis'))
    for y in np.arange(-10 * scale, 10 * scale, scale):
        lines.append(ax.plot(x, beta*x + y, '-r', label=y))
        lines.append(ax.plot(x, (1/beta)*x + y, '-..g', label=y))

def onclick(event):
    #print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %(event.button, event.x, event.y, event.xdata, event.ydata))
    if event.y > 95: 
        sc.append(ax.scatter(event.xdata, event.ydata, s=30, color = 'red'))
        stevents.append([round(event.xdata,3), round(event.ydata,3)])
        betastevents.append([round((gamma * (event.xdata - beta * event.ydata)),3), round((gamma * (event.ydata - beta * event.xdata)),3)])
        fig.canvas.draw()
        ''' The y>95 line is needed because the code was throwing a very bizarre bug in which clicking
        * the minkowski or regular gridline buttons would plot a point on the grid
        *specifically the point at which you'd be clicking if the button was at (0,0)
        *It coulnd't distinguish between xdata and ydata from the grid and the buttons.
        *Fortunately, It can distinguish between x and y from the grid and buttons.
        '''
        plt.draw()


def betachange(beta):
    beta = betaslider.val
    ax.lines = []
    linedraw(x, beta, scale)
    if minkfuncoff.counter % 2 == 1:
        minkfuncoff.counter = minkfuncoff.counter + 1
    if lightconefunc.counter % 2 == 0:
        lightconefunc.counter = lightconefunc.counter + 1
    for z in range(len(stevents)):
        betastevents[z][0] = round(gamma * (stevents[z][0] - beta * stevents[z][1]),3)
        betastevents[z][1] = round(gamma * (stevents[z][1] - beta * stevents[z][0]),3)
    #print(betastevents)
    plt.draw()

def lightconefunc(event):
    if lightconefunc.counter % 2 == 1:
        for p in range(len(stevents)):
            lightcones.append(ax.plot(x, x + stevents[p][1] - stevents[p][0], '-b'))
            lightcones.append(ax.plot(x, -x + stevents[p][1] + stevents[p][0], '-b'))
            plt.draw()
        lightconefunc.counter = lightconefunc.counter + 1
    elif lightconefunc.counter % 2 == 0:
        ax.lines = [] #main bug:turning off lightcones kills minkowski lines for some reason
        #Okay watch this trick: Instead of figuring out why this isn't working
        #we're going to call minkfuncoff and pretend like there isn't a problem
        #by doing it before plt.draw(), the user can't even notice!
        #I am such a fraud
        if minkfuncoff.counter % 2 == 0:
            minkfuncoff.counter = minkfuncoff.counter + 1
            minkfuncoff(event)
        plt.draw()
        lightconefunc.counter = lightconefunc.counter + 1

minkfuncoff.counter = 0
lightconefunc.counter = 1


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(-5,5,100)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.xlim(-5, 5)
plt.ylim(-10, 10)

plt.subplots_adjust(bottom=0.2)

gridbutton = plt.axes([0.41, 0.11, 0.25, 0.075])
bgridfunc = Button(gridbutton, 'Regular Gridlines!', color = 'grey', hovercolor = 'green')
bgridfunc.on_clicked(gridfunc)

minkgridbuttonoff = plt.axes([0.15, 0.11, 0.25, 0.075])
mgridfuncoff = Button(minkgridbuttonoff, 'Minkowski Gridlines!', color = 'grey', hovercolor = 'green')
mgridfuncoff.on_clicked(minkfuncoff)

lightconebutton = plt.axes([0.67, 0.11, 0.25, 0.075])
lightcone = Button(lightconebutton, 'Lightcone toggle!', color = 'grey', hovercolor = 'green')
lightcone.on_clicked(lightconefunc)

slid1 = plt.axes([0.1, 0.03, 0.8, 0.075])
betaslider = Slider(slid1, 'Beta!', valmin = 0.5, valmax = 0.99, valinit = 0.7, valfmt = '%1.3f', color = 'pink')
betaslider.on_changed(betachange)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

beta = betaslider.val
scale = math.sqrt((1 + beta ** 2) / (1 - beta ** 2))
gamma = 1 / math.sqrt((1-beta**2))
lines = []
lightcones = []
linedraw(x, beta, scale)

stevents = [] #spacetime events
betastevents = []
for x in range(len(stevents)):
    betastevents[x][0] = round(gamma * (stevents[x][0] - beta * stevents[x][1]), 3)
    betastevents[x][1] = round(gamma * (stevents[x][1] - beta * stevents[x][0]), 3)
sc = []
plt.show()
