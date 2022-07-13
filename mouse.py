# mouse.py
# How to use the mouse events
# 6.22.22 

import cv2


# list all events
events = [i for i in dir(cv2) if 'EVENT' in i]
for e in events:
    print(e)
# Results:
# EVENT_FLAG_ALTKEY
# EVENT_FLAG_CTRLKEY
# EVENT_FLAG_LBUTTON
# EVENT_FLAG_MBUTTON
# EVENT_FLAG_RBUTTON
# EVENT_FLAG_SHIFTKEY
# EVENT_LBUTTONDBLCLK
# EVENT_LBUTTONDOWN
# EVENT_LBUTTONUP
# EVENT_MBUTTONDBLCLK
# EVENT_MBUTTONDOWN
# EVENT_MBUTTONUP
# EVENT_MOUSEHWHEEL
# EVENT_MOUSEMOVE
# EVENT_MOUSEWHEEL
# EVENT_RBUTTONDBLCLK
# EVENT_RBUTTONDOWN
# EVENT_RBUTTONUP


lastx = 0
lasty = 0


# callback function
def drawCircle(event, x, y, flags, param):
    global lasty
    global lastx
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 10, (255, 20, 55), 10)
        if lastx != 0 or lasty !=0:
            cv2.line(img, (lastx, lasty), (x, y), (0,0,250), 2, cv2.LINE_AA)
        lastx = x
        lasty = y


# load image
img = cv2.imread('../_images/scene1.jpg', cv2.IMREAD_COLOR)
# create window
window_name = 'My Window'

# create a window
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
# bind mouse event to window
cv2.setMouseCallback(window_name, drawCircle)


while True:
    cv2.imshow(window_name, img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
