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
