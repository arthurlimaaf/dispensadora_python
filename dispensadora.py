import cv2
from time import sleep
import pyautogui
from pylibdmtx import pylibdmtx

indexCAM = 1
lastBarCode = b''
lastBarCode2 = b''
lastBarCode3 = b''
lastBarCode4 = b''

def initCamera():
  cap = cv2.VideoCapture(indexCAM, cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
  # cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)
  cap.set(cv2.CAP_PROP_ZOOM, 300)
  cap.set(cv2.CAP_PROP_FOCUS, 40)
  # cap.set(cv2.CAP_PROP_FOCUS, 140)
  # cap.set(cv2.CAP_PROP_EXPOSURE, 2)
 
  if not cap.isOpened():
    raise Exception("Camera not found")
  return cap

# LEITURA DO DATAMATRIX 1
def decode(cap):
  _, im = cap.read()
  frame = im[50: 200, 70: 300]
  gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  _, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  if(frame is not None):
    decodedObjects = pylibdmtx.decode(frame, timeout=200, max_count=1)
    if len(decodedObjects) > 0:
      x, y, w, h = decodedObjects[0].rect
      frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    return decodedObjects
  return None

# LEITURA DO DATAMATRIX 2
def decode2(cap):
  _, im = cap.read()
  frame = im[50: 200, 260: 400]
  gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  _, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  if(frame is not None):
    decodedObjects = pylibdmtx.decode(frame, timeout=200, max_count=1)
    if len(decodedObjects) > 0:
      x, y, w, h = decodedObjects[0].rect
      frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    return decodedObjects
  return None

# LEITURA DO DATAMATRIX 3
def decode3(cap):
  _, im = cap.read()
  frame = im[50: 200, 390: 510]
  gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  _, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  if(frame is not None):
    decodedObjects = pylibdmtx.decode(frame, timeout=200, max_count=1)
    if len(decodedObjects) > 0:
      x, y, w, h = decodedObjects[0].rect
      frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)
    return decodedObjects
  return None

# LEITURA DO DATAMATRIX 4
def decode4(cap):
  _, im = cap.read()
  frame = im[50: 200, 520: 650]
  gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  _, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  if(frame is not None):
    decodedObjects = pylibdmtx.decode(frame, timeout=200, max_count=1)
    if len(decodedObjects) > 0:
      x, y, w, h = decodedObjects[0].rect
      frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.imshow("frame", frame)
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
        serial1 = serial.decode('ascii')
        pyautogui.write(serial1)
        pyautogui.press('Enter')
        lastBarCode = serial
        sleep(1)

        info = decode2(cap)
        if len(info) == 0:
            continue
        serial = info[0].data
        if serial == lastBarCode2:
            continue
        print(serial.decode('ascii'))
        serial2 = serial.decode('ascii')
        pyautogui.write(serial2)
        pyautogui.press('Enter')
        lastBarCode2 = serial
        sleep(1)

        info = decode3(cap)
        if len(info) == 0:
            continue
        serial = info[0].data
        if serial == lastBarCode3:
            continue
        print(serial.decode('ascii'))
        serial3 = serial.decode('ascii')
        pyautogui.write(serial3)
        pyautogui.press('Enter')
        lastBarCode3 = serial
        sleep(1)

        info = decode4(cap)
        if len(info) == 0:
            continue
        serial = info[0].data
        if serial == lastBarCode4:
            continue
        print(serial.decode('ascii'))
        serial4 = serial.decode('ascii')
        pyautogui.write(serial4)
        pyautogui.press('Enter')
        lastBarCode4 = serial
        sleep(1)
        
  except Exception as e:
    print(e)
    sleep(1)

      
      
