from pydualsense import *

dualsense = pydualsense()

if dualsense is not None:
    dualsense.init()

if dualsense is not None:
    dualsense.light.setColorI(0, 255, 0)
    dualsense.light.setBrightness(Brightness.high)


def cl_ds():
    if dualsense is not None:
        dualsense.close()
