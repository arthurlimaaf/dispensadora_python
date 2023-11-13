import cv2
from time import sleep
from pylibdmtx import pylibdmtx

indexCAM = 1
lastBarCode = b''

def initCamera():
  cap = cv2.VideoCapture(indexCAM, cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
  # cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)
  cap.set(cv2.CAP_PROP_ZOOM, 300)
  cap.set(cv2.CAP_PROP_FOCUS, 80)
  # cap.set(cv2.CAP_PROP_FOCUS, 140)
  # cap.set(cv2.CAP_PROP_EXPOSURE, 2)

  if not cap.isOpened():
    raise Exception("Camera not found")
  return cap

def decode(cap):
  _, im = cap.read()
  gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
  _, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  if(im is not None):
    decodedObjects = pylibdmtx.decode(im, timeout=200, max_count=1)
    if len(decodedObjects) > 0:
      x, y, w, h = decodedObjects[0].rect
      im = cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.imshow("frame", im)
    cv2.waitKey(1)
    return decodedObjects
  return None

while True:
  try:
    cap = initCamera()
    print('Inicialização OK')
    while(True):
        info = decode(cap)
        if len(info) == 0:
            continue
        serial = info[0].data
        if serial == lastBarCode:
            continue
        print(serial.decode('ascii'))
  except Exception as e:
    print(e)
    sleep(1)

      
      
