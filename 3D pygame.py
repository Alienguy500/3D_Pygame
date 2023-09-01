# 3D stuff in pygame
# Made by u/Alienguy500

import pygame, math
from sys import exit


pygame.init()
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()

# Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Camera coordinates
cx = 0
cy = 0
cz = 0

# Camera velocity
cxv = 0
cyv = 0
czv = 0

# Camera rotation
yaw = 0
pitch = 0

fov = 300

speed = 1

def deg2rad(angle):
    """
    Convert an angle from degrees to radians
    """
    angle /= 180
    angle *= math.pi
    return angle

def rotate(x0,y0,z0,cx,cy,cz,angle,axis:str):
    """
    Rotate a point about another by any angle (in radians)
    """
    x0 -= cx
    y0 -= cy
    z0 -= cz
    if axis == 'X':
        x1 = x0
        y1 = y0*math.cos(angle) - z0*math.sin(angle)
        z1 = y0*math.sin(angle) + z0*math.cos(angle)
    
    elif axis == 'Y':
        x1 = x0*math.cos(angle) + z0*math.sin(angle)
        y1 = y0
        z1 = z0*math.cos(angle) - x0*math.sin(angle)
    elif axis == 'Z':
        x1 = x0*math.cos(angle) - y0*math.sin(angle)
        y1 = x0*math.sin(angle) + y0*math.cos(angle)
        z1 = z0
    x1 += cx
    y1 += cy
    z1 += cz
    return x1,y1,z1

def goTo(pos:tuple):
    """goTo function
    
    This function converts 3-dimensional coordinates into 2-dimensional screen coordinates

    pos: tuple must contain 3 real numbers
    """
    x = float(pos[0])
    y = float(pos[1])
    z = float(pos[2])
    
    yaw_rotation = rotate(x,y,z,cx,cy,cz,deg2rad(yaw),'Y')
    x,y,z = yaw_rotation[0],yaw_rotation[1],yaw_rotation[2]
    p_rot = rotate(x,y,z,cx,cy,cz,deg2rad(pitch),'X') # After the rotation in the yaw, the X axis is now perpendicular to the camera's direction
    x,y,z = p_rot[0],p_rot[1],p_rot[2]
    x -= cx
    y -= cy
    z -= cz
    x *= fov
    y *= fov
    if z <= 0:
        return 'error'
    # Flatten the 3D coordinates into 2D
    x /= z
    y /= z
    x += screen.get_width()/2
    y *= -1
    y += screen.get_height()/2
    return float(x),float(y)

def drawline(colour, start: tuple, end: tuple, width:int=1):
    '''
    Draw a 3D line between two points
    '''
    x1 = start[0]
    y1 = start[1]
    z1 = start[2]
    x2 = end[0]
    y2 = end[1]
    z2 = end[2]
    if goTo((x1,y1,z1)) != 'error' and goTo((x2,y2,z2)) != 'error':
        pygame.draw.line(screen,colour,goTo((x1,y1,z1)),goTo((x2,y2,z2)),width)

def go2d(pos:tuple):
    '''
    Does the same as goTo but in 2D
    '''
    x = float(pos[0])
    y = float(pos[1])
    x += screen.get_width()/2
    y *= -1
    y += screen.get_height()/2
    return float(x),float(y)

def comeFrom(x,y):
    """Convert coordinates from the 'goTo' system back to the default
    
    See goTo function for more details
    """
    x -= (screen.get_width())//2
    y -= (screen.get_height())//2
    y = y*-1
    return (x,y)

def drawHitbox(x1,y1,z1,x2,y2,z2):
    """
    This function draws an outline for hitboxes

    Only works for cuboids
    """
    coords = [(x1,y1,z1),#0
              (x2,y1,z1),#1
              (x1,y2,z1),#2
              (x2,y2,z1),#3
              (x1,y1,z2),#4
              (x2,y1,z2),#5
              (x1,y2,z2),#6
              (x2,y2,z2)]#7
    drawline(white,coords[0],coords[1],4)
    drawline(white,coords[0],coords[2],4)
    drawline(white,coords[3],coords[2],4)
    drawline(white,coords[3],coords[1],4)
    drawline(white,coords[0],coords[4],4)
    drawline(white,coords[1],coords[5],4)
    drawline(white,coords[2],coords[6],4)
    drawline(white,coords[3],coords[7],4)
    drawline(white,coords[4],coords[5],4)
    drawline(white,coords[4],coords[6],4)
    drawline(white,coords[7],coords[6],4)
    drawline(white,coords[7],coords[5],4)
    

class cube:
    def __init__(self,x,y,z,w,h,l,xv,yv,zv,onGround: bool):
        self.x = x
        self.y = y
        self.z = z
        self.l = l
        self.w = w
        self.h = h
        self.xv = xv
        self.yv = yv
        self.zv = zv
        self.onGround = onGround
    def draw(self):
        drawHitbox(self.x,self.y,self.z,self.x+self.w,self.y+self.h,self.z+self.l)

cubes = [cube(0,0,10,100,100,100,0,0,0,True),cube(0,200,10,100,100,100,0,0,0,False)]

pygame.mouse.set_pos(go2d((0,0)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(black)

    key_input = pygame.key.get_pressed()
    mouse_input = pygame.mouse.get_pressed(num_buttons=5)
    #game code
    for i in cubes:
        i.draw()
    if key_input[pygame.K_ESCAPE]:
        pygame.quit()
        exit()

    mousepos = comeFrom(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    yaw -= mousepos[0]
    pitch += mousepos[1]
    pygame.mouse.set_pos(go2d((0,0)))
    if pitch > 90:
        pitch = 90
    if pitch < -90:
        pitch = -90
    
    if mouse_input[3]:
        fov += 1
    if mouse_input[4]:
        fov -= 1

    if key_input[pygame.K_w]:
        czv += speed*(math.cos(deg2rad(-1*yaw)))
        cxv += speed*(math.sin(deg2rad(-1*yaw)))
    if key_input[pygame.K_s]:
        czv -= speed*(math.cos(deg2rad(-1*yaw)))
        cxv -= speed*(math.sin(deg2rad(-1*yaw)))
    if key_input[pygame.K_d]:
        cxv += speed*(math.cos(deg2rad(yaw)))
        czv += speed*(math.sin(deg2rad(yaw)))
    if key_input[pygame.K_a]:
        cxv -= speed*(math.cos(deg2rad(yaw)))
        czv -= speed*(math.sin(deg2rad(yaw)))
    if key_input[pygame.K_SPACE]:
        cyv += 1
    if key_input[pygame.K_LSHIFT]:
        cyv -= 1
    if key_input[pygame.K_l]:
        yaw += 1
    if key_input[pygame.K_j]:
        yaw -= 1
    if key_input[pygame.K_i]:
        pitch += 1
    if key_input[pygame.K_k]:
        pitch -= 1
    if key_input[pygame.K_LCTRL]:
        speed = 2
    else:
        speed = 1
    
    
    cx += cxv
    cy += cyv
    cz += czv

    cxv *= 0.9
    cyv *= 0.9
    czv *= 0.9

    pygame.display.update()
    clock.tick(60)