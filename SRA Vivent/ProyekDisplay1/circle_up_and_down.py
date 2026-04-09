print("Loading libraries")
from pynq.overlays.base import BaseOverlay
print("BaseOverlay Library uploaded")
from pynq.lib.video import *
print("pynq.lib.video Library uploaded")
import numpy as np
print("numpy Library uploaded")
import cv2 as cv
print("cv2 Library uploaded")
import matplotlib.pyplot as plt
print("matplotlib.pyplot Library uploaded")
from time import sleep 
print("sleep Library uploaded")
#
print("Loading libraries completed.")
#
import cv2
base = BaseOverlay("base.bit")
####
# 640x480, 800x600, 1280x720, 1280x1024, 1920x1080
# 
#
frame_in_w = 1920 #1280
frame_in_h = 1080 #1024
Mode = VideoMode(frame_in_w,frame_in_h,24,fps=60)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(Mode,PIXEL_BGR)
hdmi_out.start()
#
imgblank = np.zeros((frame_in_h,frame_in_w,3), np.uint8)
outframeblank = hdmi_out.newframe()
outframeblank[:] = imgblank
#
img = np.zeros((frame_in_h,frame_in_w,3), np.uint8)
#
# Draw a diagonal blue line with thickness of 5 px
cv.line(img,(0,0),(frame_in_w,frame_in_h),(255,0,0),5)
# Create a circle
cv.circle(img,(0,0), 63, (0,0,255), -1)
# Write some text on the screen
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'Calvin Institute of Technology',(10,500), font, 1,(255,255,255),2,cv.LINE_AA)
# Output image
outframe = hdmi_out.newframe()
outframe[:] = img
hdmi_out.writeframe(outframe)
#
print("Drawing initial position (wait until the shapes appear)")
pauseawhile = input("and ready to animate. Press ENTER to continue...")

delta=0.5625 # round(frame_in_h/frame_in_w)
outframe = hdmi_out.newframe()

for n in range(0,32,2):
    xstep=10*(n+1)
    for i in range(0,frame_in_w,xstep):      
        #
        img = np.zeros((frame_in_h,frame_in_w,3), np.uint8)
        cv.line(img,(0,0),(frame_in_w,frame_in_h),(255,0,0),5)
        cv.circle(img,(i,round(i*delta)), 63, (0,0,255), -1)
        cv.putText(img,'Calvin Institute of Technology',(10,500), font, 1,(255,255,255),2,cv.LINE_AA)
        # Output image
        outframe[:] = img
        
#         hdmi_out.writeframe(outframeblank)
        hdmi_out.writeframe(outframe)
        
    xstep=-xstep
    for i in range(frame_in_w,0,xstep):
        #
        img = np.zeros((frame_in_h,frame_in_w,3), np.uint8)
        cv.line(img,(0,0),(frame_in_w,frame_in_h),(255,0,0),5)
        cv.circle(img,(i,round(i*delta)), 63, (0,0,255), -1)
        cv.putText(img,'Calvin Institute of Technology',(10,500), font, 1,(255,255,255),2,cv.LINE_AA)
        # Output image
        outframe[:] = img
    
#         hdmi_out.writeframe(outframeblank)
        hdmi_out.writeframe(outframe)
#     sleep(1/1000)  # sleep(1/100000)
    
pauseawhile = input("Press ENTER to stop...")

print("program completed.")

hdmi_out.close()

cv2.imshow("Ventilator GUI V2", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
