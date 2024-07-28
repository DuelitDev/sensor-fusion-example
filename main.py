from ursina import *
from src.filter import *
from src.sensor import *
from math import degrees as deg

MODEL = "resources/plane.obj"


sensor = SerialSensor(
    filter_=FusionFilter(
        FusionFilterOptions(
            gain=0.5,
            initial_gain=10.0,
            initial_period=3.0,
            acc_rejection=10.0,
            gyr_range=500.0,
            mag_rejection=10.0,
            recovery_period=600)),
    port="/dev/cu.usbserial-0001"
)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
sensor.set_invert(ax=True, ay=True, gz=True)
sensor.set_calibrate(
    ax=0.021067, ay=0.005876, az=-0.063086,
    gx=0.128189, gy=0.930908, gz=-0.924316,
    mx=-32.236874, my=25.489622, mz=3.673504)


app = Ursina()
model = Entity(model=MODEL, scale=(-0.5, -0.5, 0.5), noCache=True)


def update():
    v = sensor.euler_angles
    r, p, y = deg(v.x), deg(v.y), deg(v.z)
    model.rotation = p, -y, r


app.run()
