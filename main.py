from djitellopy import tello
from rich import print
from time import sleep
import numpy
import cv2


TELLO_IP = '192.168.10.1'
TELLO_PORT = '8889'
FB_RANGE = [6200, 6800]
PID = [0.4, 0.4, 0]
P_ERROR = 0


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


def find_face(img):
    face_cascade = cv2.CascadeClassifier("Resources\haarcascade_frontalface_default.xml")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.2, 8)
    
    myFaceListCenter = []
    myFaceListArea = []

    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + (w // 2)
        cy = y + (h // 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListCenter.append([cx, cy])
        myFaceListArea.append(area)
    
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListCenter[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def track_face(my_tello, info, w):
    fb = 0
    x, y = info[0]
    area = info[1]
    error = x - (w // 2)
    speed = (PID[0] * error) + (PID[1] * (error - P_ERROR)) 
    speed = int(numpy.clip(speed, -100, 100))

    if area > FB_RANGE[0] and area < FB_RANGE[1]:   # No change ->
        fb = 0                                      # Drone stay still.
    if area > FB_RANGE[1]:                          # Object is too close ->
        fb = -20                                    # Drone moves backwards.
    elif area < FB_RANGE[0] and area != 0:          # Object is too far ->
        fb = 20                                     # Drone moves forwards.
    
    if x == 0:
        speed = 0
        error = 0

    my_tello.send_rc_control(0, fb, 0, speed)
    return error


def face_tracking_tello(my_tello):
    my_tello.streamon()
    fly_drone(my_tello)
    my_tello.send_rc_control(0, 0, 25, 0)
    sleep(2.2)
    flying = True

    while flying:
        img = my_tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        img, info = find_face(img)
        P_ERROR = track_face(my_tello, info, 360)
        cv2.imshow("Face Tracking Tello", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            land_drone(my_tello)
            flying = False


def main():
    try:
        print("[bold yellow]Connecting to TELLO...")
        me = tello.Tello()
        me.connect()
        print_battery_drone(me)

        face_tracking_tello(me)

        # stream_video_from_drone(me)
        # fly_drone(me)
        # sleep(1)
        # print("[bold yellow]Prepare for landing...")
        # land_drone(me)
    
    except KeyboardInterrupt:
        print("[bold red]Stopped.")
        exit()
    except Exception:
        print("[bold red]Error occurred.")
        exit()


if __name__ == '__main__':
    main()
