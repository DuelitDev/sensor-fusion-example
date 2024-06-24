from ursina import *
from src.filter import *
from src.util import *


sensor = Sensor()
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
ahrs = Madgwick2Filter(beta=1, zeta=0)

app = Ursina()
camera.orthographic = True
camera.fov = 10
camera.position = (0, 0, -10)
# Create entities & UI elements
model = Entity(model="model/plane", texture="model/plane.tga",
               scale=0.5, position=(0, 0, 0))


def update():
    ahrs.update(sensor.av, sensor.gv, sensor.mv)
    rad = 180 / math.pi
    v = ahrs.quaternion.euler_angles
    r, p, y = -v.x * rad, v.y * rad, v.z * rad
    model.rotation = p, y, r


app.run()
