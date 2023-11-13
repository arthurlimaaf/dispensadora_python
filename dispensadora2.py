import asyncio
import cv2
import socketio
import pyautogui
from time import sleep
from pyModbusTCP.client import ModbusClient
from pylibdmtx import pylibdmtx
import mysql.connector
from mysql.connector import Error
import os.path
import os
import sys

c = ModbusClient(host="192.168.0.10", auto_open=True, auto_close=True)

sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=1, reconnection_delay_max=5, randomization_factor=0.5,
                     logger=True, serializer='default', json=None, handle_sigint=True)

sio.connect(f'http://192.168.0.60:7500')

indexCAM = 0
lastBarCode = ""
i = 0

def initCamera():
  cap = cv2.VideoCapture(indexCAM, cv2.CAP_DSHOW)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
  # cap.set(cv2.CAP_PROP_AUTOFOCUS, 2)
  cap.set(cv2.CAP_PROP_ZOOM, 300)
  cap.set(cv2.CAP_PROP_FOCUS, 70)
  # cap.set(cv2.CAP_PROP_EXPOSURE, 70)
  # cap.set(cv2.CAP_PROP_FOCUS, 140)
  # cap.set(cv2.CAP_PROP_EXPOSURE, 1)

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
    cv2.imwrite('barcode.jpg', im)
    # cv2.imshow("frame", im)
    # cv2.waitKey(1)
    return decodedObjects
  return None

while True:
  try:
    cap = initCamera()
    print('Inicialização OK')
    while(True):
        Value1 = c.read_holding_registers(202, 1)
        Value2 = c.read_holding_registers(204, 1)
        info = decode(cap)
        if (Value1 == [1]):
          sleep(0.5)
          for i in range(0, 7):
            sys.stdout.write("\r{}".format(i))
            sys.stdout.flush()
            sleep(1)
            info = decode(cap)
            if len(info) == 0 and i == 6:
              print("Sem label")
              c.write_single_register(118, 1)
              sleep(0.5)
              c.write_single_register(204, 1)
              sleep(0.5)
              c.write_single_register(202, 0)
              continue
            elif len(info) == 0:
                continue
            serial = info[0].data
            if serial == lastBarCode:
                continue 
            datamatrix = serial.decode('ascii')
            con = mysql.connector.connect(
            host='localhost', database='auto_loading', user='root', password='')
            cursor = con.cursor()
            seleciona = "SELECT datamatrix FROM loading WHERE datamatrix = '{}'".format(datamatrix)
            cursor.execute(seleciona)
            resultado = cursor.fetchall()
            if len(resultado) == 0 or len(resultado) != 0:
              print(datamatrix)
              pyautogui.write(datamatrix)
              pyautogui.press('Enter')
              c.write_single_register(204, 1)
              sleep(1)
            lastBarCode = serial
            break

        elif(Value1 == [0]):
          print("Aguardando Placa!")
          sleep(1)

  except Exception as e:
    print(e)
    sleep(1)

      
      
