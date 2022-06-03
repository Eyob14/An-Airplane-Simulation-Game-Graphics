#!/usr/bin/python3
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

P0 = [1, -1, -1]

V1 = [2, 0 ,0]
V2 = [0, 2, 0]
V3 = [0, 0, 2]



P = np.add(P0, np.multiply(t, V1))

vertices = (
(1, -1, -1),
(1, 1, -1),
(-1, 1, -1),
(-1, -1, -1),
(1, -1, 1),
(1, 1, 1),
(-1, -1, 1),
(-1, 1, 1)
)



edges = (
(0,1),
(0,3),
(0,4),
(2,1),
(2,3),
(2,7),
(6,3),
(6,4),
(6,7),
(5,1),
(5,4),
(5,7)
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(Verticies[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glRotatef(1, 1, 3, 1)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
main()
        