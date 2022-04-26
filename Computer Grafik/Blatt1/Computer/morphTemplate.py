"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke
 *             @version:   0.9
 *                @date:   16.04.2021
 ******************************************************************************/
/**         RenderWindow.py
 *
 *          Simple Python OpenGL program that uses PyOpenGL + GLFW to get an
 *          OpenGL 3.2 context and display some 2D scene.
 ****
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


class Scene:
    """ 
        OpenGL 2D scene class 
    """
    # initialization
    def __init__(self, width, height, 
                polygon_A=np.array([0, 0]), polygon_B=np.array([0, 0]),   
                scenetitle="2D Scene"):
        # time
        self.X =0
        self.Y =1
        self.t = 0
        self.dt = 0.01
        self.scenetitle = scenetitle
        self.pointsize = 7
        self.linewidth = 3
        self.width = width
        self.height = height
        self.polygon_A = polygon_A
        self.polygon_B = polygon_B
        self.rendered_polygon = polygon_A
        self.m = []
        self.b = []
        self.d =[]
        self.forward_animation = False
        self.backward_animation = False


    # set scene dependent OpenGL states
    def setOpenGLStates(self):
        glPointSize(self.pointsize)
        glLineWidth(self.linewidth)
    def setInterpolationValues(self):
        i=0;
        for point in self.polygon_A:
            self.m.append(point[self.Y])
            self.b.append((self.polygon_B[i][self.Y]-point[self.Y])/((self.polygon_B[i][self.X]-point[self.X])))
            x1 = point[self.X]
            x2 =self.polygon_B[i][self.X];
            if  x1 < x2:
                if x1 < 0 and x2 < 0:
                    length = -(x1-x2)
                elif x2>0 and x1< 0:
                    length = x2 +(-x1) 
                else:
                    length = x2-x1       
            else:
                if x1 < 0 and x2 < 0:
                    length = -(x1-x2)
                elif x2<0 and x1> 0:
                    length = x2-x1 
                else:
                    length = x2-x1  
                    
            self.d.append(length)
            i += 1
        print ()
        

    # step
    def step(self):
        # TODO 4:
        # - interpolate: 
        if self.forward_animation | self.backward_animation:
            to_rendered_polygon = []
            i = 0;
            for point in self.rendered_polygon:
                x = self.polygon_A[i][self.X]+(self.t * self.d[i])
                x1 =self.polygon_A[i][self.X]
                to_rendered_polygon.append([x,self.m[i]+(self.b[i] * (x- x1))])
                i += 1
            self.rendered_polygon = to_rendered_polygon
        

    # animation
    def animation(self):
        if self.forward_animation: 
            self.t += self.dt
            if self.t>=1:
                self.t = 1
                self.forward_animation = False
        
        if self.backward_animation: 
            self.t -= self.dt
            if self.t<=0:
                self.t = 0
                self.backward_animation = False
        
        self.step()


    # render 
    def render(self):
        # set color to blue
        glColor(0.0, 0.0, 1.0)

        self.animation()

        # render points
        glBegin(GL_POINTS)
        for p in self.rendered_polygon:
            glVertex2fv(p)
        glEnd()

        # render polygon
        glBegin(GL_LINE_LOOP)
        for p in self.rendered_polygon:
            glVertex2fv(p)
        glEnd()
        

    # set polygon A
    def set_polygon_A(self, polygon):
        self.polygon_A = np.copy(polygon)
        


    # set polygon B
    def set_polygon_B(self, polygon):
        self.polygon_B = np.copy(polygon)



class RenderWindow:
    """ 
        GLFW Rendering window class
        YOU SHOULD NOT EDIT THIS CLASS!
    """
    def __init__(self, scene):
        
        # save current working directory
        cwd = os.getcwd()
        
        # Initialize the library
        if not glfw.init():
            return
        
        # restore cwd
        os.chdir(cwd)
        
        # version hints
        #glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        #glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        #glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = scene.width, scene.height
        self.aspect = self.width/float(self.height)
        self.window = glfw.create_window(self.width, self.height, scene.scenetitle, None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)
    
        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glOrtho(-self.width/2,self.width/2,-self.height/2,self.height/2,-2,2)
        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)
        
        # create scene
        self.scene = scene #Scene(self.width, self.height)
        self.scene.setOpenGLStates()
        
        # exit flag
        self.exitNow = False

        # animation flags
        self.forward_animation = False
        self.backward_animation = False

        
    def onMouseButton(self, win, button, action, mods):
        print("mouse button: ", win, button, action, mods)
    

    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            if key == glfw.KEY_F:
                # Forward animation
                self.scene.forward_animation = True
                print("Forward")
            if key == glfw.KEY_B:
                # Backward animation
                self.scene.backward_animation = True


    def onSize(self, win, width, height):
        print("onsize: ", win, width, height)
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)
    

    def run(self):
        # initializer timer
        self.scene.setInterpolationValues()
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            currT = glfw.get_time()
            if currT - t > 1.0/self.frame_rate:
                # update time
                t = currT
                # clear viewport
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                # render scene
                self.scene.render()
                # swap front and back buffer
                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()
   
        
            


def readPolygon(filename,polygon):
    polygon_Data = open(filename,'r')
    for point in polygon_Data:
        polygon.append(np.fromstring(np.fromstring(point,dtype=float, sep= ' ')))
    return polygon

def makeEqual(polygon, pointToAdd, length):
    while pointToAdd != 0:
        polygon.append(polygon[length-1])
        pointToAdd -= 1
    
    return polygon

def toGolbal(width, height, polygon):
    polygon_global=[]
    for point in polygon:
        polygon_global.append([width*(point[0]-0.5),-height* (0.5-point[1])])
        
    return polygon_global
# main
if __name__ == '__main__':
    if len(sys.argv) != 3:
       print("morph.py firstPolygon secondPolygon")
       print("pressing 'F' should start animation morphing from first polygon to second")
       print("pressing 'B' should start animation morphing from second polygon back to first")
       #sys.exit(-1)

    # set size of render viewport
    width, height = 640, 480

    # TODO 1:
    # - read in polygons
    #np.array([-width/2.5, 0])
    polygon_A = []
    polygon_B = []
    polygon_A = readPolygon("Computer/data/polygonG.dat", polygon_A)
    polygon_B = readPolygon("Computer/data/polygonZ.dat", polygon_B)
        
    
    # TODO 2:
    length_A =len(polygon_A)
    length_B =len(polygon_B)
    if length_A > length_B:
        polygon_B=  makeEqual(polygon_B, length_A - length_B, length_B)
     
    elif length_A < length_B:
        polygon_A=makeEqual(polygon_A, length_B - length_A,length_A)
             
         
    # TODO 3:
    # - transform from local into global coordinate system 
    polygon_A = toGolbal(width,height,polygon_A)
    polygon_B = toGolbal(width, height, polygon_B)

    # instantiate a scene
    scene = Scene(width, height, polygon_A, polygon_B, "Morphing Template")

    # pass the scene to a render window
    rw = RenderWindow(scene)
    rw.run()

