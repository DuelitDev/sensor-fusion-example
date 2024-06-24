from ursina import *
from src.filter import *
from src.util import *


sensor = Sensor()
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
ahrs1 = MadgwickFilter(beta=4, zeta=1)
ahrs2 = Madgwick2Filter(beta=4, zeta=1)

app = Ursina()
camera.orthographic = True
camera.fov = 10
camera.position = (0, 0, -10)
# Create entities & UI elements
model1 = Entity(model="model/plane", texture="model/plane.tga",
                scale=0.3, position=(-4, 0, 0))
model2 = Entity(model="model/plane", texture="model/plane.tga",
                scale=0.3, position=(4, 0, 0))
xyz1 = Text(text="", scale=0.03)
xyz2 = Text(text="", scale=0.03)
i = 0


def update():
    global i
    ahrs1.update(sensor.av, sensor.gv, sensor.mv)
    ahrs2.update(sensor.av, sensor.gv, sensor.mv)
    rad = 180 / math.pi
    v1 = ahrs1.quaternion.euler_angles
    r1, p1, y1 = -v1.x * rad, v1.y * rad, v1.z * rad
    model1.rotation = p1, y1, r1
    v2 = ahrs2.quaternion.euler_angles
    r2, p2, y2 = -v2.x * rad, v2.y * rad, v2.z * rad
    model2.rotation = p2, y2, r2
    if i > 20:
        tr1, tp1, ty1 = r1, -p1, y1 if y1 > 0 else y1 + 360
        fac1 = "East" if 45 <= ty1 < 135 else "South" if 135 <= ty1 < 225 else \
               "West" if 225 <= ty1 < 315 else "North"
        xyz1.text = (f"\n\n\nMadgwick1\n"
                     f"Temp: {sensor.temperature:.2f}\n"
                     f"Pre: {sensor.pressure:.2f}\n"
                     f"Fac: {fac1}\n"
                     f"R: {tr1:.2f}\n"
                     f"P: {tp1:.2f}\n"
                     f"Y: {ty1:.2f}")
        tr2, tp2, ty2 = r2, -p2, y2 if y2 > 0 else y2 + 360
        fac2 = "East" if 45 <= ty2 < 135 else "South" if 135 <= ty2 < 225 else \
            "West" if 225 <= ty2 < 315 else "North"
        xyz2.text = (f"\n\n\n\t\t\t\t\tMadgwick2\n"
                     f"\t\t\t\t\tTemp: {sensor.temperature:.2f}\n"
                     f"\t\t\t\t\tPre: {sensor.pressure:.2f}\n"
                     f"\t\t\t\t\tFac: {fac2}\n"
                     f"\t\t\t\t\tR: {tr2:.2f}\n"
                     f"\t\t\t\t\tP: {tp2:.2f}\n"
                     f"\t\t\t\t\tY: {ty2:.2f}")
        i = 0
    i += 1


app.run()
