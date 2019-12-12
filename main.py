from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import numpy as np
import math


def gridfunc(event):
    ax.grid()
    plt.draw()

def minkfuncoff(event):
    if minkfuncoff.counter % 2 == 1:
        print(len(lines))
        ax.lines = []
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1
        print(minkfuncoff.counter)
    elif minkfuncoff.counter % 2 == 0:
        linedraw(x, beta, scale)
        plt.draw()
        minkfuncoff.counter = minkfuncoff.counter + 1
    
def linedraw(x, beta, scale):
    lines.append(ax.plot(x, beta*x, '-r', label='ct prime axis'))
    lines.append(ax.plot(x, (1/beta)*x,'-.g', label='x prime axis'))
    for y in np.arange(-10 * scale, 10 * scale, scale):
        lines.append(ax.plot(x, beta*x + y, '-r', label=y))
        lines.append(ax.plot(x, (1/beta)*x + y, '-.g', label=y))

minkfuncoff.counter = 0    
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(-5,5,100)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

beta = 0.5
scale = math.sqrt((1 + beta ** 2) / (1 - beta ** 2))
lines = []
linedraw(x, beta, scale)

plt.xlim(-5, 5)
plt.ylim(-10, 10)

gridbutton = plt.axes([0.51, 0.01, 0.2, 0.075])
bgridfunc = Button(gridbutton, 'Regular Gridlines!', color = 'grey', hovercolor = 'green')
bgridfunc.on_clicked(gridfunc)

minkgridbuttonoff = plt.axes([0.21, 0.01, 0.2, 0.075])
mgridfuncoff = Button(minkgridbuttonoff, 'Minkowski Gridlines!', color = 'grey', hovercolor = 'green')
mgridfuncoff.on_clicked(minkfuncoff)
plt.show()
