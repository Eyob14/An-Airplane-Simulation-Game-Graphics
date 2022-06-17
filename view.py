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
def initial():        
    pygame.init()
    width = 1000
    height = 500
    window = pygame.display.set_mode((width,height), OPENGL | DOUBLEBUF)

    # textfont = pygame.font.SysFont("Comic Sans MS", 30)

    # load here the 3d meshes
    plane_indices, plane_buffer = ObjLoader.load_model("meshes/plane_.obj")
    background_indices, background_buffer = ObjLoader.load_model("meshes/background.obj")
    eagle_indices, eagle_buffer = ObjLoader.load_model("meshes/Eagle.obj")

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # VAO and VBO
    global VAO, VBO
    VAO = glGenVertexArrays(3)
    VBO = glGenBuffers(3)

    # plane VAO
    vertex_Attribute(plane_buffer, 0)

    # background VAO
    vertex_Attribute(background_buffer, 1)

    # Eagle VAO
    vertex_Attribute(eagle_buffer, 2)


    textures = glGenTextures(3)
    load_texture("meshes/plane.JPG", textures[0])
    load_texture("meshes/sky.jpg", textures[1])
    load_texture("meshes/eagle.png", textures[2])


    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

        
    # Position of the models
    background_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-2, 0, -50]))

    # eye, target, up
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


    obstacle_positions = [
        pyrr.Vector3([10, random.randrange(-3, 0), -10]),
        pyrr.Vector3([100, random.randrange(0, 3), -10])
        # pyrr.Vector3([70, random.randrange(-3, 3), -10])
    ]

    plane_x_pos = -6
    plane_y_pos = -2
    plane_z_pos = -4

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(20)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                sys.exit()
            
        keys = pygame.key.get_pressed()  
        
        if keys[pygame.K_UP]:
            if plane_y_pos < 3.69999999:
                plane_y_pos += 0.3
        elif keys[pygame.K_DOWN]:
            if plane_y_pos > -3.79999999:
                plane_y_pos -= 0.3 
        elif keys[pygame.K_LEFT]:
            if plane_x_pos > -6.3:
                plane_x_pos -= 0.3
        elif keys[pygame.K_RIGHT]:
            if plane_x_pos < 6.2:
                plane_x_pos +=  0.3               
        for idx, obsPos in enumerate(obstacle_positions):
            x = obsPos.x - 4 * (dt / 1000)
            y = obsPos.y
            obstacle_positions[idx] = pyrr.Vector3([x, y, obsPos.z])
            result_y = abs(plane_y_pos - y)
            result_x = abs(int(x) - int(plane_x_pos))
            print("before: ", result_x, result_y, idx)
            if result_y < 0.6 and (result_x < 2):
                print("You lose")
                print("after: ", result_x, result_y, idx)
                running = False
                new_window()
                # sys.exit()
            if obstacle_positions[idx].x < -30:
                obstacle_positions[idx] = pyrr.Vector3([30, y, obsPos.z])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        plane_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([plane_x_pos, plane_y_pos, plane_z_pos]))
        model = pyrr.matrix44.multiply(1, plane_pos)

        # draw the plane character
        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(plane_indices))

        model = pyrr.matrix44.multiply(1, background_pos)

        # draw the background head
        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(background_indices))
        
        for idx, obsPos in enumerate(obstacle_positions):
            model = pyrr.matrix44.create_from_translation(obsPos)
            # draw the obstacle head
            glBindVertexArray(VAO[2])
            glBindTexture(GL_TEXTURE_2D, textures[2])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawArrays(GL_TRIANGLES, 0, len(eagle_indices))
            
        pygame.display.flip()
initial()