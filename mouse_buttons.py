# mouse_buttons
# left, right click mouse buttons
# process selected area on video feed
# 7/12/22

import cv2

x_init = -1
y_init = -1


def draw_rectangle(event, x, y, flags, params):
    global x_init, y_init, drawing, top_left_pt, bottom_right_pt

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            top_left_pt = (min(x_init, x), min(y_init, y))
            bottom_right_pt = (max(x_init, x), max(y_init, y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        top_left_pt = (min(x_init, x), min(y_init, y))
        bottom_right_pt = (max(x_init, x), max(y_init, y))


def process_rectangle(top_left, bottom_right):
    global img
    (x0, y0), (x1, y1) = top_left, bottom_right
    image_roi = img[y0:y1, x0:x1]

    # blur effect
    if image_roi.any():
        image_roi = cv2.medianBlur(image_roi, 33)
        img[y0:y1, x0:x1] = image_roi

    # cartoonize
    if image_roi.any():
        image_original = image_roi.copy()
        img_gray = cv2.cvtColor(image_roi, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, 1)  # blur
        edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=7)
        ret, mask = cv2.threshold(edges, 20, 255, cv2.THRESH_BINARY_INV)  # mask is the cartoon
        image_roi = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # image_roi = cv2.bitwise_and(image_original, image_roi)
        img[y0:y1, x0:x1] = image_roi


    # negative film effect
    # img[y0:y1, x0:x1] = 255 - img[y0:y1, x0:x1]


if __name__ == '__main__':
    drawing = False
    top_left_pt, bottom_right_pt = [-1, -1], [-1, -1]

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cv2.namedWindow('Webcam')
    cv2.setMouseCallback('Webcam', draw_rectangle)

    while True:
        ret, frame = cap.read()
        img = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # img = frame

        # (x0, y0), (x1, y1) = top_left_pt, bottom_right_pt
        # img[y0:y1, x0:x1] = 255 - img[y0:y1, x0:x1]
        process_rectangle(top_left_pt, bottom_right_pt)

        cv2.imshow('Webcam', img)
        c = cv2.waitKey(1)
        if c == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
