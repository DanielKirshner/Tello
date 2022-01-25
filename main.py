from djitellopy import tello
from rich import print
from time import sleep
import numpy as np
import cv2


TELLO_IP = '192.168.10.1'
TELLO_PORT = '8889'


def print_battery_drone(my_tello):
    bat = my_tello.get_battery()
    if bat >= 65:
        print(f"[bold green]Battery = {bat}%")
    elif bat >= 25:
        print(f"[bold yellow]Battery = {bat}%")
    else:
        print(f"[bold red]Battery = {bat}%")


def stream_video_from_drone(my_tello):
    my_tello.streamon()
    while True:
        img = my_tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240)) # There is a small delay so smaller resolution is better
        cv2.imshow("Tello Live", img)
        cv2.waitKey(1)


def fly_drone(my_tello):
    my_tello.takeoff()


def land_drone(my_tello):
    my_tello.land()


def face_tracking():
    CAMERA_INDEX = 0 # if you have multiple tellos/cameras you need to change it to 1,2,3, etc...
    cap = cv2.VideoCapture(CAMERA_INDEX)
    



def main():
    try:
        print("[bold yellow]Connecting to TELLO...")
        me = tello.Tello()
        me.connect()
        print_battery_drone(me)
        # stream_video_from_drone(me)
        fly_drone(me)
        sleep(1) # Stay in the air for 1 second
        print("[bold yellow]Prepare for landing...")
        land_drone(me)
    
    except KeyboardInterrupt:
        print("[bold red]Stopped.")
        # if me.is_flying():
            # land_drone(me)
        exit()
    except Exception:
        print("[bold red]Error occurred.")
        exit()


if __name__ == '__main__':
    main()
