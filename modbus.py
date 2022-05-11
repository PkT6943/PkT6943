from pyModbusTCP.client import ModbusClient
import time


def configure(server, port):

    client = ModbusClient()

    client.host(server)
    client.port(port)
    client.open()

    if client.is_open():
        print("Modbus connection successfully established at ", server, ":", port)

    return client

# Send single value for angle of rotation of the box


def sendAngleValue(client, address, a):
    client.write_single_register(address, a*10)

# Send 3 values of x, y, z for a coordinate of an object


def sendPointCoordinates(client, address, x, y, z):
    client.write_single_register(address, x*10)
    client.write_single_register(address+1, y*10)
    client.write_single_register(address+2, z*10)
