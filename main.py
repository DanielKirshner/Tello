from djitellopy import tello

TELLO_IP = '192.168.10.1'
TELLO_PORT = '8889'

print("Connecting to TELLO...")
me = tello.Tello()
me.connect()

print(f"{me.get_battery()}%")
