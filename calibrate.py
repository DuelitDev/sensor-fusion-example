from time import sleep
from src.filter import *
from src.sensor import *


# MPU2950
SAMPLE = 1000


sensor = SerialSensor(
    filter_=FusionFilter(
        FusionFilterOptions(
            gain=0.0,
            initial_gain=0.0,
            initial_period=0.0,
            gyr_range=0.0,
            acc_rejection=0.0,
            mag_rejection=0.0,
            recovery_period=0)),
    port="/dev/cu.usbserial-0001"
)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
sensor.set_invert(ax=True, ay=True)
avl, gvl, mvl = [], [], []


sleep(3)
print("Starting accelerometer & gyroscope calibration...")
print("Don't move the device!")
for _ in range(SAMPLE):
    avl.append(sensor.av)
    gvl.append(sensor.gv)
    sleep(0.005)
print("Accelerometer & Gyroscope calibration complete.")


sleep(3)
print("Starting magnetometer calibration...")
print("Rotate the device around the Yaw axis.")
for _ in range(SAMPLE * 3):
    mvl.append(sensor.mv)
    sleep(0.005)
print("Magnetometer calibration complete.")


cax = -sum(map(lambda v: v.x, avl)) / SAMPLE
cay = -sum(map(lambda v: v.y, avl)) / SAMPLE
caz = -sum(map(lambda v: v.z - 1, avl)) / SAMPLE
cgx = -sum(map(lambda v: v.x, gvl)) / SAMPLE
cgy = -sum(map(lambda v: v.y, gvl)) / SAMPLE
cgz = -sum(map(lambda v: v.z, gvl)) / SAMPLE
cmx = -(max(map(lambda v: v.x, mvl)) + min(map(lambda v: v.x, mvl))) / 2
cmy = -(max(map(lambda v: v.y, mvl)) + min(map(lambda v: v.y, mvl))) / 2
cmz = -(max(map(lambda v: v.z, mvl)) + min(map(lambda v: v.z, mvl))) / 2


print("Calibration values:")
print(f"AX: {cax:12.6f}")
print(f"AY: {cay:12.6f}")
print(f"AZ: {caz:12.6f}")
print(f"GX: {cgx:12.6f}")
print(f"GY: {cgy:12.6f}")
print(f"GZ: {cgz:12.6f}")
print(f"MX: {cmx:12.6f}")
print(f"MY: {cmy:12.6f}")
print(f"MZ: {cmz:12.6f}")
