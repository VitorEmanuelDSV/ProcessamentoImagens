from pyopengltk import OpenGLFrame
from OpenGL import GL
from OpenGL.GLU import gluOrtho2D
from openGL.open_gl_manager import OpenGLManager

class OpenGLScreen(OpenGLFrame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=int(width), height=int(height))
        self.manager = OpenGLManager(app_ref=self)
        self.manager.start_menu_thread()
        self.width = width
        self.height = height
        self.ready = False
        self.world_configured = False
        # self.start_render_loop()

    def initgl(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.ready = True

    def configure_world(self):
        """Configura a viewport e projeção (uma única vez)."""
        GL.glViewport(0, 0, self.width, self.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        gluOrtho2D(-self.width // 2, self.width // 2, -self.height // 2, self.height // 2)
        # gluOrtho2D(-256, 256, -256, 256)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def draw_axes(self):
        GL.glLineWidth(1)
        GL.glBegin(GL.GL_LINES)

        # Eixo X
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2f(-self.width // 2, 0.0)
        GL.glVertex2f(self.width // 2, 0.0)

        # Eixo Y
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2f(0.0, -self.height // 2)
        GL.glVertex2f(0.0, self.height // 2)

        GL.glEnd()

    def redraw(self):
        if not self.ready:
            return

        if not self.world_configured:
            self.configure_world()
            self.world_configured = True

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        # self.draw_axes()
        self.manager.draw()

        self.update_idletasks()
        self.update()
        self.tkSwapBuffers()

    def set_shape(self, shape_name):
        self.manager.set_shape(shape_name)

    def start_render_loop(self):
        self.redraw()
        self.after(16, self.start_render_loop)
