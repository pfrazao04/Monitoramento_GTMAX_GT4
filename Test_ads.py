import board
import busio
import adafruit_ads1x15.ads1115 as ADS    # Biblioteca ADS1115
import time as t
import csv
import datetime as dt
from adafruit_ads1x15.analog_in import AnalogIn  # Leitura de entrada analogica

i2c = busio.I2C(board.SCL, board.SDA)    #Comunicacao I2C
ads = ADS.ADS1115(i2c)
ads.data_rate= 860      #Frequencia de amostragem

date= dt.date.today().strftime("%d_%m_%Y")
file_number= 0
f= "./dados_csv/Impressao_{}.csv".format(date)

while True:
    try:
        file= open(f, "x", newline='')
        break
    except Exception:
        file_number+= 1
        f= "./dados_csv/Impressao_{}_({}).csv".format(date, file_number)

writer= csv.writer(file)

data= ["Tempo",
       "Valor A0 bits","Valor A0 Volts",
       "Valor A1 bits","Valor A1 Volts",
       "Valor A2 bits","Valor A2 Volts",
       "Valor A3 bits","Valor A3 Volts"]

start= t.time()


def analog_A0():
    return AnalogIn(ads, ADS.P0)

def analog_A1():
    return AnalogIn(ads, ADS.P1)

def analog_A2():
    return AnalogIn(ads, ADS.P2)

def analog_A3():
    return AnalogIn(ads, ADS.P3)

def time():
    end= t.time()
    return end - start
try:
    writer.writerow(data)
    file.flush()
    
    while True:

        # Payload: Tempo de impressao, Valor em bits das entradas analogicas , Valor de tensão das entradas analogicas   
        data= [time(),
               analog_A1().value, analog_A1().voltage,
               analog_A1().value, analog_A1().voltage,
               analog_A2().value, analog_A2().voltage,
               analog_A3().value, analog_A3().voltage ]
        
    
        print('A0: ',analog_A0().voltage,
              'A1: ',analog_A1().voltage,
              'A2: ',analog_A2().voltage,
              'A3: ',analog_A0().voltage, end='\r')
        
        
        writer.writerow(data)
        file.flush()
        
        #t.sleep(1)

# Ctrl + C p/ finalizar a leitura de dados
except KeyboardInterrupt:
    for i in range(len(data)):
        data[i]= "END"
    writer.writerow(data)
    file.close()