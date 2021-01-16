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
    risen_time = set - rise
    set_time = 86400 - risen_time
    if rise < now_seconds() < set:
        body.status = 'risen'
        return np.pi/risen_time
    elif now_seconds() < rise or now_seconds() > set:
        body.status = 'set'
        return -np.pi/set_time

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

class Body:
    def __init__(self, name):
        self.name = name
        self.ang_velocity = 0
        self.angle = 0
        self.move_amount = None
        self.color = None
        self.ball = None
        self.rad = None
        self.status = None
        if name == 'Sun':
            self.rise = datetime.today().strftime('%A')[0:3]+' '+re.findall("Sunrise Today: </th><td>(.*?)<span", html)[0]
            self.set = datetime.today().strftime('%A')[0:3]+' '+re.findall("Sunset Today: </th><td>(.*?)<span", html)[0]
            bodies.append(self)
        elif name == 'Moon':
            self.phase = re.findall("moon-percent>(.*?)</span", html)[0]
            self.rise = datetime.today().strftime('%A')[0:3]+' '+re.findall("Moonrise Today: </th><td>(.*?)<span", html)[0]
            self.set = datetime.today().strftime('%A')[0:3]+' '+re.findall("Moonset Today: </th><td>(.*?)<span", html)[0]
            self.arcsize = None
            bodies.append(self)
        else:
            stats = re.findall('>([^"]*)</td', re.findall(name+"</th><td class=\"c\" (.*?)<td>", html)[0])
            self.rise = stats[0]
            self.mid = stats[2]
            self.set = stats[1]
            self.vis = re.findall('</td><td>([^"]*)</td>', re.findall(name+"</th><td class=\"c\" (.*?)</tr>", html)[0])[0]
            self.rad = (len(bodies)+5)*10
            bodies.append(self)

    def update(self):
        old_angle = self.angle
        if self.status == 'risen':
            self.angle = ((now_seconds()-float(to_seconds(self.rise))%86400)*self.ang_velocity)%(2*np.pi)
        elif self.status == 'set':
            self.angle = ((((float(to_seconds(self.set))%86400)-now_seconds())*self.ang_velocity)%(2*np.pi))+np.pi
        self.move_amount = [self.rad*(np.cos(self.angle)-np.cos(old_angle)), self.rad*(np.sin(self.angle)-np.sin(old_angle))]

location = str(input('input your city (all lowercase): '))

window = tkinter.Tk()
C_height = 300
C_width = 300
C = tkinter.Canvas(window,height=C_height,width=C_width)
C.pack()

while True:

    bodies = []

    html = urlopen('https://www.timeanddate.com/astronomy/usa/'+location).read().decode('utf-8')
    sun = Body('Sun')
    sun.color = 'yellow'
    moon = Body('Moon')
    moon.color = 'gray'
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
    sun.rad = neptune.rad
    moon.rad = neptune.rad
    moon.arcsize = mercury.rad + 40

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
    sun.ball = ball(sun.rad, sun.angle, C, "")
    moon.ball = ball(moon.rad, moon.angle, C, "")

    mercury_circle = circle(C_height/2, C_width/2, mercury.rad, C, mercury.color)
    venus_circle = circle(C_height/2, C_width/2, venus.rad, C, venus.color)
    mars_circle = circle(C_height/2, C_width/2, mars.rad, C, mars.color)
    jupiter_circle = circle(C_height/2, C_width/2, jupiter.rad, C, jupiter.color)
    saturn_circle = circle(C_height/2, C_width/2, saturn.rad, C, saturn.color)
    uranus_circle = circle(C_height/2, C_width/2, uranus.rad, C, uranus.color)
    neptune_circle = circle(C_height/2, C_width/2, neptune.rad, C, neptune.color)

    horizon = C.create_line((C_width/2)-neptune.rad, C_height/2, (C_width/2)+neptune.rad, C_height/2)
    sunline = C.create_line(C_width/2, C_height/2, (C_width/2)-sun.rad*np.cos(sun.angle), (C_height/2)-sun.rad*np.sin(sun.angle), fill=sun.color)
    moonline = C.create_line(C_width/2, C_height/2, (C_width/2)-moon.rad*np.cos(moon.angle), (C_height/2)-moon.rad*np.sin(moon.angle), fill=moon.color)
    moonarc =  C.create_arc(C_width-moon.arcsize, C_height-moon.arcsize, moon.arcsize, moon.arcsize, start=0, extent=359.99*float(moon.phase[0:3])/100, fill=moon.color, outline='')
    mooncirc = C.create_arc(C_width-moon.arcsize, C_height-moon.arcsize, moon.arcsize, moon.arcsize, start=0, extent=359.99, outline=moon.color)

    for i in range(86400):
        C.delete(sunline)
        C.delete(moonline)
        C.delete(moonarc)
        for b in bodies:
            b.update()
            C.move(b.ball, -b.move_amount[0], -b.move_amount[1])
        sunline = C.create_line(C_width/2, C_height/2, (C_width/2)-sun.rad*np.cos(sun.angle), (C_height/2)-sun.rad*np.sin(sun.angle), fill=sun.color)
        moonline = C.create_line(C_width/2, C_height/2, (C_width/2)-moon.rad*np.cos(moon.angle), (C_height/2)-moon.rad*np.sin(moon.angle), fill=moon.color)
        moonarc =  C.create_arc(C_width-moon.arcsize, C_height-moon.arcsize, moon.arcsize, moon.arcsize, start=0, extent=359.99*float(moon.phase[0:3])/100, fill=moon.color, outline='')
        window.update()
        time.sleep(5)

window.mainloop()
