import pygame
#uso de teclado y raton
from pygame.locals import * 
from pygame.constants import *  

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga la blblioteca para el manejo de texturas
#from PIL import Image

# IMPORT OBJECT LOADER
from objloader import * #requerimos pasar esta parte al main

import math
#texturas-imagenes
import pygame
import OpenGL.GL as gl
# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Casa import Casa

from Cubo import Cubo
from Persona import Persona

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
'''EYE_X = 1.0   #300.0
EYE_Y = 2.0   #200.0
EYE_Z = 0.0   #300.0
CENTER_X = 0.0    #0
CENTER_Y = 2.0    #0
CENTER_Z = 0.0    #0'''
#pruebas
#EYE_X = 300.0
#EYE_Y = 200.0
#EYE_Z = 300.0
#CENTER_X = 0
#CENTER_Y = 0
#CENTER_Z = 0
#pruebas dentro del cubo
EYE_X = 100.0
EYE_Y = 49.0
EYE_Z = 100.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 300

#Variables para el control de las personas
personas = []
npersonas = 5


#Variables para el control del observador
theta = 1.0
radius = 300
dir = [1.0, 0.0, 0.0]

#Variables asociados a los objetos de la clase Cubo
#cubo = Cubo(DimBoard, 1.0)
cubos = []
ncubos = 20


pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    global obj
    #global texture_id1, texture_id2, texture_id3, texture_id4
    global texture_id1, texture_id2, texture_id3, texture_id4
    global casa
    global casa2
    
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    #Configuramos la iluminacion
    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
    
    #Texturas para las personas u objetos que se mueven en el plano 
    obj_files = ["Proyecto Emmitt2\Proyecto FInal\Texturas\CasaAmarilla.obj", "Proyecto Emmitt2\Proyecto FInal\Texturas\CasaVerde.obj"]
    #obj = OBJ("Archivos obj/obj/CasaAmarilla.obj", swapyz=True)
    #obj.generate()
    casa = Casa("Proyecto Emmitt2\Proyecto FInal\Texturas\CasaVerde.obj")
    casa.generate()
    casa2 = Casa("Proyecto Emmitt2\Proyecto FInal\Texturas\CasaAmarilla.obj")
    casa2.generate()
    
    
    for i in range(npersonas):
        obj_file = obj_files[i % len(obj_files)]
        persona = Persona(50, 1.0, obj_file)
        personas.append(persona)
    
    #for i in range(ncubos):
    #    cubos.append(Cubo(DimBoard, 1.0))
    
    

def load_texture(image_path):
    
    # Load image
    image = pygame.image.load(image_path)
    image = pygame.transform.flip(image, False, True)
    image_data = pygame.image.tostring(image, "RGB", 1)
    
    # Generate a texture id
    texture_id = glGenTextures(1)

    # Bind the texture
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Upload texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.get_width(), image.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    return texture_id

def drawFondo():
    textures = [load_texture(image_path) for image_path in ["Proyecto Emmitt2\Proyecto FInal\Texturas\FondoDesierto.bmp", "Proyecto Emmitt2\Proyecto FInal\Texturas\FondoDesierto.bmp", "Proyecto Emmitt2\Proyecto FInal\Texturas\FondoDesierto.bmp", "Proyecto Emmitt2\Proyecto FInal\Texturas\FondoDesierto.bmp"]]
   
    
    vertex_coords = [
        1, 1, 1,  1, 1, -1,  1, -1, -1,  1, -1, 1,
        -1, 1, 1,  -1, 1, -1,  -1, -1, -1,  -1, -1, 1
    ]
    '''vertex_colors = [ 
        1, 1, 1,  1, 0, 0,  1, 1, 0,  0, 1, 0,
        0, 0, 1,  1, 0, 1,  0, 0, 0,  0, 1, 1
    ]'''
    element_array = [ 
        0, 1, 2, 3,  0, 3, 7, 4,  0, 4, 5, 1,
        6, 2, 1, 5,  6, 5, 4, 7,  6, 7, 3, 2
    ]
    
    texture_coords = [
        0, 0,  1, 0,  1, 1,  0, 1,  # Cara 1
        0, 0,  1, 0,  1, 1,  0, 1,  # Cara 2
        0, 0,  1, 0,  1, 1,  0, 1,  # Cara 3
        0, 0,  1, 0,  1, 1,  0, 1,  # Cara 4
    ]
    #dibujamos el cubo
    glPushMatrix()
    glScalef(300.0, 50.0, 300.0)  
    # Trasladar el cubo
    glTranslatef(0.0, 0.9, 0.0)
    
    glEnable(GL_TEXTURE_2D)
    glEnableClientState(GL_VERTEX_ARRAY)
    #glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, vertex_coords)
    #glColorPointer(3, GL_FLOAT, 0, vertex_colors)
    glTexCoordPointer(2, GL_FLOAT, 0, texture_coords)
    
    for i in range(0, len(element_array), 4):  # Para cada cara
        glBindTexture(GL_TEXTURE_2D, textures[i % 4])  # Activar la textura
        glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, element_array[i:i+4])
    glDisable(GL_TEXTURE_2D)
    glDisableClientState(GL_VERTEX_ARRAY)
    #glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glPopMatrix()
    

#dibujamos el fondo
"""
def drawFondo():
    
    vertex_coords = [
        1, 1, 1,  1, 1, -1,  1, -1, -1,  1, -1, 1,
        -1, 1, 1,  -1, 1, -1,  -1, -1, -1,  -1, -1, 1
    ]
    vertex_colors = [ 
        1, 1, 1,  1, 0, 0,  1, 1, 0,  0, 1, 0,
        0, 0, 1,  1, 0, 1,  0, 0, 0,  0, 1, 1
    ]
    element_array = [ 
        0, 1, 2, 3,  0, 3, 7, 4,  0, 4, 5, 1,
        6, 2, 1, 5,  6, 5, 4, 7,  6, 7, 3, 2
    ]
    
    #dibujamos el cubo
    glPushMatrix()
    glScalef(300.0, 50.0, 300.0)  
    
    # Trasladar el cubo
    glTranslatef(0.0, 0.9, 0.0)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertex_coords)
    glColorPointer(3, GL_FLOAT, 0, vertex_colors)
    glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, element_array)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glPopMatrix()
"""
        
def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    
    
    #Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    #se dibuja el fondo
    drawFondo()
   
    #se dibujan la casa verde
    glPushMatrix()
    #glScalef(3.5, 3.5, 3.5)
    glScale(2,2,2)
    glTranslate(20, 0, 0)
    glRotate(-90, 1, 0, 0)
    glRotate(-90, 0, 0, 1)
    casa.draw()
    #obj.render()
    glPopMatrix()
    
    #se dibuja la casa amarilla
    glPushMatrix()
    glScale(2,2,2)
    glTranslate(-20, 0, 0)
    glRotate(-90, 1, 0, 0)
    glRotate(-90, 0, 0, 1)
    casa2.draw()
    #obj.render()
    glPopMatrix()
    
    #Se dibuja cubos
    glPushMatrix()
    #glScale(0.8,0.8,0.8)
    glTranslate(120.0, 0.0, 0.0)
    #glRotate(-90, 1, 0, 0)
    
    for obj in personas:
        obj.draw()
        obj.update()
    glPopMatrix()
    
    #for obj in cubos:
    #    obj.draw()
    #    obj.update()
    
    pygame.display.flip()
    #pygame.time.wait(100)
    
done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            #se controla el movimiento para adelante
            if event.key == pygame.K_UP:
                EYE_X = EYE_X + dir[0]
                EYE_Z = EYE_Z + dir[2]
                CENTER_X = CENTER_X + dir[0]
                CENTER_Z = CENTER_Z + dir[2]
                glLoadIdentity()
                gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
            #se controla el movimiento para atras
            if event.key == pygame.K_DOWN:
                EYE_X = EYE_X - dir[0]
                EYE_Z = EYE_Z - dir[2]
                CENTER_X = CENTER_X + dir[0]
                CENTER_Z = CENTER_Z + dir[2]
                glLoadIdentity()
                gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
            #se controla el movimieto de camara a la derecha
            if event.key == pygame.K_RIGHT:
                dir[0] = (math.cos(math.radians(-theta)) * dir[0]) + (math.sin(math.radians(-theta)) * dir[2])
                dir[2] = -(math.sin(math.radians(-theta)) * dir[0]) + (math.cos(math.radians(-theta)) * dir[2])
                #EYE_X = EYE_X + dir[0]
                #EYE_Z = EYE_Z + dir[2]
                CENTER_X = EYE_X + dir[0]
                CENTER_Z = EYE_Z + dir[2]
                glLoadIdentity()
                gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
            #se controla el movimieto de camara a la izquierda
            if event.key == pygame.K_LEFT:
                dir[0] = (math.cos(math.radians(theta)) * dir[0]) + (math.sin(math.radians(theta)) * dir[2])
                dir[2] = -(math.sin(math.radians(theta)) * dir[0]) + (math.cos(math.radians(theta)) * dir[2])
                #EYE_X = EYE_X - dir[0]
                #EYE_Z = EYE_Z - dir[2]
                CENTER_X = EYE_X + dir[0]
                CENTER_Z = EYE_Z + dir[2]
                glLoadIdentity()
                gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
            if event.key == pygame.K_ESCAPE:
                done = True
                
    #Colisiones entre las personas y su rebote en la dirección contraria
    parejas_persona = Persona.parejasPersonas(personas)
    Persona.colisionDetection(parejas_persona) 
    
    display()
   
    pygame.time.wait(30)

pygame.quit()