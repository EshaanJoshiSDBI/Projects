import cv2
import numpy as np
import pyautogui
import time

resolution = (1920,1080)
x = time.time()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('vid%s.avi'%(x),fourcc,20.0,(resolution))
fps = 60
prev = 0
while True:
    time_elapsed = time.time() - prev
    img = pyautogui.screenshot()
    if time_elapsed > 1.0/fps:
        prev = time.time()
        frame = np.array(img)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        out.write(frame)
    cv2.waitKey(40)
cv2.destroyAllWindows()
cv2.release()
