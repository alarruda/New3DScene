# 3D-Scene main.py
# Created by: Antonio Arruda
# Southern New Hampshire University

from OpenGL.GL import *
import glfw
import numpy as np
from utils import load_image


# Create function to generate window
def createwindow():
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Add title bar to window
    glfwwindow = glfw.create_window(800, 600, 'Antonio Arruda CS-499 3D-Scene', None, None)
    glfw.make_context_current(glfwwindow)
    return glfwwindow


window = createwindow()


# Define function to plot vertices, color coords, and texture coords.
def drawtriangle():
    coords = np.array([
        0.5, 0.5,
        -0.5, -0.5,
        0.5, -0.5,
        0.5, 0.5
    ], dtype=np.float32)

    colors = np.array([
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5
    ], dtype=np.float32)

    tex_coords = np.array([
        0.5, 0,
        0, 1,
        1, 1
    ], dtype=np.float32)

    size = np.dtype('float32').itemsize

    # Initialize Vertex Array Objects and bind VAO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Create and bind Vertex Buffer Array to Array Buffer
    vbo_id = glGenBuffers(3)

    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[0])
    glBufferData(GL_ARRAY_BUFFER, size * coords.size, coords, GL_STATIC_DRAW)

    # Get the vertex array locations
    coords_attrib_location = glGetAttribLocation(program, 'coords')

    # Tell the GPU how to interpret the data
    glVertexAttribPointer(coords_attrib_location, 2, GL_FLOAT, GL_FALSE, 0, None)

    # Link variable and buffer on GL_ARRAY_BUFFER
    glEnableVertexAttribArray(coords_attrib_location)

    # Link the variable and buffer to colors
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
    glBufferData(GL_ARRAY_BUFFER, size * colors.size, colors, GL_STATIC_DRAW)
    colors_attrib_location = glGetAttribLocation(program, 'colors')
    glVertexAttribPointer(colors_attrib_location, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(colors_attrib_location)

    # Link the variable and buffer to texture coords
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id[2])
    glBufferData(GL_ARRAY_BUFFER, size * tex_coords.size, tex_coords, GL_STATIC_DRAW)
    tex_coords_attrib_location = glGetAttribLocation(program, 'a_tex_coords')
    glVertexAttribPointer(tex_coords_attrib_location, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(tex_coords_attrib_location)


# Define function to load texture
def loadtextures():
    texture_data, width, height = load_image('/home/parallels/PycharmProjects/3D-Scene/resources/carpet.png')

    print(texture_data, width, height)

    gentexture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, gentexture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    texturelocation = glGetUniformLocation(program, 'octo_texture')

    return gentexture, texturelocation


# Create function to load the shader programs
def loadshaders():
    with open('./shaders/vertex.glsl') as vertex_shader:
        vertex_src = vertex_shader.read()
    with open('./shaders/frag.glsl') as frag_shader:
        frag_src = frag_shader.read()

    vert_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vert_shader, vertex_src)
    glCompileShader(vert_shader)

    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(frag_shader, frag_src)
    glCompileShader(frag_shader)

    print(glGetShaderInfoLog(vert_shader))
    print(glGetShaderInfoLog(frag_shader))

    createprogram = glCreateProgram()

    glAttachShader(createprogram, vert_shader)
    glAttachShader(createprogram, frag_shader)

    glLinkProgram(createprogram)

    return createprogram


# Create function to handle textures and use shader program
def texturehandler():
    glUniform1i(texturelocation2, 0)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)


program = loadshaders()
drawtriangle()

glUseProgram(program)
texture, texturelocation2 = loadtextures()


# Create function to draw the triangles to create the object and initialize texture handler
def drawobject():
    glClear(GL_COLOR_BUFFER_BIT)

    texturehandler()

    glDrawArrays(GL_TRIANGLES, 0, 3)


# Define the main loop that will keep the window and program alive until the user exits
def main():
    while not glfw.window_should_close(window):
        drawobject()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


main()
