import cv2
from picamera2 import Picamera2
from libcamera import controls

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    im = picam2.capture_array()
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im=cv2.resize(grey,(640,480))
    cv2.imshow("Camera", im)
    key = cv2.waitKey(1)
    # Escキーを入力されたら画面を閉じる
    if key == 27:
        break

picam2.stop()
cv2.destroyAllWindows()
