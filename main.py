from djitellopy import tello
from rich import print
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


def main():
    me = tello.Tello()
    me.connect()
    print_battery_drone(me)

    stream_video_from_drone(me)


if __name__ == '__main__':
    main()
