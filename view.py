import random
import pygame, sys
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from shaders import vertex_src, fragment_src

def vertex_Attribute(buffer_name, index):
    global VAO
    glBindVertexArray(VAO[index])
    # plane Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[index])
    glBufferData(GL_ARRAY_BUFFER, buffer_name.nbytes, buffer_name, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer_name.itemsize * 8, ctypes.c_void_p(0))
    # plane textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer_name.itemsize * 8, ctypes.c_void_p(12))
    # plane normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer_name.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

def new_window():
    background_colour = (50,150,225)
    (width, height) = (500, 500)
    screen = pygame.display.set_mode((width, height))
    textfont = pygame.font.SysFont("monospace", 70)
    textfonttwo = pygame.font.SysFont("monospace", 25)

    pygame.display.set_caption('Game Detail')
    screen.fill(background_colour)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        textTBD = textfont.render("GAME OVER!", True, (0, 0, 0))
        textTwo = textfonttwo.render("press enter to restart the game", True, (0, 0, 0))
        
        
        screen.blit(textTBD, (55, 200))
        screen.blit(textTwo, (20, 300))
        
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_RETURN]:
            running = False
            initial()
        pygame.display.update()
VAO, VBO = None, None        
