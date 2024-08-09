from time import sleep
from ins.filter import *
from ins.sensor import *


filter_ = FusionFilter(FusionFilterOptions())
sensor = UDPSensor(filter_=filter_, address="0.0.0.0", port=8888)
sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.YXZ)
sensor.set_invert(ax=True, ay=True, gz=True)
# sensor = SerialSensor(filter_=filter_, port="/dev/cu.usbserial-0001")
# sensor.set_order(a=Order.YXZ, g=Order.YXZ, m=Order.XYZ)
# sensor.set_invert(ax=True, ay=True, gz=True)


SAMPLE = 1000
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
print(f"ax={cax:.6f}, ay={cay:.6f}, az={caz:.6f}")
print(f"gx={cgx:.6f}, gy={cgy:.6f}, gz={cgz:.6f}")
print(f"mx={cmx:.6f}, my={cmy:.6f}, mz={cmz:.6f}")
