from math import degrees as deg
from ins.filter import *
from ins.sensor import *
from ursina import *


filter_ = FusionFilter(FusionFilterOptions())
sensor = UDPSensor(filter_=filter_, address="0.0.0.0", port=8888)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
sensor.set_invert(ax=True, ay=True, gz=True)
sensor.set_calibrate(
    ax=0.0, ay=0.0, az=0.0,
    gx=0.0, gy=0.0, gz=0.0,
    mx=0.0, my=0.0, mz=0.0
)
# sensor = SerialSensor(filter_=filter_, port="COM3")
# sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
# sensor.set_invert(ax=True, ay=True, gz=True)
# sensor.set_calibrate(
#     ax=0.0, ay=0.0, az=0.0,
#     gx=0.0, gy=0.0, gz=0.0,
#     mx=0.0, my=0.0, mz=0.0
# )


app = Ursina()
model = Entity(model="resources/plane.obj")


def update():
    v = sensor.euler_angles
    r, p, y = deg(v.x), deg(v.y), deg(v.z)
    model.rotation = p, -y, r


app.run()
