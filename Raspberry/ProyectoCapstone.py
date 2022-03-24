import paho.mqtt.client as mqtt #Se importa cliente MQTT
import socket #Se importa la libreria para comuicación Ethernet UDP
import sys
import time
###################
def on_message(client, userdata, message):
    datosInterface=str(message.payload.decode("utf-8"))
    print("message received " ,datosInterface)
    sent = sock.sendto(datosInterface.encode(), PLCadress)
    print('se enviaron {} bytes back to {}'.format(sent, PLCadress))
            

###############
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('192.168.1.106', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

PLCadress= ('192.168.1.160',10000)

########################################

client = mqtt.Client("anto2") #create new instance
client.on_message=on_message #attach function to callback
client.connect("192.168.1.105", 1883, 60) #connect to broker


while True:
    print('\Esperando a recibir mensaje UDP desde PLC')
    dato, address = sock.recvfrom(4096)
    print('received {} bytes from {}'.format(len(dato), address))
    datosPLC=str(dato.decode("utf-8"))
    print(datosPLC)
    client.publish('codigoIoT/py/EstadoProceso', payload= datosPLC, qos=0, retain=False)
    #else:
        #client.publish('codigoIoT/py/EstadoProceso', payload= 'error PLC', qos=0, retain=False)
        
    print("Esperando a recibir mensaje MQTT")
    client.loop_start() #start the loop
    client.subscribe("codigoIoT/py/DataIni")
    time.sleep(1) # wait
    client.loop_stop() #stop the loop 
