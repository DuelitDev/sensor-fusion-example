from ursina import *
from src.filter import *
from src.util import *


sensor = Sensor()
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
ahrs = Madgwick2Filter(beta=4, zeta=1)

app = Ursina()
camera.orthographic = True
camera.fov = 10
camera.position = (0, 0, -10)
# Create entities & UI elements
model = Entity(model="model/plane", texture="model/plane.tga",
               scale=0.5, position=(0, 0, 0))
xyz = Text(text="", scale=0.05)
i = 0


def update():
    global i
    ahrs.update(sensor.av, sensor.gv, sensor.mv)
    rad = 180 / math.pi
    v = ahrs.quaternion.euler_angles
    r, p, y = -v.x * rad, v.y * rad, v.z * rad
    model.rotation = p, y, r
    if i > 20:
        tr, tp, ty = r, -p, y if y > 0 else y + 360
        fac = "East" if 45 <= ty < 135 else "South" if 135 <= ty < 225 else \
              "West" if 225 <= ty < 315 else "North"
        xyz.text = (f"\n\n\n"
                    f"\t\tTemp: {sensor.temperature:.2f}\n"
                    f"\t\tPre: {sensor.pressure:.2f}\n"
                    f"\t\tFac: {fac}\n"
                    f"\t\tR: {tr:.2f}\n"
                    f"\t\tP: {tp:.2f}\n"
                    f"\t\tY: {ty:.2f}")
        i = 0
    i += 1


app.run()
