from urllib.request import urlopen
import re
import tkinter
import time
from datetime import datetime
import numpy as np

def radians(degrees):
    return degrees*(np.pi/180)

def to_seconds(arg):
    data = re.findall(' (.*?)m', arg)[0]
    clock = int(''.join([i for i in re.findall('(.*?) ', data)[0] if i != ':']))
    if clock > 1159 and data[-1] == 'a':
        clock -= 1200
    if data[-1] == 'p' and clock < 1200:
        clock += 1200
    clock = str(clock)
    while len(clock) < 4:
        clock = ''.join(['0']+list(clock))
    seconds = (int(clock[0:2])*3600)+(int(clock[2:])*60)
    if arg[0:3] != datetime.today().strftime('%A')[0:3]:
        seconds += 86400
    return seconds

def now_seconds():
    now = str(datetime.now())
    hm = str(now)[11:16]
    clock = ''.join([i for i in hm if i != ':'])
    seconds = float((int(clock[0:2])*3600)+(int(clock[2:])*60)) + float(now[17:])
    return seconds

def ang_velocity(body):
    rise = to_seconds(body.rise)
    set = to_seconds(body.set)
    time_span = set - rise
    return np.pi/time_span

def circle(x, y, r, canvas, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, outline=color)

def ball(r, theta, canvas, color):
    r = -r
    theta = theta
    x = r*np.cos(theta) + (C_width/2)
    y = r*np.sin(theta) + (C_height/2)
    size = 5
    x0 = x - size
    y0 = y - size
    x1 = x + size
    y1 = y + size
    return canvas.create_oval(x0, y0, x1, y1, outline=color, fill=color)

class HTML:
    def __init__(self):
        self.sun = urlopen('https://www.timeanddate.com/sun/usa/toledo').read().decode('utf-8')
        self.moon = urlopen('https://www.timeanddate.com/moon/usa/toledo').read().decode('utf-8')
        self.planets = urlopen('https://www.timeanddate.com/astronomy/night/usa/toledo').read().decode('utf-8')

class Body:
    def __init__(self, name):
        self.name = name
        if name == 'Sun':
            self.rise = re.findall("Sunrise Today: </th><td>(.*?)<span", html.sun)[0]
            self.set = re.findall("Sunset Today: </th><td>(.*?)<span", html.sun)[0]
        elif name == 'Moon':
            self.alt = re.findall("moonalt>(.*?)</td", html.moon)[0]
            self.phase = re.findall("moon-percent>(.*?)</span", html.moon)[0]
            #self.rise = re.findall("Next Moonrise: </th><td>(.*?)</td>", html.moon)[0]
            #The above is sometimes "Next Moonset"
        else:
            stats = re.findall('>([^"]*)</td', re.findall(name+"</th><td class=\"c\" (.*?)<td>", html.planets)[0])
            self.rise = stats[0]
            self.mid = stats[2]
            self.set = stats[1]
            self.vis = re.findall('</td><td>([^"]*)</td>', re.findall(name+"</th><td class=\"c\" (.*?)</tr>", html.planets)[0])[0]
            self.ang_velocity = None
            self.angle = 0
            self.move_amount = None
            self.rad = (len(bodies)+5)*10
            self.color = None
            self.ball = None

            bodies.append(self)

    def update(self):
        old_angle = self.angle
        self.angle = ((now_seconds()-float(to_seconds(self.rise))%86400)*self.ang_velocity)%(2*np.pi)
        self.move_amount = [self.rad*(np.cos(self.angle)-np.cos(old_angle)), self.rad*(np.sin(self.angle)-np.sin(old_angle))]

window = tkinter.Tk()
C_height = 300
C_width = 300
C = tkinter.Canvas(window,height=C_height,width=C_width)
C.pack()

while True:

    bodies = []

    html = HTML()
    sun = Body('Sun')
    moon = Body('Moon')
    mercury = Body('Mercury')
    mercury.color = 'brown'
    venus = Body('Venus')
    venus.color = 'gray'
    mars = Body('Mars')
    mars.color = 'red'
    jupiter = Body('Jupiter')
    jupiter.color = 'orange'
    saturn = Body('Saturn')
    saturn.color = 'beige'
    uranus = Body('Uranus')
    uranus.color = 'cyan'
    neptune = Body('Neptune')
    neptune.color = 'blue'

    for b in bodies:
        b.ang_velocity = ang_velocity(b)
        b.update()

    mercury.ball = ball(mercury.rad, mercury.angle, C, mercury.color)
    venus.ball = ball(venus.rad, venus.angle, C, venus.color)
    mars.ball = ball(mars.rad, mars.angle, C, mars.color)
    jupiter.ball = ball(jupiter.rad, jupiter.angle, C, jupiter.color)
    saturn.ball = ball(saturn.rad, saturn.angle, C, saturn.color)
    uranus.ball = ball(uranus.rad, uranus.angle, C, uranus.color)
    neptune.ball = ball(neptune.rad, neptune.angle, C, neptune.color)

    mercury_circle = circle(C_height/2, C_width/2, mercury.rad, C, mercury.color)
    venus_circle = circle(C_height/2, C_width/2, venus.rad, C, venus.color)
    mars_circle = circle(C_height/2, C_width/2, mars.rad, C, mars.color)
    jupiter_circle = circle(C_height/2, C_width/2, jupiter.rad, C, jupiter.color)
    saturn_circle = circle(C_height/2, C_width/2, saturn.rad, C, saturn.color)
    uranus_circle = circle(C_height/2, C_width/2, uranus.rad, C, uranus.color)
    neptune_circle = circle(C_height/2, C_width/2, neptune.rad, C, neptune.color)

    for i in range(86400):

        for b in bodies:
            b.update()
            C.move(b.ball, -b.move_amount[0], -b.move_amount[1])
            window.update()
        time.sleep(1)

window.mainloop()
