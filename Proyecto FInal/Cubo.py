import pygame
from pygame.locals import *
from objloader import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

class Cubo:
    
    def __init__(self, dim, vel, texture_file):
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        #Se inicializa los colores de los vertices del cubo
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1  ]
        #Se inicializa el arreglo para la indexacion de los vertices
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]

        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
        self.texture_obj = OBJ(texture_file)
        

    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]
        
        if(abs(new_x) <= self.DimBoard):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        
        if(abs(new_z) <= self.DimBoard):
            self.Position[2] = new_z
        else:
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        self.texture_obj.render()
        glPopMatrix()
    
