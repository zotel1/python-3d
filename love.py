import matplotlib.pyplot as plt
import numpy as np 
from PIL import Image
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
from IPython.display import HTML

### Definimos la funcion que genera la superficie del corazón

def corazon_3d(x,y,z):
    a = (x**2 + (9/4) * (y**2) + z**2 - 1) **3
    b = x**2 * z**3
    c = (9/80) * (y**2) * (z**3)
    return a - b - c

# Creamos la figura y el eje en 3D

bbox = (-1.5, 1.5)
xmin, xmax, ymin, ymax, zmin, zmax = bbox * 3

fig = plt.figure(figsize=(18, 18))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(xmin, xmax)
ax.set_ylim3d(ymin, ymax)
ax.set_zlim3d(zmin, zmax)
ax.set_facecolor('black')
plt.axis('off')

# Iniciamos la superficie del corazon

M = np.linspace(xmin, xmax, 100)
N = np.linspace(xmin, xmax, 50)
M1, M2 = np.meshgrid(M, M)

for z in N:
    X, Y = M1, M2
    Z = corazon_3d(X, Y, z)
    if np.any((Z + z) > ax.get_zlim()[0]) and np.any((Z + z) < ax.get_zlim()[1]):
        cset = ax.contour(X, Y, Z+z,[z], zdir='z',
                      colors= ('red'), linewidths=0.2)

for y in N:
    X, Z = M1, M2
    Y = corazon_3d(X, y, Z)
    if np.any((Y + y) > ax.get_ylim()[0]) and np.any((Y + y) < ax.get_ylim()[1]):
        cset = ax.contour(X, Y+y, Z, [y], zdir='y',
                      colors= ('red'), linewidths=0.2)

for x in N:
    Y, Z = M1, M2
    X = corazon_3d(x, Y, Z)
    if np.any((X + x) > ax.get_xlim()[0]) and np.any((X + x) < ax.get_xlim()[1]):
        cset = ax.contour(X+x, Y, Z, [x], zdir='x',
                       colors= ('red'), linewidths=0.2)

# Obtener la imagen
img = Image.open('imgs/marti.jpeg')
img = np.array(img.convert("RGBA"))

#Escalar la imagen para que se ajuste al rango de los ejes

x = np.linspace(-0.75, 0.75, img.shape[1])
y = np.linspace(-1, 1, img.shape[0])
X1, Y1 = np.meshgrid(x, y)

# Obtener la extension del corazón

R, G, B, A = img [:, :,0], img[:,:,1], img[:,:,2], img[:,:,3]

# Normalizamos los canales RGB para que esten entre  [0,1]

R_n, G_n, B_n, A_n = R/255.0, G/255.0, B/255.0, A/255.0

# Aplicar la máscara a los canales RGBA de la imagen
mask = corazon_3d(X1, 0, -Y1) < 0
R_n[~mask], G_n[~mask], B_n[~mask], A_n[~mask] = 0, 0, 0, 0

# Graficar la imagen como una superficie en el plano z
ax.plot_surface(X1, np.zeros_like(X1), -Y1, facecolors=np.dstack((R_n,G_n,B_n,A_n)), rstride=1, cstride=1 )

# Definir la función de animacion
def animate(i):
    if i <= 180:
        elev = 10 + 0.1*i
    else:
        elev = 28 - 0.1*(i - 180)
    ax.view_init(elev= elev, azim=i)
    return fig,

# Creamos la animación
anim = animation.FuncAnimation(fig, animate, frames=360, interval=25, blit= True)

# Guardamos la animación

writer = FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
anim.save('3D_marti.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

# Mostramos la animación

HTML(anim.to_html5_video())