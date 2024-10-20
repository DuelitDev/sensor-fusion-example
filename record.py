from ins.filter import *
from ins.sensor import *
from time import sleep, time


filter_ = FusionFilter(FusionFilterOptions())
sensor = UDPSensor(filter_=filter_, address="0.0.0.0", port=8888)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
sensor.set_invert(
    ax=True,  ay=True,  az=False,
    gx=False, gy=False, gz=True,
    mx=False, my=False, mz=False
)
sensor.set_calibrate(
    ax=0.0, ay=0.0, az=0.0,
    gx=0.0, gy=0.0, gz=0.0,
    mx=0.0, my=0.0, mz=0.0
)
# sensor = SerialSensor(filter_=filter_, port="COM3")
# sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
# sensor.set_invert(
#     ax=True,  ay=True,  az=False,
#     gx=False, gy=False, gz=True,
#     mx=False, my=False, mz=False
# )
# sensor.set_calibrate(
#     ax=0.0, ay=0.0, az=0.0,
#     gx=0.0, gy=0.0, gz=0.0,
#     mx=0.0, my=0.0, mz=0.0
# )


with open("sensor.csv", "w") as f:
    print("Recording...")
    f.write("time,ax,ay,az,gx,gy,gz,mx,my,mz\n")
    now = time()
    while True:
        f.write(f"{time() - now},"
                f"{sensor.ax},{sensor.ay},{sensor.az},"
                f"{sensor.gx},{sensor.gy},{sensor.gz},"
                f"{sensor.mx},{sensor.my},{sensor.mz}\n")
        sleep(0.001)

