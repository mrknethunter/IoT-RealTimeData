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
          print("Dati inviati con successo a NiFi:", data)
      except Exception as e:
          print("Errore durante l'invio dei dati a NiFi:", e)
  
  while True:
      try:
          energy_data = EnergyConsumption()
          json_data = ujson.dumps(energy_data)
          sendToNifi(json_data)
          time.sleep(60)
      except Exception as e:
          print("Errore durante l'invio dei dati:", e)
          
          machine.reset()
