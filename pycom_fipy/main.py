from network import LTE
import socket
import time
import machine
import ujson
from energyConsumption import EnergyConsumption
from dotenv import load_dotenv
import os

if __name__ == '__main__':
  load_dotenv()
  lte = LTE()
  lte.attach()
  while not lte.isattached():
      time.sleep(0.25)
  lte.connect()
  while not lte.isconnected():
      time.sleep(0.25)
  
  NIFI_IP = os.getenv('NIFI_IP')
  SERVER_PORT = int(os.getenv('PORT'))
  
  def sendToNifi(data):
      try:
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((SERVER_IP, SERVER_PORT))
          s.sendall(data.encode('utf-8'))
          s.close()
          print(f'Data sent to Nifi\nData: {data}')
      except Exception as e:
          print(f'Error: {e} occured while sending data')
  
  while True:
      try:
          energy_data = EnergyConsumption()
          data = ujson.dumps(energy_data)
          sendToNifi(data)
          time.sleep(60)
      except Exception as e:
          print(f'An error occured while sending the data to the server: {e}')
          
          machine.reset()
