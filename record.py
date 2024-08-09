from ins.filter import *
from ins.sensor import *
from time import sleep, time


filter_ = FusionFilter(FusionFilterOptions())
sensor = UDPSensor(filter_=filter_, address="0.0.0.0", port=8888)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
sensor.set_invert(ax=True, ay=True, gz=True)
sensor.set_calibrate(
    ax=0.003237, ay=-0.011006, az=0.005022,
    gx=-0.001501, gy=-0.005425, gz=0.001142,
    mx=2.099998, my=4.124998, mz=0.299999
)
# sensor = SerialSensor(filter_=filter_, port="/dev/cu.usbserial-0001")
# sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
# sensor.set_invert(ax=True, ay=True, gz=True)
# sensor.set_calibrate(
#     ax=-0.006249, ay=-0.019650, az=0.004745,
#     gx=0.001802, gy=0.930908, gz=-0.924316,
#     mx=-33.211478, my=30.362637, mz=0.000000
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

