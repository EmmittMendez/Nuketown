import pygame
#uso de teclado y raton
from pygame.locals import * 
from pygame.constants import *  

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# IMPORT OBJECT LOADER
from objloader import * #requerimos pasar esta parte al main

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Casa import Casa

from Cubo import Cubo
from Persona import Persona
from Vehiculo import Vehiculo
from Suelo import Suelo
from Letrero import Letrero 
from Valla import Valla

screen_width = 900
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
# ZFAR=1000.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

EYE_X = 1.0   #300.0
EYE_Y = 7.0   #200.0
EYE_Z = 0.0   #300.0
CENTER_X = 0.0    #0
CENTER_Y = 7.0    #0
CENTER_Z = 0.0    #0
#pruebas
#EYE_X = 300.0
#EYE_Y = 200.0
#EYE_Z = 300.0
#CENTER_X = 0
#CENTER_Y = 0
#CENTER_Z = 0
#pruebas dentro cubo 2

# EYE_X = 90.0
# EYE_Y = 49.0
# EYE_Z = 90.0
# CENTER_X = 0
# CENTER_Y = 0
# CENTER_Z = 0

#pruebas dentro del cubo
# EYE_X = 300.0
# EYE_Y = 90.0
# EYE_Z = 300.0
# CENTER_X = 0
# CENTER_Y = 0
# CENTER_Z = 0c:\Users\edgar\Desktop\Otoño 2023\Graficación\Archivos obj\Texturas Nuketown\Objetos Corregidos\Mas texturas\MapaNuketown2.py
'''
#pruebas dentro del cubo casa amarilla
EYE_X = 1.0
EYE_Y = 50.0
EYE_Z = 0.0
CENTER_X = 0
CENTER_Y = 50
CENTER_Z = 0
'''
#pruebas centro del mapa
'''
EYE_X = 100.0
EYE_Y = 49.0
EYE_Z = 100.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
'''

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
DimBoard = 400

#Variables para el control de las personas
personas = []
npersonas = 10


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
    #global obj
    global casa, casa2, bus, carro, suelo, suelo2, letrero, vallaC, vallaL1, vallaL2, vallaL3, vallaM1, vallaM2
    #screen = pygame.display.set_mode(
        #(screen_width, screen_height), DOUBLEBUF | OPENGL)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("OpenGL: Mapa Nuketown")

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    
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
    
    #obj_files = ["Archivos obj\obj\Chevrolet_Camaro_SS_Low.obj", "Archivos obj\obj\CasaVerde.obj", "Archivos obj\obj\CasaAmarilla.obj"]
    #obj = OBJ("Archivos obj/obj/CasaAmarilla.obj", swapyz=True)
    #obj.generate()
    
    # Texturas para el suelo
    suelo = Suelo("Proyecto FInal\Texturas\BaseSuelo.obj")
    suelo.generate()
    suelo2 = Suelo("Proyecto FInal\Texturas\Suelo.obj")
    suelo2.generate()
    # Texturas para las vallas
    # vallaC = Valla("Proyecto FInal\Texturas\VallaChica1.obj")
    # vallaC.generate()
    # vallaL1 = Valla("Proyecto FInal\Texturas\VallaLarga1.obj")
    # vallaL1.generate()
    # vallaL2 = Valla("Proyecto FInal\Texturas\VallaLarga2.obj")
    # vallaL2.generate()
    # vallaL3 = Valla("Proyecto FInal\Texturas\VallaLarga3.obj")
    # vallaL3.generate()
    # vallaM1 = Valla("Proyecto FInal\Texturas\VallaMediana1.obj")
    # vallaM1.generate()
    # vallaM2 = Valla("Proyecto FInal\Texturas\VallaMediana2.obj")
    # vallaM2.generate()
    
    # Arreglo de la direccion de las texturas de las personas
    #obj_files = ["Proyecto FInal\Texturas\HelloK.obj"]
    # Casa verde y amarilla
    casa = Casa("Proyecto FInal\Texturas\CasaVerde.obj")
    casa.generate()
    casa2 = Casa("Proyecto FInal\Texturas\CasaAmarilla.obj")
    casa2.generate()
    # Creamos el bus
    bus = Vehiculo("Proyecto FInal\Texturas\BusAmarillo.obj")
    bus.generate()
    carro = Vehiculo("Proyecto FInal\Texturas\Chevrolet_Camaro_SS_Low.obj")
    # Creamos el letrero
    letrero = Letrero("Proyecto FInal\Texturas\Letrero.obj")
    letrero.generate()
    
    # Asigamos las texturas a cada persona
    # for i in range(npersonas):
    #     obj_file = obj_files[i % len(obj_files)]
    #     persona = Persona(20, 1.0, obj_file)
    #     personas.append(persona)
        

#dibujamos el fondo  
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
    glScalef(400.0, 50.0, 400.0)  
    
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

        

    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    #Se dibuja el plano verde
    glColor3f(0.3, 1.0, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    #se dibuja el fondo
    drawFondo()
    
    #se dibuja el suelo
    glPushMatrix()
    glScale(8,8,8)
    glTranslate(1.5, 0, 0)
    glRotate(69, 0, 1, 0)
    glRotate(90, 1, 0, 0)
    suelo.draw()
    glPopMatrix()
    
    #se dibuja el suelo2
    glPushMatrix()
    glScale(8,8,8)
    glTranslate(0, 0.08, 0)
    # glRotate(75, 0, 1, 0) #cambio para ver orientacion del suelo
    glRotate(105, 0, 1, 0)
    glRotate(-90, 1, 0, 0)
    #glRotate(90, 1, 0, 0) #cambio para ver orientacion del suelo
    suelo2.draw()
    glPopMatrix()
    
    
    #se dibujan la casa verde
    glPushMatrix()
    #glScalef(3.5, 3.5, 3.5)
    #glTranslate(30, 0, 10)
    glScale(7,7,7)
    glTranslate(20, 0, 6.3)
    glRotate(-18, 0, 1, 0)
    glRotate(-90, 1, 0, 0 )
    glRotate(-90, 0, 0, 1)
    casa.draw()
    #obj.render()
    glPopMatrix()
    
    #se dibuja la casa amarilla
    glPushMatrix()
    glScale(7,7,8)
    glTranslate(-18, 0, 3.5)
    glRotate(18, 0, 1, 0)
    #glTranslate(-30, 0, -10)
    glRotate(-90, 1, 0, 0)
    glRotate(-90, 0, 0, 1)
    casa2.draw()
    #obj.render()
    glPopMatrix()
    
    # #se dibujan la casa verde2
    # glPushMatrix()
    # #glScalef(3.5, 3.5, 3.5)
    # #glTranslate(30, 0, 10)
    # glScale(7,7,7)
    # glTranslate(0, 0, 30)
    # glRotate(-90, 0, 1, 0)
    # glRotate(-90, 1, 0, 0 )
    # glRotate(-90, 0, 0, 1)
    # casa.draw()
    # #obj.render()
    # glPopMatrix()
    
    
    #Dibuja las personas
    glPushMatrix()
    #glScale(0.8,0.8,0.8)
    #glTranslate(120.0, 0.0, 0.0)
    glTranslate(0.0, -3.5, 0.0)
    glTranslate(-4, 0, 0)
    #glRotate(-90, 1, 0, 0)
    for obj in personas:
        obj.draw()
        obj.update()
    glPopMatrix()
   
    #Se dibuja el bus
    glPushMatrix()
    glScale(5,5,5)
    glTranslate(4, 1.4, -5)
    glRotate(-90, 1, 0, 0)
    bus.draw()
    glPopMatrix()
    
    #Se dibuja el bus2
    glPushMatrix()
    glScale(5,5,5)
    glTranslate(-8, 1.4, 2)
    glRotate(-90, 1, 0, 0)
    bus.draw()
    glPopMatrix()
    
    #se dibuja el carro
    glPushMatrix()
    glScale(3,3,3)
    glTranslate(3, 1.4,-30)
    glRotate(90, 0, 1, 0)
    glRotate(-90, 1, 0, 0)
    carro.draw()
    glPopMatrix()
    
    #se dibuja el carro casa verde
    glPushMatrix()
    glScale(3,3,3)
    glTranslate(27, 1.4, 26)
    glRotate(70, 0, 1, 0)
    glRotate(-90, 1, 0, 0)
    carro.draw()
    glPopMatrix()
    
    #Se dibuja el letrero
    glPushMatrix()
    glScale(1,1,1)
    glTranslate(80, 1.4, -20)
    glRotate(-90, 0, 1, 0)
    glRotate(-90, 1, 0, 0)
    letrero.draw()
    glPopMatrix()
    
    #Se dibujan las vallas
    # glPushMatrix()
    # glScale(14,14,14)
    # #glTranslate(12, 0, -5.5)
    # glTranslate(6.5, 0, -4.8)
    # glRotate(-21, 0, 1, 0)
    # glRotate(-90, 1, 0, 0)
    # vallaC.draw()
    # glPopMatrix()
    
    # glPushMatrix()
    # glScale(7, 14, 7)
    # #glTranslate(12, 0, -5.5)
    # glTranslate(15.8, 0, -10)
    # glRotate(65, 0, 1, 0)
    # glRotate(-90, 1, 0, 0)
    # vallaC.draw()
    # glPopMatrix()
    
    # #valla larga
    # glPushMatrix()
    # glScale(14, 14, 14)
    # #glTranslate(12, 0, -5.5)
    # glTranslate(13.8, 0.5, -4.6)
    # glRotate(-18, 0, 1, 0)
    # glRotate(-90, 1, 0, 0)
    # vallaM1.draw()
    # glPopMatrix()
    
    
    pygame.display.flip()
    #pygame.time.wait(100)
    
done = False
Init()

# Mouse CAM
last_mouse_pos = pygame.mouse.get_pos()
sensitivity = 0.1
phi = 0  # Define phi con un valor inicial

center_x = screen_width // 2
center_y = screen_height // 2
pygame.mouse.set_pos((center_x, center_y))

mouse_intentional = False

pygame.mouse.set_visible(False)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            # Obtener la posición actual del mouse
            current_pos = pygame.mouse.get_pos()

            # Si el mouse se ha movido desde el centro de la ventana intencionalmente
            if current_pos != (center_x, center_y):
                mouse_intentional = True
                delta_x = current_pos[0] - center_x
                delta_y = current_pos[1] - center_y

                theta += delta_x * sensitivity
                phi -= delta_y * sensitivity

                phi = max(min(phi, 89), -89)
                theta %= 360
                pygame.mouse.set_pos((center_x, center_y))
            else:
                mouse_intentional = False  # El movimiento del mouse fue debido a centrado, no intencional

        if not mouse_intentional:
            dir[0] = math.cos(math.radians(theta)) * math.cos(math.radians(phi))
            dir[1] = math.sin(math.radians(phi))
            dir[2] = math.sin(math.radians(theta)) * math.cos(math.radians(phi))

            CENTER_X = EYE_X + dir[0]
            CENTER_Y = EYE_Y + dir[1]
            CENTER_Z = EYE_Z + dir[2]

            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        if event.type == pygame.QUIT:
            done = True
        
        keys = pygame.key.get_pressed()
        #if event.type == pygame.KEYDOWN:
            #se controla el movimiento para adelante
        if keys[K_UP] or keys[K_w]:
            EYE_X = EYE_X + dir[0]
            EYE_Z = EYE_Z + dir[2]
            CENTER_X = CENTER_X + dir[0]
            CENTER_Z = CENTER_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        #se controla el movimiento para atras
        if keys[K_DOWN] or keys[K_s]:
            EYE_X = EYE_X - dir[0]
            EYE_Z = EYE_Z - dir[2]
            CENTER_X = CENTER_X + dir[0]
            CENTER_Z = CENTER_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        #se controla el movimieto de camara a la derecha
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dir[0] = (math.cos(math.radians(-theta)) * dir[0]) + (math.sin(math.radians(-theta)) * dir[2])
            dir[2] = -(math.sin(math.radians(-theta)) * dir[0]) + (math.cos(math.radians(-theta)) * dir[2])
            #EYE_X = EYE_X + dir[0]
            #EYE_Z = EYE_Z + dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        #se controla el movimieto de camara a la izquierda
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dir[0] = (math.cos(math.radians(theta)) * dir[0]) + (math.sin(math.radians(theta)) * dir[2])
            dir[2] = -(math.sin(math.radians(theta)) * dir[0]) + (math.cos(math.radians(theta)) * dir[2])
            #EYE_X = EYE_X - dir[0]
            #EYE_Z = EYE_Z - dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
        if keys[K_ESCAPE]:
            done = True
        # if event.key == pygame.K_ESCAPE:
        #    done = True
            # glLoadIdentity()
            # gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    # Generar las parejas de obj
    parejas_persona = Persona.parejasPersonas(personas)

    # Llamar a la función colisionDetection con las parejas
    Persona.colisionDetection(parejas_persona) 
    display()

pygame.quit()