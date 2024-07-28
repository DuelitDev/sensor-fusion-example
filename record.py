from time import sleep, time
from src.filter import *
from src.sensor import *


sensor = SerialSensor(
    filter_=FusionAHRS(
        FusionAHRSSettings(
            gain=0.0,
            gyr_range=0.0,
            acc_reject=0.0,
            mag_reject=0.0,
            recovery_period=0)),
    port="/dev/cu.usbserial-0001"
)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
sensor.set_invert(ax=True, ay=True, gz=True)
sensor.set_calibrate(
    ax=0.021067, ay=0.005876, az=-0.063086,
    gx=0.128189, gy=0.930908, gz=-0.924316,
    mx=-33.211478, my=30.362637, mz=0.000000)


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

